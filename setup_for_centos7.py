#!/usr/bin/env python

import sys
import os
import subprocess
import shutil
import fix_rocks_network
import json

pxelinux_kernels_dir='/tftpboot/pxelinux/';
centos7_templates_dir='./centos7_ks'
centos7_dir='/export/rocks/install/centos7/';
centos7_ks_scripts_dir=centos7_dir+'/scripts/';
centos7_pxeboot_dir=centos7_dir+'/images/pxeboot';

#Fix PXE boot bug
def fix_pxe_bug():
    shutil.copy('/usr/share/syslinux/chain.c32', pxelinux_kernels_dir);
    subprocess.call('rocks add bootaction action=os kernel="com32 chain.c32" args="hd0"', shell=True);

def fix_install_action():
    shutil.copy(centos7_pxeboot_dir+'/vmlinuz', pxelinux_kernels_dir+'/vmlinuz-centos7');
    shutil.copy(centos7_pxeboot_dir+'/initrd.img', pxelinux_kernels_dir+'/initrd.img-centos7');
    ks_host = fix_rocks_network.get_rocks_attr('Kickstart_PrivateKickstartHost');
    ks_base_dir = fix_rocks_network.get_rocks_attr('Kickstart_PrivateKickstartBasedir');
    subprocess.call('rocks add bootaction action=install kernel=vmlinuz-centos7 ramdisk=initrd.img-centos7 args="ksdevice=bootif ramdisk_size=16000 ks=http://'+ks_host+'/'+ks_base_dir+'/centos7/ks.cfg rhgb quiet console=tty0 console=ttyS0,115200n8"', shell=True);

def setup_for_centos7(params): 
  if(not os.path.isdir(centos7_dir)):
    sys.stderr.write('ERROR: the contents of a CentOS-7 iso must be unpacked in the directory: '+centos7_dir+'\n');
    raise Exception('Missing directory containing CentOS-7 iso contents');
  try:
    os.mkdir(centos7_ks_scripts_dir, 0755);
  except OSError:
    pass
  #PXE boot changes
  fix_pxe_bug();
  fix_install_action();
  #ssh public key
  shutil.rmtree(centos7_ks_scripts_dir+'/ssh_public_keys', ignore_errors=True);
  try:
    os.remove(centos7_ks_scripts_dir+'/ssh_public_keys');
  except Exception:
    pass
  if('ssh_public_keys_file' in params):
    shutil.copy(params['ssh_public_keys_file'], centos7_ks_scripts_dir+'/ssh_public_keys');
  #Get root password
  root_passwd='$6$CdGXnN6zABQ0Pc/7$lsUtU27wSxwpGNrLQq00Mzpwb27ujgkV5Trq8wlZrqOmrmFuX6q5X0hebNKKs5DSk8.fU3o.b6Z0ISOfNnpTl.';
  sys.stderr.write('Enter the root password to be set for your cluster by kickstart\n');
  pid = subprocess.Popen('grub-crypt --sha-512', shell=True, stdout=subprocess.PIPE);
  stdout_str = pid.communicate()[0];
  if(pid.returncode == 0):
    root_passwd = stdout_str.strip();
  else:
    sys.stderr.write('ERROR: could not obtain root password, using a random string. Re-run the program to set your root passwd\n');
  #Copy disk.py file for partitioning
  shutil.copy(centos7_templates_dir+'/scripts/disk.py', centos7_ks_scripts_dir+'/disk.py');
  #Create files from templates
  shutil.copy(centos7_templates_dir+'/ks_template.cfg', centos7_dir+'/ks.cfg');
  shutil.copy(centos7_templates_dir+'/scripts/pre_install_template.sh', centos7_ks_scripts_dir+'/pre_install.sh');
  shutil.copy(centos7_templates_dir+'/scripts/post_install_template.sh', centos7_ks_scripts_dir+'/post_install.sh');
  ks_host = fix_rocks_network.get_rocks_attr('Kickstart_PrivateKickstartHost');
  ks_base_dir = fix_rocks_network.get_rocks_attr('Kickstart_PrivateKickstartBasedir');
  cmd = 'sed -i -e \'s/Kickstart_PrivateKickstartHost/'+ks_host+'/g\' -e \'s/Kickstart_PrivateKickstartBasedir/'+ks_base_dir+'/g\' '+centos7_ks_scripts_dir+'/post_install.sh '+centos7_ks_scripts_dir+'/pre_install.sh '+centos7_dir+'/ks.cfg';
  status = subprocess.call(cmd, shell=True);
  if(status != 0):
    sys.stderr.write('ERROR: could not setup pre/post install scripts and kickstart file\n');
    raise Exception('Could not setup pre/post install scripts and kickstart file');
  if('timezone' in params):
    cmd = 'sed -i -e \'/^timezone/c\\\ntimezone '+params['timezone']+'\' '+centos7_dir+'/ks.cfg' 
    status = subprocess.call(cmd, shell=True);
    if(status != 0):
      sys.stderr.write('ERROR: could not setup timezone in kickstart file\n');
      raise Exception('Could not setup timezone in kickstart file');
  with open(centos7_dir+'/ks.cfg', 'ab') as fptr:
    fptr.write('rootpw --iscrypted '+root_passwd+' \n');
    fptr.close();

if __name__ == "__main__":
  params = {};
  if(len(sys.argv) >= 2):
    with open(sys.argv[1], 'rb') as data_file:    
      params = json.load(data_file);
  directory = os.path.dirname(sys.argv[0]);
  if(directory and directory != ''):
    os.chdir(directory);
  setup_for_centos7(params);

