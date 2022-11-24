from dataclasses import dataclass
from Common import *

print_in_color('You must be sourced with *.rc file, for example overcloudrc', 'green')

@dataclass
class TestScale:
    """Class for keeping track of an item in inventory."""
    source_file: str = 'overcloudrc'
    number_of_zones: int = 1000
    number_of_recordsets: int = 100

    @staticmethod
    def exec_command(command):
        try:
            print_in_color('\n' + command + '\n', 'blue')
            result = subprocess.check_output(command, stdin=True, stderr=subprocess.STDOUT, shell=True,
                                             encoding='UTF-8')
            clear_result = ''
            for line in result.splitlines():
                if line.startswith('/') or line.startswith(' '):
                    pass
                else:
                    clear_result += line + '\n'
            print_in_color(clear_result, 'green')
            cont = to_continue()
            if cont == 'y':
                pass
            else:
                sys.exit(1)
            return (0, result)
        except subprocess.CalledProcessError as e:
            print_in_color(e, 'red')
            cont = to_continue()
            if cont == 'y':
                pass
            else:
                sys.exit(1)
            return (e.returncode, e.output)


    def create_zone(self, zone_name, zone_email):
        command = 'openstack zone create --email {} {}'.format(zone_email, zone_name)
        return_code, returned_output = self.exec_command(command)
        if return_code != 0:
            print_in_color('Failed to execute: "{}"'.format(command), 'red')
            print_in_color(returned_output, 'red')
            sys(exit(1))



