from dataclasses import dataclass
from Common import *
import ipaddress, threading

print_in_color('You must be sourced with *.rc file, for example overcloudrc', 'green')
IPs = [str(ip) for ip in ipaddress.IPv4Network('192.0.0.0/12')]

# Parameters #
threads_number = 100  # Number of threads
zones = 100           # Number of zones to be created in each thread
recordsets = 10       # Number of recordsets to be created within a zone
start_index = 0       # Start index (For example if zero all the stuff
                      # will be started from example0.com)


@dataclass
class TestScale:
    number_of_zones: int
    number_of_recordsets: int
    start_index: int

    @staticmethod
    def exec_command(command, exit_on_error=False):
        try:
            print_in_color('\n' + command + '\n', 'blue')
            result = subprocess.check_output(
                command, stdin=True, stderr=subprocess.STDOUT, shell=True,
                encoding='UTF-8')
            clear_result = ''
            for line in result.splitlines():
                if line.startswith('/') or line.startswith(' '):
                    pass
                else:
                    clear_result += line + '\n'
            print_in_color(clear_result, 'green')
            return (0, result)
        except subprocess.CalledProcessError as e:
            if exit_on_error:
                print_in_color('Failed to execute: "{}"'.format(command), 'red')
                print_in_color(e, 'red')
                sys(exit(1))
            else:
                print_in_color(e, 'red')
                return (e.returncode, e.output)

    def create_zone(self, zone_name, zone_email):
        command = 'openstack zone create --email {} {}'.format(zone_email, zone_name)
        self.exec_command(command, exit_on_error=True)

    def create_A_recordset(self, zone_name, record_name, record_ip):
        command = 'openstack recordset create {} --type A {} --record {}'.format(zone_name, record_name, record_ip)
        self.exec_command(command, exit_on_error=True)

    def create_zones_with_recordsets(self):
        for zone in range(self.start_index, self.start_index+self.number_of_zones):
            zone_name, zone_email = 'example{}.com.'.format(zone), 'example{}@example{}.com'.format(zone, zone)
            self.create_zone(zone_name, zone_email)
            for record in range(self.start_index, self.start_index+self.number_of_recordsets):
                record_name = 'vm{}'.format(record)
                self.create_A_recordset(zone_name, record_name, IPs[record])


if __name__ == "__main__":
    # Increase quota
    zones = 100000
    zone_recordsets = 100000
    command = 'openstack dns quota set --zone-recordsets {} --zones {}'.format(zone_recordsets, zones)
    TestScale.exec_command(command)

    # # Start stuff creation in SERIAL
    # obj = TestScale(number_of_zones=10, number_of_recordsets=3, start_index=40)
    # obj.create_zones_with_recordsets()

    start_indexes = range(start_index, start_index + threads_number * threads_number, threads_number)
    threads=[]
    for index in start_indexes:
        threads.append(TestScale(number_of_zones=zones, number_of_recordsets=recordsets, start_index=index))
    for obj in threads:
        print(obj.number_of_zones, obj.number_of_recordsets, obj.start_index)
    for t in threads:
        thread = threading.Thread(target=t.create_zones_with_recordsets)
        thread.start()
        #thread.join()
