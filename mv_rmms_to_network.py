#!/usr/bin/env python

import sys
import subprocess

if(len(sys.argv) < 4):
	sys.stderr.write("Needs 3 arguments <appliance> <network> <starting_ip>\n");
	sys.exit(-1)

appliance=sys.argv[1]
dst_network=sys.argv[2]
starting_ip=sys.argv[3]

do_config = False;
if(len(sys.argv) >= 5):
	do_config = sys.argv[4] in ['true', 'True', '1', 't', 'y', 'yes'];

ip_tokens=starting_ip.split('.')
curr_idx = int(ip_tokens[3]);

ph = subprocess.Popen('rocks list host', shell=True, stdout=subprocess.PIPE);

stdout_str = ph.communicate()[0]

host_lines = stdout_str.split('\n');
line_idx = 0;
for line in host_lines:
	if(line_idx > 0):
		tokens = line.split();
		if(len(tokens) >= 7):
			host_name = tokens[0].replace(':', '');
			appliance_type = tokens[1];
			if(appliance_type == appliance):
				ph2 = subprocess.Popen('rocks list host interface '+host_name, shell=True, stdout=subprocess.PIPE);
				interface_stdout_string = ph2.communicate()[0];
				interface_lines = interface_stdout_string.split('\n');
				interface_tokens = interface_lines[1].split();
				network = interface_tokens[0];
				if(network != dst_network):
					mac = interface_tokens[2];
					cmd = 'rocks set host interface subnet %s %s %s'%(host_name, mac, dst_network)
					if(do_config):
						subprocess.call(cmd, shell=True);
					else:
						print(cmd);
					cmd = 'rocks set host interface ip %s %s %s.%d'%(host_name, mac, '.'.join(ip_tokens[0:3]), curr_idx)
					curr_idx -= 1;
					if(do_config):
						subprocess.call(cmd, shell=True);
					else:
						print(cmd);
	line_idx += 1;

cmd='rocks sync config'
if(do_config):
	subprocess.call(cmd, shell=True);
else:
	print(cmd)
