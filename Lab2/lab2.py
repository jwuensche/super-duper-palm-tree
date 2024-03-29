# Copyright (C) 2012 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
An OpenFlow 1.0 L2 learning switch implementation.
"""


from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0
from ryu.lib.mac import haddr_to_bin
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import icmp
from ryu.lib.mac import haddr_to_bin

class SimpleSwitch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch, self).__init__(*args, **kwargs)
        self.mac_to_port = {}

    def add_flow(self, datapath, in_port, dst, src, actions):
        ofproto = datapath.ofproto

        match = datapath.ofproto_parser.OFPMatch(
            in_port=in_port,
            dl_dst=haddr_to_bin(dst), dl_src=haddr_to_bin(src))

        self.logger.info("addflow %s %s %s %s",  src, dst, in_port, actions)

        mod = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath, match=match, cookie=0,
            command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
            priority=ofproto.OFP_DEFAULT_PRIORITY,
        flags=ofproto.OFPFF_SEND_FLOW_REM, actions=actions)
        datapath.send_msg(mod)

    def ipv4_to_int(self, string):
        ip = string.split('.')
        assert len(ip) == 4
        i = 0
        for b in ip:
            b = int(b)
            i = (i << 8) | b
        return i

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return

        # Mac addresses
        dst = eth.dst
        src = eth.src

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, msg.in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = msg.in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD


    	actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next tim3

        pkt = packet.Packet(data=msg.data)
        pkt_icmp = pkt.get_protocol(icmp.icmp)
 
        if pkt_icmp:

            targetHwAddr = "00:00:00:00:00:03"
            targetIpAddr = "10.0.0.3"
            output_port_1 = 2
            output_port_2 = 3

            if msg.in_port == 1:
                if dst == "00:00:00:00:00:03":
                    output_port_1 = 3
                    output_port_2 = 2
                    targetHwAddr = "00:00:00:00:00:02"
                    targetIpAddr = "10.0.0.2"
            if msg.in_port == 2:
                if dst == "00:00:00:00:00:03":
                    output_port_1 = 3
                    output_port_2 = 1
                    targetHwAddr = "00:00:00:00:00:01"
                    targetIpAddr = "10.0.0.1"
                if dst == "00:00:00:00:00:01":
                    output_port_1 = 1
                    output_port_2 = 3
                    targetHwAddr = "00:00:00:00:00:03"
                    targetIpAddr = "10.0.0.3"
            if msg.in_port == 3:
                if dst == "00:00:00:00:00:02":
                    output_port_1 = 2
                    output_port_2 = 1
                    targetHwAddr = "00:00:00:00:00:01"
                    targetIpAddr = "10.0.0.1"
                if dst == "00:00:00:00:00:01":
                    output_port_1 = 1
                    output_port_2 = 2
                    targetHwAddr = "00:00:00:00:00:02"
                    targetIpAddr = "10.0.0.2"

	    # At first output to target port, then change src mac and ip and output to third host that
	    # is not included in the ICMP transaction
            actions = [datapath.ofproto_parser.OFPActionOutput(output_port_1),
                 datapath.ofproto_parser.OFPActionSetDlDst(haddr_to_bin(targetHwAddr)),
                 datapath.ofproto_parser.OFPActionSetNwDst(self.ipv4_to_int(targetIpAddr)),
                 datapath.ofproto_parser.OFPActionOutput(output_port_2)]
            self.add_flow(datapath, msg.in_port, dst, src, actions)


        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath, buffer_id=msg.buffer_id, in_port=msg.in_port,
            actions=actions, data=data)
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


