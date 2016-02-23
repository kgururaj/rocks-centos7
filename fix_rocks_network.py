#!/usr/bin/env python

import sys
import subprocess
import json
import socket
import shutil
import os
import ipaddress

def exit_if_error(ret_code):
    if(ret_code != 0):
        raise RuntimeError('Error');

def sync_network(hostname):
    rocks_hostname = hostname.split('.')[0];
    subprocess.call('rocks sync config', shell=True);
    subprocess.call('rocks sync host network '+rocks_hostname, shell=True);

def get_ip_for_interface(eth):
    cmd='ip -f inet -o addr show dev '+eth;
    pid = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE);
    stdout_str = pid.communicate()[0];
    if(pid.returncode != 0):
        return '';
    tokens = stdout_str.split();
    if(len(tokens) >= 4):
        return tokens[3].split('/')[0];
    else:
        return '';

def get_subnet(ipaddr, netmask):
    if(ipaddr == '' or netmask == ''):
        return '';
    interface = ipaddress.IPv4Interface(unicode(ipaddr+'/'+netmask));
    subnet_with_prefix = str(interface.network);
    tokens = subnet_with_prefix.split('/');
    return tokens[0];

def get_prefix_length(ipaddr, netmask):
    if(ipaddr == '' or netmask == ''):
        return '';
    interface = ipaddress.IPv4Interface(unicode(ipaddr+'/'+netmask));
    return str(interface.network.prefixlen);

def get_broadcast_address(ipaddr, netmask):
    if(ipaddr == '' or netmask == ''):
        return '';
    interface = ipaddress.IPv4Interface(unicode(ipaddr+'/'+netmask));
    return str(interface.network.broadcast_address);

def get_rocks_attr(attr_name):
    pid = subprocess.Popen('rocks list attr | grep '+attr_name, shell=True, stdout=subprocess.PIPE);
    stdout_str = pid.communicate()[0];
    if(pid.returncode != 0):
        return '';
    tokens = stdout_str.split()
    if(len(tokens) >= 2):
        return tokens[1];
    else:
        return '';

def fix_rocks_hostname(hostname):
    old_rocks_hostname = socket.gethostname().split('.')[0];
    new_rocks_hostname = hostname.split('.')[0];
    cmd='sed -i \'/HOSTNAME/d\' /etc/sysconfig/network';
    ret = subprocess.call(cmd, shell=True);
    cmd='sed -i \'$ a\\\nHOSTNAME='+new_rocks_hostname+'\' /etc/sysconfig/network';
    ret = subprocess.call(cmd, shell=True);
    ret = subprocess.call('hostname '+new_rocks_hostname, shell=True);
    if(old_rocks_hostname != new_rocks_hostname):
        ret = subprocess.call('rocks set host name '+old_rocks_hostname+' '+new_rocks_hostname, shell=True);
        ret = subprocess.call('rocks set attr Kickstart_PublicHostname '+new_rocks_hostname, shell=True);
        ret = subprocess.call('rocks set attr Kickstart_PrivateHostname '+new_rocks_hostname, shell=True);
    if(len(hostname.split('.')) > 1):
        subprocess.call('rocks add host alias '+new_rocks_hostname+' '+hostname, shell=True);

def fix_rocks_private_interface(private_eth_params):
    hostname = socket.gethostname();
    rocks_hostname = hostname.split('.')[0];
    old_eth = get_rocks_attr('Kickstart_PrivateInterface');
    eth = old_eth;
    ipaddr = get_ip_for_interface(eth);
    if('name' in private_eth_params):
        eth = private_eth_params['name'];
        if(eth != old_eth):
            subprocess.call('rocks remove host interface '+rocks_hostname+' '+old_eth, shell=True);
            subprocess.call('rocks remove host interface '+rocks_hostname+' '+eth, shell=True);
            status = subprocess.call('rocks add host interface '+rocks_hostname+' '+eth+' subnet=private name='+rocks_hostname, shell=True);
            if(status == 0):
                subprocess.call('rocks set attr Kickstart_PrivateInterface '+eth, shell=True);
            return True;
    if('ip' in private_eth_params):
        subprocess.call('rocks set host interface ip '+rocks_hostname+' '+eth+' '+private_eth_params['ip'], shell=True);
        subprocess.call('rocks set attr Kickstart_PrivateAddress '+private_eth_params['ip'], shell=True);
        ipaddr = private_eth_params['ip'];
    if('gateway' not in private_eth_params):
        private_eth_params['gateway'] = ipaddr;
    subprocess.call('rocks remove route 0.0.0.0', shell=True);
    subprocess.call('rocks add route 0.0.0.0 '+private_eth_params['gateway']+ ' netmask=0.0.0.0', shell=True);
    subprocess.call('rocks set attr Kickstart_PrivateGateway '+private_eth_params['gateway'], shell=True);
    subprocess.call('rocks set attr Kickstart_PrivateNTPHost '+private_eth_params['gateway'], shell=True);
    if(private_eth_params['gateway'] != ipaddr):
      unique_name = 'internal-gateway';
      if('gateway_name' in private_eth_params):
	unique_name = private_eth_params['gateway_name'];
      if(rocks_hostname == unique_name):
	unique_name = unique_name+'-'+str(os.urandom(2));
      subprocess.call('rocks add host '+unique_name+' cpus=1 membership="Ethernet Switch" rack=0 rank=0', shell=True);
      subprocess.call('rocks add host interface '+unique_name+' eth0 ip='+private_eth_params['gateway']+' subnet=private', shell=True);
      private_eth_params['gateway_name'] = unique_name;
    if('gateway_name' in private_eth_params and private_eth_params['gateway_name'] != 'gateway'):
      subprocess.call('rocks add host alias '+private_eth_params['gateway_name']+' gateway ', shell=True);
    if('vm_host_name' in private_eth_params and 'vm_host' in private_eth_params):
      unique_name = private_eth_params['vm_host_name'];
      subprocess.call('rocks add host '+unique_name+' cpus=1 membership="Ethernet Switch" rack=0 rank=0', shell=True);
      subprocess.call('rocks add host interface '+unique_name+' eth0 ip='+private_eth_params['vm_host']+' subnet=private', shell=True);
    if('netmask' in private_eth_params):
        subprocess.call('rocks set network netmask private '+private_eth_params['netmask'], shell=True);
        subprocess.call('rocks set attr Kickstart_PrivateNetmask '+private_eth_params['netmask'], shell=True);
        subnet_value = get_subnet(ipaddr, private_eth_params['netmask']);
        if(subnet_value != ''):
            subprocess.call('rocks set network subnet private '+subnet_value, shell=True);
            subprocess.call('rocks set attr Kickstart_PrivateNetwork '+subnet_value, shell=True);
    if('netmask' in private_eth_params and 'ip' in private_eth_params):
        broadcast_address = get_broadcast_address(private_eth_params['ip'], private_eth_params['netmask']);
        subprocess.call('rocks set attr Kickstart_PrivateBroadcast '+broadcast_address, shell=True);
        prefix_length = get_prefix_length(private_eth_params['ip'], private_eth_params['netmask']);
        subprocess.call('rocks set attr Kickstart_PrivateNetmaskCIDR '+prefix_length, shell=True);
    if('zone' in private_eth_params):
        pid = subprocess.Popen('rocks list network private|grep -v SUBNET', shell=True, stdout=subprocess.PIPE);
        stdout_str = pid.communicate()[0];
        old_zone = stdout_str.split()[3];
        if(old_zone != private_eth_params['zone']):
            subprocess.call('rocks set network zone private '+private_eth_params['zone'], shell=True);
        subprocess.call('rocks set attr Kickstart_PrivateDNSDomain '+private_eth_params['zone'], shell=True);
    subprocess.call('rocks set attr Kickstart_PrivateKickstartHost '+ipaddr, shell=True);
    subprocess.call('rocks set attr Kickstart_PrivateDNSServers '+ipaddr, shell=True);
    subprocess.call('rocks set attr Kickstart_PrivateSyslogHost '+ipaddr, shell=True);
    subprocess.call('rocks set attr dhcp_nextserver '+ipaddr, shell=True);
    subprocess.call('rocks set host attr '+rocks_hostname+' dhcp_nextserver '+ipaddr, shell=True);
    return False;

def fix_rocks_public_interface(public_eth_params):
    hostname = socket.gethostname();
    hostname_tokens = hostname.split('.');
    rocks_hostname = hostname_tokens[0];
    zone_from_hostname = '.'.join(hostname_tokens[1:]) if (len(hostname_tokens) > 1) else '';
    old_eth = get_rocks_attr('Kickstart_PublicInterface');
    eth = old_eth;
    ipaddr = get_ip_for_interface(eth);
    if('name' in public_eth_params):
        eth = public_eth_params['name'];
        if(eth != old_eth):
            subprocess.call('rocks remove host interface '+rocks_hostname+' '+old_eth, shell=True);
            subprocess.call('rocks remove host interface '+rocks_hostname+' '+eth, shell=True);
            status = subprocess.call('rocks add host interface '+rocks_hostname+' '+eth+' subnet=public name='+rocks_hostname, shell=True);
            if(status == 0):
                subprocess.call('rocks set attr Kickstart_PublicInterface '+eth, shell=True);
            return True;
    if('ip_source' in public_eth_params):
        if(public_eth_params['ip_source'] == 'static'):
            if('ip' in public_eth_params):
                subprocess.call('rocks set host interface ip '+rocks_hostname+' '+eth+' '+public_eth_params['ip'], shell=True);
                ipaddr = public_eth_params['ip'];
        else:
            subprocess.call('rocks set host interface ip '+rocks_hostname+' '+eth+' ip=NULL', shell=True);
            subprocess.call('rocks set host interface options '+rocks_hostname+' '+eth+' options="dhcp"', shell=True);
            #Get info from leases file
            lease_file='/var/lib/dhclient/dhclient-'+eth+'.leases';
            shutil.rmtree(lease_file, ignore_errors=True);
            sync_network(rocks_hostname);
            ipaddr = get_ip_for_interface(eth);
            public_eth_params['ip'] = ipaddr
            fptr = open(lease_file, 'rb');
            for line in fptr:
                tokens = line.split();
                if(len(tokens) >= 3 and tokens[0] == 'option'):
                    value = tokens[2].replace(';', '');
                    if(tokens[1] == 'subnet-mask' and 'netmask' not in public_eth_params):
                        public_eth_params['netmask'] = value; 
                    elif(tokens[1] == 'routers' and 'gateway' not in public_eth_params):
                        first_router = value.split(',')[0];     #could be list
                        public_eth_params['gateway'] = first_router;
                    elif(tokens[1] == 'domain-name' and 'zone' not in public_eth_params):
                        public_eth_params['zone'] = value;
                    elif(tokens[1] == 'domain-name-servers' and 'dnsservers' not in public_eth_params):
                        public_eth_params['dnsservers'] = value.split(',');
            fptr.close();
    if('zone' not in public_eth_params and zone_from_hostname != ''):
        public_eth_params['zone'] = zone_from_hostname;
    if('ip' in public_eth_params):
        subprocess.call('rocks set attr Kickstart_PublicAddress '+public_eth_params['ip'], shell=True);
    if('gateway' in public_eth_params):
        subprocess.call('rocks remove host route '+rocks_hostname+' 0.0.0.0', shell=True);
        subprocess.call('rocks add host route '+rocks_hostname+' 0.0.0.0 '+public_eth_params['gateway']+ ' netmask=0.0.0.0', shell=True);
        subprocess.call('rocks set attr Kickstart_PublicGateway '+public_eth_params['gateway'], shell=True);
    if('netmask' in public_eth_params):
        subprocess.call('rocks set network netmask public '+public_eth_params['netmask'], shell=True);
        subprocess.call('rocks set attr Kickstart_PublicNetmask '+public_eth_params['netmask'], shell=True);
        subnet_value = get_subnet(ipaddr, public_eth_params['netmask']);
        if(subnet_value != ''):
            subprocess.call('rocks set network subnet public '+subnet_value, shell=True);
            subprocess.call('rocks set attr Kickstart_PublicNetwork '+subnet_value, shell=True);
    if('netmask' in public_eth_params and 'ip' in public_eth_params):
        broadcast_address = get_broadcast_address(public_eth_params['ip'], public_eth_params['netmask']);
        subprocess.call('rocks set attr Kickstart_PublicBroadcast '+broadcast_address, shell=True);
        prefix_length = get_prefix_length(public_eth_params['ip'], public_eth_params['netmask']);
        subprocess.call('rocks set attr Kickstart_PublicNetmaskCIDR '+prefix_length, shell=True);
    if('zone' in public_eth_params):
        pid = subprocess.Popen('rocks list network public|grep -v SUBNET', shell=True, stdout=subprocess.PIPE);
        stdout_str = pid.communicate()[0];
        old_zone = stdout_str.split()[3];
        if(old_zone != public_eth_params['zone']):
            subprocess.call('rocks set network zone public '+public_eth_params['zone'], shell=True);
        subprocess.call('rocks set attr Kickstart_PublicDNSDomain '+public_eth_params['zone'], shell=True);
    if('dnsservers' in public_eth_params):
        subprocess.call('rocks set attr Kickstart_PublicDNSServers '+','.join(public_eth_params['dnsservers']), shell=True);
    return False;

def fix_resolv_conf():
    public_domain = get_rocks_attr('Kickstart_PublicDNSDomain');
    private_domain = get_rocks_attr('Kickstart_PrivateDNSDomain');
    private_dns_server = get_rocks_attr('Kickstart_PrivateDNSServers');
    fptr = open('/etc/resolv.conf', 'wb');
    fptr.write('search '+public_domain+' '+private_domain+'\n');
    fptr.write('nameserver '+private_dns_server+'\n');
    fptr.close();

#Set PEERDNS=no on public network interface ifcfg script
def fix_peer_dns():
    eth = get_rocks_attr('Kickstart_PublicInterface');
    if(eth != ''):
	local_eth_file =  '/etc/sysconfig/network-scripts/ifcfg-'+eth;
	if(os.path.exists(local_eth_file)):
	    subprocess.call('sed -i \'/PEERDNS/d\' '+local_eth_file, shell=True);
	    subprocess.call('sed -i \'$ a\\\nPEERDNS=no\' '+local_eth_file, shell=True);
	    rocks_hostname = socket.gethostname().split('.')[0];
	    subprocess.call('rocks set host interface options '+rocks_hostname+' iface='+eth+' options="noreport"', shell=True);
	else:
	    fptr = open(local_eth_file, 'wb');
	    fptr.write('PEERDNS=no\n');
	    fptr.close();

def fix_rocks_network(json_file):
    with open(json_file) as data_file:    
        params = json.load(data_file);
        public_rerun = False;
        private_rerun = False;
        if('hostname' in params):
            fix_rocks_hostname(params['hostname']);
        if('public_eth' in params):
            public_rerun = fix_rocks_public_interface(params['public_eth']);
        if('private_eth' in params):
            private_rerun = fix_rocks_private_interface(params['private_eth']);
        sync_network(socket.gethostname());
        if(public_rerun):
            fix_rocks_public_interface(params['public_eth']);
        if(private_rerun):
            fix_rocks_private_interface(params['private_eth']);
        if(public_rerun or private_rerun):
            sync_network(socket.gethostname());
        fix_resolv_conf();
        fix_peer_dns();
        subprocess.call('cd /export/rocks/install && rocks create distro', shell=True);


if __name__ == "__main__":
    if(len(sys.argv) < 2):
        sys.stderr.write('Needs 1 file as argument <json_file>\n');
        sys.exit(-1);
    fix_rocks_network(sys.argv[1]);


