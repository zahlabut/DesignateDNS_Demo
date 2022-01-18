# Usage
# You need to be sourced (admintrc, openrc ...) to run this script

from Common import *

random_string = rand()

sec_gr_commands = [
"openstack security group list --project=admin",
"openstack security group rule create $(openstack security group list --project=admin | grep default | awk '{print $2}') --protocol icmp --ingress",
"openstack security group rule create $(openstack security group list --project=admin | grep default | awk '{print $2}') --protocol icmp --egress",
"openstack security group rule create $(openstack security group list --project=admin | grep default | awk '{print $2}') --protocol tcp --dst-port 22 --ingress",
"openstack security group rule create $(openstack security group list --project=admin | grep default | awk '{print $2}') --protocol tcp --dst-port 22 --egress",
"openstack security group rule create $(openstack security group list --project=admin | grep default | awk '{print $2}') --protocol tcp --dst-port 80 --ingress",
"openstack security group rule create $(openstack security group list --project=admin | grep default | awk '{print $2}') --protocol tcp --dst-port 80 --egress"]

net_commands=[
    'openstack network create net{}'.format(random_string),
    'openstack subnet create subnet{} --network net{} --subnet-range 192.0.2.0/24'.format(random_string,random_string)]

zone_to_net_commands=[
    'openstack zone create example{}.com. --email example1@example.com'.format(random_string),
    'openstack zone list --all',
    'openstack network list',
    'openstack network set --dns-domain example{}.com. net{}'.format(random_string, random_string),
    'openstack network show net{}'.format(random_string)
]

create_router_commands = [
    'openstack router create router{}'.format(random_string),
    'openstack router set --external-gateway public router{}'.format(random_string),
    'openstack router add subnet router{} subnet{}'.format(random_string,random_string),
    'openstack router show router{}'.format(random_string)
]

create_vm_commands=[
    'openstack flavor list',
    'openstack image list',
    'openstack server create --flavor m1.micro --image cirros-0.5.1-x86_64-disk --nic net-id=net{} vm{}'.format(random_string,random_string),
    'openstack server list'
]

create_fip_for_vm_port_commands=[
    'openstack port list --server vm{}'.format(random_string),
    "openstack floating ip create public --port $(openstack port list --server vm{}".format(random_string)+" | grep ip_address | awk '{print $2}')"
]


for com in sec_gr_commands:
    exec_command(com)

for com in net_commands:
    exec_command(com)

for com in zone_to_net_commands:
    exec_command(com)

for com in create_router_commands:
    exec_command(com)

for com in create_vm_commands:
    exec_command(com)

for com in create_fip_for_vm_port_commands:
    exec_command(com)



### Configure local resolver with a NEW created zone ###
exec_command('sudo mkdir -p /etc/systemd/resolved.conf.d')
local_resolver_ip = get_ips_from_file()[0]
zone_data_file='example{}.conf'.format(random_string)
zone_data='[Resolve]\n'
zone_data+='DNS={}\n'.format(local_resolver_ip)
zone_data+='Domains=~example{}.com'.format(random_string)
fil = open(zone_data_file,'w')
fil.write(zone_data)
fil.close()
exec_command('sudo mv '+zone_data_file+' '+'/etc/systemd/resolved.conf.d/'+zone_data_file)
exec_command('sudo systemctl restart systemd-resolved')

designate_demo_commands=[
    'openstack recordset list example{}.com.'.format(random_string),
    'dig @{} vm{}.example{}.com. A'.format(local_resolver_ip, random_string,random_string)
]

for com in designate_demo_commands:
    exec_command(com)




