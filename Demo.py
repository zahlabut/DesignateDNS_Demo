# Usage
# You need to be sourced (admintrc, openrc ...) to run this script

import time
from Common import *
from art import *

sleep_time=3
random_string = rand()

sec_gr_commands = [
"openstack security group list --project=admin",
"openstack security group rule create $(openstack security group list --project=admin | grep default | awk '{print $2}') --protocol icmp --ingress",
"openstack security group rule create $(openstack security group list --project=admin | grep default | awk '{print $2}') --protocol icmp --egress",
]

net_commands=[
    'openstack network create net{} -c name'.format(random_string),
    'openstack subnet create subnet{} --network net{} --subnet-range 192.0.2.0/24 -c name'.format(random_string,random_string)]

zone_to_net_commands=[
    'openstack zone create example{}.com. --email example{}@example.com'.format(random_string, random_string),
    'openstack zone show example{}.com.'.format(random_string),
    'openstack network set --dns-domain example{}.com. net{}'.format(random_string, random_string),
    'openstack network show net{} -c dns_domain'.format(random_string)
]

create_router_commands = [
    'openstack router create router{} -c name'.format(random_string),
    'openstack router set --external-gateway public router{}'.format(random_string),
    'openstack router add subnet router{} subnet{}'.format(random_string,random_string)
]

create_vm_commands=[
    'openstack server create --flavor m1.micro --image cirros-0.5.1-x86_64-disk --nic net-id=net{} vm{}'.format(random_string,random_string),
    'sleep',
    'openstack server show vm{}'.format(random_string)
]

create_fip_for_vm_port_commands=[
    'openstack port list --server vm{}'.format(random_string),
    "openstack floating ip create public --port $(openstack port list --server vm{}".format(random_string)+" | grep ip_address | awk '{print $2}') -c name"
]

if to_continue('Are you sourced with *.rc file y/n?') == 'n':
    sys.exit(1)

cont = to_continue('To run the Security Grup create CLIs y/n? ')
if cont == 'y':
    for com in sec_gr_commands:
        exec_command_silence(com)

for com in net_commands:
    exec_command(com)

for com in zone_to_net_commands:
    exec_command(com)

for com in create_router_commands:
    exec_command(com)

for com in create_vm_commands:
    if com == 'sleep':
        time.sleep(sleep_time)
    else:
        exec_command(com)

for com in create_fip_for_vm_port_commands:
    exec_command(com)



### Configure local resolver with a NEW created zone ###
exec_command_silence('sudo mkdir -p /etc/systemd/resolved.conf.d', False)
local_resolver_ip = get_ips_from_file()[0]
zone_data_file='example{}.conf'.format(random_string)
zone_data='[Resolve]\n'
zone_data+='DNS={}\n'.format(local_resolver_ip)
zone_data+='Domains=~example{}.com'.format(random_string)
fil = open(zone_data_file,'w')
fil.write(zone_data)
fil.close()
exec_command_silence('sudo mv '+zone_data_file+' '+'/etc/systemd/resolved.conf.d/'+zone_data_file, False)
exec_command_silence('sudo cat /etc/systemd/resolved.conf.d/'+zone_data_file, False)
exec_command_silence('sudo systemctl restart systemd-resolved', False)

designate_demo_commands=[
    'openstack recordset list example{}.com.'.format(random_string),
    'dig @{} vm{}.example{}.com. A'.format(local_resolver_ip, random_string,random_string),
    'dig @{} vm{}.example{}.com. A +short'.format(local_resolver_ip, random_string,random_string),
    'ping -c 4 vm{}.example{}.com'.format(random_string, random_string),
    'openstack server delete vm{}'.format(random_string),
    'sleep',
    'dig @{} vm{}.example{}.com. A +short'.format(local_resolver_ip, random_string, random_string),
    'ping -c 1 -W 1 vm{}.example{}.com'.format(random_string, random_string)
]
for com in designate_demo_commands:
    if com == 'sleep':
        time.sleep(sleep_time)
    else:
        exec_command(com)

tprint("It's Over!!!")