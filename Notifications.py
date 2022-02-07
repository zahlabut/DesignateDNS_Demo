# Usage
# 1) Run all Designate Tempest tests
# 2) Run this script as root only


import subprocess


def exec_command(command):
    try:
        print_in_color('--> ' + command, 'bold')
        result = subprocess.check_output(command, stdin=True, stderr=subprocess.STDOUT, shell=True, encoding='UTF-8')
        return {'ReturnCode': 0, 'CommandOutput': result}
    except subprocess.CalledProcessError as e:
        return {'ReturnCode': e.returncode, 'CommandOutput': e.output}


def print_in_color(string, color_or_format=None):
    string = str(string)

    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    if color_or_format == 'green':
        print(bcolors.OKGREEN + string + bcolors.ENDC)
    elif color_or_format == 'red':
        print(bcolors.FAIL + string + bcolors.ENDC)
    elif color_or_format == 'yellow':
        print(bcolors.WARNING + string + bcolors.ENDC)
    elif color_or_format == 'blue':
        print(bcolors.OKBLUE + string + bcolors.ENDC)
    elif color_or_format == 'bold':
        print(bcolors.BOLD + string + bcolors.ENDC)
    else:
        print(string)


rabitmq_commands = [
    'rabbitmq-plugins enable rabbitmq_management',
    'rabbitmqctl list_vhosts',
    'rabbitmqctl list_queues -q -p /',
    'rabbitmqctl add_user test-admin test-admin',
    'rabbitmqctl set_user_tags test-admin administrator',
    'rabbitmqctl set_permissions -p / test-admin ".*" ".*" ".*"',
    'rabbitmqctl change_password test-admin testpass']

expected_notifications = [
    'dns.tld.create', 'dns.tld.update', 'dns.tld.delete',
    'dns.tsigkey.create', 'dns.tsigkey.update', 'dns.tsigkey.delete',
    'dns.domain.create', 'dns.zone.create', 'dns.domain.update',
    'dns.zone.update', 'dns.domain.delete', 'ns.zone.delete',
    'dns.zone.touch', 'dns.recordset.create', 'dns.recordset.update',
    'dns.recordset.delete', 'dns.record.create', 'dns.record.update',
    'dns.record.delete', 'dns.blacklist.create', 'dns.blacklist.update',
    'dns.blacklist.delete', 'dns.pool.create', 'dns.pool.update',
    'dns.pool.delete', 'dns.domain.update', 'dns.zone.update',
    'dns.zone_transfer_request.create', 'dns.zone_transfer_request.update',
    'dns.zone_transfer_request.delete', 'dns.zone_transfer_accept.create',
    'dns.zone_transfer_accept.update', 'dns.zone_transfer_accept.delete',
    'dns.zone_import.create', 'dns.zone_import.update', 'dns.zone_import.delete',
    'dns.zone_export.create', 'dns.zone_export.update', 'dns.zone_export.delete']

read_msges = 'rabbitmqadmin get -V / -u test-admin -p testpass queue=notifications.info count=10000000'

for com in rabitmq_commands:
    command_out = exec_command(com)
    if command_out == 0:
        print_in_color(command_out['CommandOutput'], 'green')
    else:
        print_in_color(str(command_out['ReturnCode']) + ' -- ' + command_out['CommandOutput'], 'red')

messages = exec_command(read_msges)['CommandOutput'].lower()

for string in expected_notifications:
    if string not in messages:
        print_in_color('Error - notification message:{} was not detected:'.format(string), 'red')