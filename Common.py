import subprocess, sys, re


import random

def rand():
    return str(random.randint(1,1000))

def exec_command(command):
    try:
        #os.system('clear')
        print_in_color('\n' + command+ '\n', 'blue')
        result = subprocess.check_output(command, stdin=True, stderr=subprocess.STDOUT, shell=True,encoding='UTF-8')
        clear_result = ''
        for line in result.splitlines():
            if line.startswith('/') or line.startswith(' '):
                pass
            else:
                clear_result+=line+'\n'
        print_in_color(clear_result, 'green')
        cont=to_continue()
        if cont=='y':
            pass
        else:
            sys.exit(1)
        return {'ReturnCode': 0, 'CommandOutput': result}
    except subprocess.CalledProcessError as e:
        print_in_color(e, 'red')
        cont=to_continue()
        if cont=='y':
            pass
        else:
            sys.exit(1)
        return {'ReturnCode': e.returncode, 'CommandOutput': e.output}


def exec_command_silence(command, print_com = True):
    if print_com:
        print_in_color(command, 'blue')
    try:
        result = subprocess.check_output(command, stdin=True, stderr=subprocess.STDOUT, shell=True,encoding='UTF-8')
        return {'ReturnCode': 0, 'CommandOutput': result}
    except:
        pass


def print_in_color(string,color_or_format=None):
    string=str(string)
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
    elif color_or_format =='red':
        print(bcolors.FAIL + string + bcolors.ENDC)
    elif color_or_format =='yellow':
        print(bcolors.WARNING + string + bcolors.ENDC)
    elif color_or_format =='blue':
        print(bcolors.OKBLUE + string + bcolors.ENDC)
    elif color_or_format =='bold':
        print(bcolors.BOLD + string + bcolors.ENDC)
    else:
        print(string)


def to_continue(msg='To continue y/n? '):
    result = None
    while result not in ['y', 'n']:
        result = input(msg)
    return result


def get_ips_from_file(fil='/etc/bind/named.conf.options'):
    with open(fil) as fh:
        fstring = fh.readlines()
    ip_list=[]
    for line in fstring:
        ipPattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        findIP = re.findall(ipPattern, line)
        if len(findIP)>0:
            for ip in findIP:
                if ip not in ip_list:
                    ip_list.append(ip)
    return ip_list
