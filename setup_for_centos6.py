#!/usr/bin/env python

import sys
import os
import subprocess
import shutil
import fix_rocks_network
import setup_for_centos7
import json

pxelinux_kernels_dir='/tftpboot/pxelinux/';
centos6_templates_dir='./centos6_ks'
centos6_dir='/export/rocks/install/centos6/';
centos6_ks_scripts_dir=centos6_dir;
rocks_customize_nodes_dir='/export/rocks/install/site-profiles/6.1.1/nodes/'

def setup_for_centos6(params): 
  shutil.rmtree(centos6_dir, ignore_errors=True);
  try:
    os.remove(centos6_dir);
  except Exception:
    pass
  os.makedirs(centos6_ks_scripts_dir, 0755);
  #PXE boot changes
  setup_for_centos7.fix_pxe_bug();
  #ssh public key
  shutil.rmtree(centos6_ks_scripts_dir+'/ssh_public_keys', ignore_errors=True);
  try:
    os.remove(centos6_ks_scripts_dir+'/ssh_public_keys');
  except Exception:
    pass
  if('ssh_public_keys_file' in params):
    shutil.copy(params['ssh_public_keys_file'], centos6_ks_scripts_dir+'/ssh_public_keys');
  #Copy extend-compute.xml
  shutil.copy(centos6_templates_dir+'/extend-compute.xml', rocks_customize_nodes_dir+'/extend-compute.xml');
  #Copy other files in the directory
  status = subprocess.call('rsync -a --exclude=extend-compute.xml '+centos6_templates_dir+'/ '+centos6_ks_scripts_dir+'/', shell=True);
  if(status != 0):
    sys.stderr.write('ERROR: could not copy pre/post install scripts\n');
    raise Exception('Could not copy pre/post install scripts');
  #Get root password
  root_passwd='$6$CdGXnN6zABQ0Pc/7$lsUtU27wSxwpGNrLQq00Mzpwb27ujgkV5Trq8wlZrqOmrmFuX6q5X0hebNKKs5DSk8.fU3o.b6Z0ISOfNnpTl.';
  sys.stderr.write('Enter the root password to be set for your cluster by kickstart\n');
  pid = subprocess.Popen('grub-crypt --sha-512', shell=True, stdout=subprocess.PIPE);
  stdout_str = pid.communicate()[0];
  if(pid.returncode == 0):
    root_passwd = stdout_str.strip();
  else:
    sys.stderr.write('ERROR: could not obtain root password, using a random string. Re-run the program to set your root passwd\n');
    raise Exception('Could not obtain root password - exiting');
  cmd = 'sed -i -e \'/rootpw/c\\\n    <rootpw>--iscrypted '+root_passwd+'</rootpw>\' '+rocks_customize_nodes_dir+'/extend-compute.xml';
  status = subprocess.call(cmd, shell=True);
  if(status != 0):
    sys.stderr.write('ERROR: could not obtain root password, using a random string. Re-run the program to set your root passwd\n');
    raise Exception('Could not obtain root password - exiting');
  if('timezone' in params):
    cmd = 'sed -i -e \'/timezone/c\\\n    <timezone>'+params['timezone']+'</timezone>\' '+rocks_customize_nodes_dir+'/extend-compute.xml';
    status = subprocess.call(cmd, shell=True);
    if(status != 0):
      sys.stderr.write('ERROR: could not setup timezone in kickstart file\n');
      raise Exception('Could not setup timezone in kickstart file');
  if('proxy_host' in params and 'proxy_port' in params):
    cmd = 'sed -i -e \'/post_install/c\\\n    bash -x ./centos6/post_install.sh '+params['proxy_host']+' '+params['proxy_port']+'\' '+rocks_customize_nodes_dir+'/extend-compute.xml';
    status = subprocess.call(cmd, shell=True);
    if(status != 0):
      sys.stderr.write('ERROR: could not setup proxy args for post-install\n');
      raise Exception('Could not setup proxy args for post-install');
  status = subprocess.call('cd /export/rocks/install && rocks create distro', shell=True);
  if(status != 0):
    sys.stderr.write('ERROR: could not build rocks distro\n');
    raise Exception('Could not build rocks distro');


if __name__ == "__main__":
  params = {};
  if(len(sys.argv) >= 2):
    with open(sys.argv[1], 'rb') as data_file:    
      params = json.load(data_file);
  directory = os.path.dirname(sys.argv[0]);
  if(directory and directory != ''):
    os.chdir(directory);
  setup_for_centos6(params);

