# Differences between 1.0 and 1.3 implementation:
# + Additionally to a MAIN_DISPATCHER a CONFIG_DISPATCHER has been added
#   - The CONFIG_DISPATCHER answers to SwitchFeature Requests and adds a flow to itself which is a generic table-miss flow entry in case if this
#     table-miss occurs the packet will be send to the controller
# + Some api changes in FlowMod, now next to actions there are also instructions which can perform actions but also are capable of switches between tables e.g.
# + Also buffer ids have been introduced which can be added to new Flow Modifications
#
#
# Maximum number of rules:
#
# The theoretical amount of rules can be determined by having a look at the structure of flow rules in OpenFlow 1.0.
#
# |Switch Port              | MAC src | MAC dst | Eth type   | VLAN ID | IPsrc(v4) | IP dst | TCP sport | TCP dport|
# |-------------------------|---------|---------|------------|---------|-----------|--------|-----------|----------|
# | number of hardware ports| 2^48    | 2^48    |4 diff types| 2^16    | 2^32      | 2^32   | 65535     | 65535    |
#
# This configuration would be correct for the maximum number of rules configurable due to the restriction to only one flow table.
# But we can restrict that number to useful application rules in our used topology (or any other topology depending on the structure of it).
#
# in the example
# |Switch Port | MAC src | MAC dst | Eth type   | VLAN ID | IPsrc(v4) | IP dst | TCP sport(in example host) | TCP dport|
# |------------|---------|---------|------------|---------|-----------|--------|----------------------------|----------|
# | 3          | 4       | 4       |4 diff types| 1       | 4         | 4      | 1000                       | 1000     |
#
# So only around 3072000000 rules that can at maxmimum be defined.
#
# For OpenFlow 1.3 though we can extend this since we no longer have a single flow table but multiple which can interlink each other,
# using this we not only can create theoretically as many rules as required we also can simplify them by using links from one table to another to group certain actions e.g. in multi-tenancy systems,
# so the upper limit will always be defined by the maximum number of rules the switch can hold.
#
# // Used partly as source: https://blog.ipspace.net/2013/10/flow-table-explosion-with-openflow-10.html


import struct
import logging

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types

FILTER_TABLE = 0
FORWARD_TABLE = 15


class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

        # To set defaults which should be checked by the switch first
        self.add_filter_table(datapath)


    # Add flow to filter table which links to forward table
    def add_filter_table(self, datapath):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_CLEAR_ACTIONS, [])]
        mod = parser.OFPFlowMod(datapath=datapath, table_id=FILTER_TABLE,
                                priority=1, instructions=inst)
        datapath.send_msg(mod)


    # Rules for filter table
    def apply_filter_table_rules(self, datapath, match):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        inst = [parser.OFPInstructionGotoTable(FORWARD_TABLE)]
        mod = parser.OFPFlowMod(datapath=datapath, table_id=FILTER_TABLE,
                                priority=ofproto.OFP_DEFAULT_PRIORITY, match=match, instructions=inst)
        datapath.send_msg(mod)


    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = datapath.ofproto_parser.OFPFlowMod(
                datapath=datapath, match=match, cookie=0,
                command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                priority=ofproto.OFP_DEFAULT_PRIORITY,
                flags=ofproto.OFPFF_SEND_FLOW_REM, instructions=inst, buffer_id=buffer_id)
        else:
            mod = datapath.ofproto_parser.OFPFlowMod(
                datapath=datapath, match=match, cookie=0,
                command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                priority=ofproto.OFP_DEFAULT_PRIORITY,
                flags=ofproto.OFPFF_SEND_FLOW_REM, instructions=inst)
        datapath.send_msg(mod)


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time and enforce the one mac
        # address per port rule
        print("s%s: in_port=%s known ports=%s" % (dpid, in_port, self.mac_to_port[dpid].values()))
        if in_port >= 3:
            match = parser.OFPMatch(in_port=in_port, eth_src=eth.src)
            self.logger.info("add >=3 packet on s%s src=%s dst=%s in_port=%s", dpid, src, dst, in_port)
            self.mac_to_port[dpid][src] = in_port
            self.apply_filter_table_rules(datapath, match)
        elif src in self.mac_to_port[dpid] or in_port not in self.mac_to_port[dpid].values():
            match = parser.OFPMatch(in_port=in_port, eth_src=eth.src)
            self.logger.info("add < 3 packet on s%s src=%s dst=%s in_port=%s", dpid, src, dst, in_port)
            self.mac_to_port[dpid][src] = in_port
            self.apply_filter_table_rules(datapath, match)
        else:
            self.logger.info("spoof")
            return


        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            if in_port > 3:
                match = parser.OFPMatch(in_port=in_port, eth_src=src, eth_dst=dst)
            else:
                match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)


    @set_ev_cls(ofp_event.EventOFPPortStatus, MAIN_DISPATCHER)
    def _port_status_handler(self, ev):
        msg = ev.msg
        reason = msg.reason
        port_no = msg.desc.port_no

        ofproto = msg.datapath.ofproto
        if reason == ofproto.OFPPR_ADD:
            self.logger.info("port added %s", port_no)
        elif reason == ofproto.OFPPR_DELETE:
            self.logger.info("port deleted %s", port_no)
        elif reason == ofproto.OFPPR_MODIFY:
            self.logger.info("port modified %s", port_no)
        else:
            self.logger.info("Illeagal port state %s %s", port_no, reason)

