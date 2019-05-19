#!/bin/sh
# Task 1 - Enable ping to all hosts
s1 dpctl add-flow tcp:127.0.0.1:6654  dl_dst=00:00:00:00:00:02,idle_timeout=0,actions=output:2
s1 dpctl add-flow tcp:127.0.0.1:6654  dl_dst=00:00:00:00:00:01,idle_timeout=0,actions=output:1
s1 dpctl add-flow tcp:127.0.0.1:6654  dl_dst=00:00:00:00:00:03,idle_timeout=0,actions=output:3

# Test with pingall

# Task 2 - Add firewall for SMTP packets matching Ports
s1 dpctl add-flow tcp:127.0.0.1:6654 ip,tcp,tp_dst=587,idle_timeout=0,priority=40000,actions=
s1 dpctl add-flow tcp:127.0.0.1:6654 ip,tcp,tp_dst=465,idle_timeout=0,priority=40000,actions=
s1 dpctl add-flow tcp:127.0.0.1:6654 ip,tcp,tp_dst=25,idle_timeout=0,priority=40000,actions=

# Test with h1 wget 10.0.0.2:25
# Before executing Task2 this should result in connection refused. 
# After executing Task2, the switch drops the packets and h1 stucks in connection attempting