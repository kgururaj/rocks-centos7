# $Id: __init__.py,v 1.14 2012/11/27 00:48:29 phil Exp $
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
# Set gateway_ip for network

import rocks.commands


class Command(rocks.commands.NetworkArgumentProcessor,
	rocks.commands.set.command):
	"""
	Sets the gateway_ip for one or more named networks .

	<arg type='string' name='network' repeat='1'> 
	One or more named networks that should have the defined netmask.
	</arg>
	
	<arg type='string' name='gateway_ip'>
	Gateway for IP
	</arg>
	
	<param type='string' name='gateway_ip'>
	Can be used in place of gateway_ip argument.
	</param>

	<example cmd='set network gateway_ip optiputer 192.168.1.1'>
	Sets the gateway_ip for the "optiputer" network to 192.168.1.1
	</example>

	<example cmd='set network gateway_ip optiputer 192.168.1.1'>
	Same as above.
	</example>

	<related>add network</related>
	<related>set network subnet</related>
	"""

        def run(self, params, args):
        	(args, gateway_ip) = self.fillPositionalArgs(('gateway_ip',))
        	
        	if not len(args):
        		self.abort('must supply network')
		if not gateway_ip:
			self.abort('must supply gateway_ip')
			      
		if (len(self.getNetworkNames(args)) != 1):
			self.abort('cannot handle multiple networks in the same command')

        	for network in self.getNetworkNames(args):
			self.db.execute("""update subnets set gateway_ip='%s' where
				subnets.name='%s'""" % (gateway_ip, network))


RollName = "base"
