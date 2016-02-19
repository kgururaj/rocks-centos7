#Copy this file to /opt/rocks/lib/python2.6/site-packages/rocks/commands/report/host/dhcpd/__init__.py
#
# $Id: __init__.py,v 1.31 2012/11/27 00:48:24 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 6.1.1 (Sand Boa)
# 
# Copyright (c) 2000 - 2014 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#
# $Log: __init__.py,v $
# Revision 1.31  2012/11/27 00:48:24  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.30  2012/10/01 04:42:34  phil
#
# Handle case when node hasn't yet reported it's interfaces (e.g. at discovery)
#
# Revision 1.29  2012/08/30 01:00:48  clem
# Fix for the dhcpd problem with duplicate host name with virtual host
#
# Revision 1.28  2012/05/06 05:48:32  phil
# Copyright Storm for Mamba
#
# Revision 1.27  2012/04/25 05:04:18  phil
# filter out long mac addresses coming from IB adapters.
#
# Revision 1.26  2012/04/07 04:06:37  phil
# Fix file names -- a missing d can ruin your day.
#
# Revision 1.25  2012/03/27 21:33:56  phil
# Right path name ... is now in the right place
#
# Revision 1.24  2012/03/27 17:11:22  clem
# Now even faster (variable lookup instead of DB lookup) ;-)
#
# Revision 1.23  2012/03/27 02:22:18  clem
# dhcpd.conf proper path name handlying recovered from previous commit
#
# Revision 1.22  2012/03/23 21:35:59  phil
# dhcpd.conf now down to two big (UNION) select statements instead of
# N. Takes less < 1 sec to complete on a 300 node test.
#
# Revision 1.19  2011/07/23 02:30:35  phil
# Viper Copyright
#
# Revision 1.18  2010/11/19 23:56:00  bruno
# convert dhcp configuration to output XML
#
# lookup the private interface name and write it to /etc/sysconfig/dhcpd
#
# Revision 1.17  2010/09/07 23:52:59  bruno
# star power for gb
#
# Revision 1.16  2010/07/27 01:29:24  anoop
# Bug fix
#
# Revision 1.15  2010/07/19 18:34:02  anoop
# Individually set "kickstartable", "dhcp_filename" and "dhcp_nextserver"
# attributes for every host/appliance. This way we can control which appliance
# gets the "dhcp_filename" option. This is to resolve a bug where setting
# the dhcp_filename option for devices like switches can cause problems for
# the devices
#
# Revision 1.14  2009/10/23 17:21:44  bruno
# user-settable lease times. a feature submitted by Tim Carlson.
#
# Revision 1.13  2009/08/14 20:40:48  bruno
# put double quotes around domain name. bug reported by Yu Fu.
#
# Revision 1.12  2009/05/01 19:07:02  mjk
# chimi con queso
#
# Revision 1.11  2009/03/21 22:22:55  bruno
#  - lights-out install of VM frontends with new node_rolls table
#  - nuked 'site' columns and tables from database
#  - worked through some bugs regarding entities
#
# Revision 1.10  2009/03/06 21:21:13  bruno
# updated for host attributes
#
# Revision 1.9  2009/03/04 21:31:44  bruno
# convert all getGlobalVar to getHostAttr
#
# Revision 1.8  2009/03/04 20:15:31  bruno
# moved 'dbreport hosts' and 'dbreport resolv' into the command line
#
# Revision 1.7  2009/02/11 19:26:01  bruno
# put quotes around the group id. thanks to Kaizaad Bilimorya for the fix.
#
# Revision 1.6  2008/10/18 00:55:56  mjk
# copyright 5.1
#
# Revision 1.5  2008/09/11 18:45:15  bruno
# put nodes that have an IP address assigned to their physical interface
# into /etc/dhcpd.conf
#
# Revision 1.4  2008/09/04 20:57:14  bruno
# ignore hosts that don't have IP addresses (like hosted VMs).
#
# Revision 1.3  2008/08/28 18:12:45  anoop
# Now solaris installations use pxelinux to chainload pxegrub. This
# way we can keep generation of pxelinux files controlled through
# "rocks add host pxeaction" and thus keep the content of
# pxelinux files consistent and managed.
#
# Revision 1.2  2008/07/23 00:29:54  anoop
# Modified the database to support per-node OS field. This will help
# determine the kind of provisioning for each node
#
# Modification to insert-ethers, rocks command line, and pylib to
# support the same.
#
# Revision 1.1  2008/05/22 21:02:06  bruno
# rocks-dist is dead!
#
# moved default location of distro from /export/home/install to
# /export/rocks/install
#
#
#

import os
import os.path
import sys
import rocks
import string
import rocks.commands
import rocks.ip

class Command(rocks.commands.HostArgumentProcessor,
	rocks.commands.report.command):
	"""
	Output the DHCP server configuration file for a specific host.

	<arg optional='0' type='string' name='host' repeat='0'>
	Create a DHCP server configuration for the machine named 'host'. If
	no host name is supplied, then generate a DHCP configuration file
	for this host.
	</arg>

	<example cmd='report host dhcpd frontend-0-0'>
	Output the DHCP server configuration file for frontend-0-0.
	</example>
	"""

	def makeAttrDictionary(self):
		# Read all the attributes global, os, app, host
		self.db.execute("""
			SELECT n.id, n.name, g.attr, g.value, 100 
			FROM nodes n JOIN global_attributes g  WHERE 
			g.attr="kickstartable" OR g.attr="dhcp_nextserver" 
			OR g.attr="dhcp_filename"
			UNION
			SELECT n.id, n.name, a.attr, a.value, 300 from nodes n,
			memberships m JOIN appliances app 
			ON m.appliance=app.id, appliance_attributes a 
			WHERE n.membership=m.id  AND a.appliance=app.id
			AND a.attr="kickstartable" OR a.attr="dhcp_nextserver"
		 	OR a.attr="dhcp_filename"
			UNION
			SELECT n.id, n.name, o.attr, o.value, 200 from nodes n,
			memberships m JOIN appliances app 
			ON m.appliance=app.id, os_attributes o 
			WHERE n.membership=m.id  AND (app.OS=o.OS)
			AND o.attr="kickstartable" OR o.attr="dhcp_nextserver" 
			OR o.attr="dhcp_filename"
			UNION
			SELECT n.id, n.name, na.attr, na.value, 400 
			from nodes n JOIN node_attributes na ON na.node=n.id
			AND na.attr="kickstartable" OR na.attr="dhcp_nextserver"
			OR na.attr="dhcp_filename"
			ORDER by 1,3,5; """)

		self.attrdict = {}
		for row in self.db.fetchall():
			key="%d-%s" %(row[0],row[2])
			self.attrdict[key]=row[3]
			
			
	def printOptions(self, prefix, network_dict):
		self.addOutput('', '%soption routers %s;' %
			(prefix, network_dict['gateway']))

		self.addOutput('', '%soption subnet-mask %s;' %
			(prefix, network_dict['netmask']))

		self.addOutput('', '%soption domain-name "%s";' %
			(prefix, network_dict['domain-name']))

		self.addOutput('', '%soption domain-name-servers %s;' %
			(prefix, network_dict['dns_server']))

		self.addOutput('', '%soption broadcast-address %s;' %
			(prefix, network_dict['broadcast-address']))
		try:
			self.db.execute("""SELECT mtu FROM subnets WHERE 
				subnets.name='%s'"""%(network_dict['name']))

			mtu, = self.db.fetchone()
			self.addOutput('', '%soption %s %s;' %
				(prefix, 'interface-mtu', mtu)) 
			
		except:
			pass

	def printHost(self, name, hostname, mac, ip, filename, nextserver):
		self.addOutput('', '\t\thost %s {' % name)
		if mac:
			self.addOutput('', '\t\t\thardware ethernet %s;' % mac)

		self.addOutput('', '\t\t\toption host-name "%s";' % hostname)
		self.addOutput('', '\t\t\tfixed-address %s;' % ip)

		if filename:
			self.addOutput('','\t\t\tfilename "%s";' % filename)
		if nextserver:
			self.addOutput('','\t\t\tnext-server %s;' % nextserver)
		self.addOutput('', '\t\t}')

		return
		

	def writeDhcpDotConf(self, hosts, all_networks):
		# Handle Path Name Fun
		RocksVersion = self.db.getHostAttr('localhost', 'rocks_version')
		if int(RocksVersion.split('.')[0]) < 6:
			self.addOutput('', '<file name="/etc/dhcpd.conf">')
		else:
			self.addOutput('', '<file name="/etc/dhcp/dhcpd.conf">')

		self.addOutput('', 'ddns-update-style none;')

		for network_dict in all_networks:
			network_name = network_dict['name']
			self.db.execute("""
			select dnszone,subnet,netmask from subnets where subnets.name="%s";
			""" % (network_name))
			network_info = self.db.fetchall();
			if(len(network_info) != 1):
				sys.stderr.write("Ignoring network %s as it's info is not found in the DB\n"%network_name)
				continue;
			dn = network_info[0][0]
			network = network_info[0][1]
			netmask = network_info[0][2]
			#Add to dictionary
			network_dict['domain-name'] = dn;
			network_dict['network'] = network;
			network_dict['netmask'] = netmask;

			self.addOutput('', 'subnet %s netmask %s {'
				% (network, netmask))

			default_lease = self.db.getHostAttr('localhost',
				'Kickstart_DefaultLeaseTime')
			max_lease = self.db.getHostAttr('localhost',
				'Kickstart_MaxLeaseTime')

			if not default_lease:
				default_lease = '1200'
			if not max_lease:
				max_lease = '1200'

			self.addOutput('', '\tdefault-lease-time %s;' % default_lease)
			self.addOutput('', '\tmax-lease-time %s;' % max_lease)

			self.printOptions('\t', network_dict)

			self.addOutput('', '\tgroup "%s" {' % dn)
			ip  = rocks.ip.IPGenerator(network, netmask)
			
			curnode = 0
			self.makeAttrDictionary()
			self.db.execute("""
				SELECT n.id,n.name,n.rack,n.rank,net.device,net.mac,
				net.ip,sub.name FROM nodes n INNER JOIN networks net 
				ON net.node=n.id, subnets sub WHERE net.subnet=sub.id
				AND (net.vlanid IS NULL OR net.vlanid=0) 
				AND sub.name="%s" 
				UNION
				SELECT n.id,n.name,n.rack,n.rank,net.device,net.mac,
				net.ip, NULL FROM nodes n INNER JOIN networks net 
				ON net.node=n.id where net.subnet IS NULL
				AND (net.vlanid IS NULL or net.vlanid=0) 
				ORDER BY 1,7 DESC; """ %(network_dict['name']))

			for row in self.db.fetchall():
				node = rocks.util.Struct()
				node.id		= row[0]
				node.name	= row[1]
				node.rack	= row[2]
				netdevice	= row[4]
				node.rank	= row[3]
				node.mac	= row[5]
				node.ip		= row[6]
				netname		= row[7]
				hostname = node.name

				if curnode != node.id :
					curnode = node.id
					unassignedidx = 0
					kickstartable = self.attrdict.get('%d-kickstartable' % node.id)
					if kickstartable:
						kickstartable = self.str2bool(kickstartable)
					else:
						kickstartable = False

					if not kickstartable:
						nextserver = None
						filename = None

					if kickstartable:
						filename = self.attrdict.get('%d-dhcp_filename' % node.id)
						nextserver = self.attrdict.get('%d-dhcp_nextserver' %node.id)
				if netname == "private":
					privateIP = node.ip

				# if both netname and IP are empty then this is 
				# an unassigned MAC
				if netname is None and  node.ip is None:
					node.ip = privateIP

				# Check that we have valid values
				if node.name is None or node.mac is None or node.ip is None or len(node.mac) > 20:
					continue

				# Try to add the netdevice name -- it won't exist
				# at first discovery
				try:
					node.name = node.name + '-' + netdevice
				except:
					pass
				self.printHost(node.name, hostname, node.mac, node.ip, filename, nextserver)

			self.addOutput('', '\t}')
			self.addOutput('', '}')

		self.addOutput('', '</file>')
		return


	def writeDhcpSysconfig(self, all_networks):
		networks = []
		for network_dict in all_networks:
			networks.append(network_dict['name'])
		dhcp_device_list=[]
		self.addOutput('', '<file name="/etc/sysconfig/dhcpd">')

		fe_name = self.db.getHostname('localhost')

		for network_name in networks:
			rows = self.db.execute("""select device from networks,subnets
				where networks.node = (select id from nodes where
				name = '%s') and
				subnets.name = "%s" and
				networks.subnet = subnets.id and
				networks.ip is not NULL and
				(networks.vlanid is NULL or
				networks.vlanid = 0)""" % (fe_name, network_name))

			if rows == 1:
				device, = self.db.fetchone()
			else:
				device = 'eth0'
			dhcp_device_list.append(device);

		self.addOutput('', 'DHCPDARGS="%s"' % (' '.join(dhcp_device_list)))

		self.addOutput('', '</file>')
		
		return


	def run(self, params, args):
		if len(args) > 1:
			self.abort('cannot supply more than one host name')
		if len(args) == 0:
			args = [ os.uname()[1] ]

		hosts = self.getHostnames(args)

		self.beginOutput()
		#list of dicts
		all_networks = [
				{
					'name': 'private',
					'gateway':self.db.getHostAttr('localhost', 'Kickstart_PrivateGateway'),
					'dns_server':self.db.getHostAttr('localhost', 'Kickstart_PrivateDNSServers'),
					'broadcast-address':self.db.getHostAttr('localhost', 'Kickstart_PrivateBroadcast')
					},
				#{ 'name': 'rmm', 'gateway':'192.168.2.1', 'dns_server':'192.168.2.2', 'broadcast-address':'192.168.2.255'},
				]
		self.writeDhcpDotConf(hosts, all_networks)
		self.writeDhcpSysconfig(all_networks)
		self.endOutput(padChar='')

RollName = "base"
