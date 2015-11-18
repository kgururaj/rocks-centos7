import sys
import os
sys.path = [ '/export/rocks/install/rocks-dist/x86_64/build/include/installclass' ] + sys.path;
import re
import subprocess
import shlex
#import argparse

membership = '&membership;'
nodename = '&hostname;'

def find_disk_size(disk_size_str):
    match = re.match(r"([0-9\.]+)([a-z]+)", disk_size_str, re.I)
    if match:
        items = match.groups();
        if(len(items) == 2):
            size_units = { 'KB':1024, 'MB':1024*1024, 'GB':1024*1024*1024, 'TB':1024*1024*1024*1024, 'PB':1024*1024*1024*1024*1024 };
            if(items[1] in size_units):
                disk_size = float(items[0])*size_units[items[1]];
                return disk_size;
    return None;

def find_disk_id(line):
    tokens = line.split();
    if(len(tokens) >= 3 and tokens[0] == 'Disk'):
        disk = tokens[1];
        disk = disk.replace(':','');
        return disk;
    return None;

def find_os_disk(disks):
    disk_list = [ ];
    for disk in disks:
        disk_id = disk[0];
        disk_size = find_disk_size(disk[1]);
        if(disk_size and disk_id):
            disk_list.append((disk_id, disk_size));
        else:
            return None;        #could not determine size for one of the disks - play safe and return None
    if(len(disk_list) > 0):
        disk_list.sort(key=lambda x:x[1]);
        fptr = open('/tmp/disk_list.csv','wb');
        first_disk = True;
        for disk_id,disk_size in disk_list:
            fptr.write(disk_id+',%.2f'%(disk_size));
            if(first_disk):
                fptr.write(',OS_disk');
            fptr.write('\n');
            first_disk = False;
        fptr.close();
        return (disk_list[0][0], disk_list[0][1]);         #smallest disk
    return None;
                
def doDisk(file, disk, disk_size, force_format=False, root_partition_size=None):
    if(force_format):
        parted_cmd = '/sbin/parted -s '+disk+' mklabel msdos';
        print(parted_cmd);
        process = subprocess.Popen(shlex.split(parted_cmd), stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT);
        stdout_str = process.communicate()[0];
        print(stdout_str);
    disk = os.path.basename(disk);
    file.write('zerombr\n')
    file.write('clearpart --drives=%s\n' % disk)
    disk_size = int(float(disk_size)/(1024*1024*1024));   #GB
    max_swap = 64;     #64 GB
    recommended_root_size = 150; #150 GB
    if(root_partition_size):
        root_partition_size = min(disk_size, root_partition_size);
        swap_size = min(max_swap, disk_size-root_partition_size);
    else:
        if(disk_size <= recommended_root_size): #<=recommended, no swap
            root_partition_size = disk_size;
            swap_size = 0;
        else:
            swap_size = min(max_swap, disk_size-recommended_root_size);
            root_partition_size = disk_size-swap_size;
    if(swap_size > 0):
        file.write(('part swap --fstype="swap" --size=%d --ondisk=%s\n') % (swap_size*1024, disk))  #MB - as per kickstart
    if(root_partition_size < (disk_size - swap_size)):
        file.write('part / --fstype="ext4" --size=%d --ondisk=%s\n' % (root_partition_size*1024, disk))
    else:
        file.write('part / --fstype="ext4" --size=1 --grow --ondisk=%s\n'    % disk)
    file.write('bootloader --location=mbr\n');

#                            
# main
#

#p = rocks_partition.RocksPartition();
#disks = p.getDisks();

def get_parted_disk_list():
    process = subprocess.Popen(shlex.split('/sbin/parted -l -m'), stdout=subprocess.PIPE);
    stdout_str = process.communicate()[0];
    list = stdout_str.split('\n');
    #First initialize uninitialized disks - create msdos if needed
    for line in list:
        if(line.find('Error') != -1 and line.find('unrecognised disk label') != -1): 
            new_line = line.strip();
            tokens = new_line.split();
            if(len(tokens) > 2):
                disk =  tokens[1].replace(':','');
                subprocess.call(shlex.split('/sbin/parted -s '+disk+' mktable msdos'));
    #Now create list of disks
    process = subprocess.Popen(shlex.split('/sbin/parted -l -m'), stdout=subprocess.PIPE);
    stdout_str = process.communicate()[0];
    list = stdout_str.split('\n');
    disk_list=[];
    next_is_disk = False;
    for line in list:
        if(next_is_disk):
            new_line = line.strip();
	    if(new_line.find('loop') == -1):	#not a loop-back device
	      new_line = new_line.replace(';','');
	      disk_list.append(new_line.split(':'));
            next_is_disk = False;
        if(line.find('BYT') != -1):
            next_is_disk = True;
    return disk_list;


def main(argv):
    arg_needs_value  = { '--root_partition_size':True, '--force_format':False, '--manual':False };
    param_values = { 'manual':False, 'force_format':False, 'root_partition_size':None } ;  #GB
    node_type = None;
    i = 0;
    for i in range(len(argv)):
        arg = argv[i];
        if(arg in arg_needs_value):
            cut_arg = arg.replace('--','');
            if(arg_needs_value[arg]):
                param_values[cut_arg] = argv[i+1];
                i += 1;
            else:
                param_values[cut_arg] = True;
        else:
            if(node_type):
                sys.stderr.write('Node type already assigned to '+node_type+', only 1 positional argument expected\n');
                sys.exit(-1);
            node_type = arg;
        i += 1;
    if(param_values['root_partition_size']):
        param_values['root_partition_size']  = int(param_values['root_partition_size']);
    if(not node_type):
        param_values['manual'] = True;
    #parser.add_argument("node_type", help='Type of node - Lustre server (OSS/MDS/MGS), compute etc');
    #parser.add_argument("--root_partition_size", help="Root partition size in GB(integer)", default=100, type=int); #GB
    #group = parser.add_mutually_exclusive_group()
    #group.add_argument("--force_format", help='Force format of whole OS disk', action="store_true");
    #group.add_argument("--manual", help='Manual format', action="store_true");
    #args = parser.parse_args();
    file = open('/tmp/user_partition_info', 'wb')
    #Manual format if manual_format or (Lustre servers and not force_format)
    if param_values['manual'] or (node_type == 'lustre_server' and not param_values['force_format']):
        file.write('rocks manual\n');
        file.close();
        sys.exit(0);
    disks = get_parted_disk_list();
    os_disk_tuple = find_os_disk(disks);
    if(os_disk_tuple):    
        doDisk(file, os_disk_tuple[0], os_disk_tuple[1], force_format=param_values['force_format'],
                root_partition_size=param_values['root_partition_size']);
    else:    #could not find a suitable disk, use manual 
        file.write("rocks manual\n");
    file.close()

if __name__ == "__main__":
    main(sys.argv[1:] if len(sys.argv) > 1 else []);

