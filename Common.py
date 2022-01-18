import subprocess, sys, time, re, os, art


import random

def rand():
    return str(random.randint(1,1000))

def exec_command(command):
    try:
        os.system('clear')
        print_in_color('\n' + command+ '\n', 'blue')
        result = subprocess.check_output(command, stdin=True, stderr=subprocess.STDOUT, shell=True,encoding='UTF-8')
        print_in_color(result, 'green')

        cont=choose_option_from_list(['yes','no'], 'To continue?')[1]
        if cont=='yes':
            pass
        else:
            sys.exit(1)
        return {'ReturnCode': 0, 'CommandOutput': result}
    except subprocess.CalledProcessError as e:
        print_in_color(e, 'red')
        cont=choose_option_from_list(['yes','no'], 'To continue?')[1]
        if cont=='yes':
            pass
        else:
            sys.exit(1)
        return {'ReturnCode': e.returncode, 'CommandOutput': e.output}


def exec_command_silence(command):
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

def choose_option_from_list(list_object, msg):
    print('')
    try:
        if (len(list_object)==0):
            print("Nothing to choose :( ")
            print("Execution will stop!")
            time.sleep(5)
            exit("Connot continue execution!!!")
            sys.exit(1)
        print(msg)
        counter=1
        for item in list_object:
            print(str(counter)+') - '+item)
            counter=counter+1
        choosed_option=input("Choose your option:")
        if choosed_option=='Demo':
            return [True, 'Demo']
        while (int(choosed_option)<0 or int(choosed_option)> len(list_object)):
            print("No such option - ", choosed_option)
            choosed_option=input("Choose your option:")
        print_in_color("Option is: '"+list_object[int(choosed_option)-1]+"'"+'\n','bold')
        return [True,list_object[int(choosed_option)-1]]
    except Exception as e:
        print('*** No such option!!!***', e)
        return[False, str(e)]


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


