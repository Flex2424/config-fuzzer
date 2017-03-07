import subprocess
from sys import argv, exit
import binascii
from colorama import *


class ConfigFuzzer:
    def __init__(self, configfile, binaryfile):
        self.config_name = configfile
        self.file_name = binaryfile
        self.config_data = None
        self.borders = []

    def execute_program(self):
        proc = subprocess.Popen([self.file_name], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        return out, err

    def fuzzing(self):
        pass

    def open_file(self):
        with open(self.config_name, 'rb') as f:
            content = f.read()
        result = binascii.hexlify(content)
        self.config_data = result.decode('ascii')

    def bytes_return(self, config_name='configs/config_2'):
        with open(config_name, 'rb') as f:
            content = f.read()
        result = binascii.hexlify(content)
        xs = result.decode('ascii')
        return xs

    def compare_two_config(self):
        xs1 = self.bytes_return()
        xs2 = self.config_data
        xs1 = ' '.join(xs1[i:i + 4] for i in range(0, len(xs1), 4))
        xs2 = ' '.join(xs2[i:i + 4] for i in range(0, len(xs2), 4))
        list1 = xs1.split(' ')
        list2 = xs2.split(' ')
        if len(list1) > len(list2):
            length = len(list2)
        else:
            length = len(list1)
        res = ""
        for i in range(0, length):
            if i % 8 == 0:
                res = res + '\n'
            if list1[i] == list2[i]:
                res = res + Fore.GREEN + list1[i] + ' '
            else:
                res = res + Fore.BLUE + list1[i] + ' '
        return res

    def find_borders(self):
        buf51 = self.bytes_return('configs/config_1')
        buf51 = ' '.join(buf51[i:i + 2] for i in range(0, len(buf51), 2))
        list51 = buf51.split(' ')
        list51 = list51[:49]

        buf52 = self.bytes_return('configs/config_2')
        buf52 = ' '.join(buf52[i:i + 2] for i in range(0, len(buf52), 2))
        list52 = buf52.split(' ')
        list52 = list52[:49]

        buf53 = self.bytes_return('configs/config_3')
        buf53 = ' '.join(buf53[i:i + 2] for i in range(0, len(buf53), 2))
        list53 = buf53.split(' ')
        list53 = list53[:49]

        buf54 = self.bytes_return('configs/config_4')
        buf54 = ' '.join(buf54[i:i + 2] for i in range(0, len(buf54), 2))
        list54 = buf54.split(' ')
        list54 = list54[:49]
        res = ''
        a = None
        isEnd = False
        for i in range(0, len(list51)):
            if list51[i] == list52[i] == list53[i] == list54[i] and isEnd:
                res += str(i) + '-'
                a = i
                isEnd = True - isEnd
            elif not list51[i] == list52[i] == list53[i] == list54[i] and not isEnd:
                res += str(i - 1) + '\n'
                isEnd = True - isEnd
                b = i - 1
                self.borders.append((a, b))
                a = 0
                b = 0
        # print(res[2:])
        # print borders
        print("BORDERS:")
        for i in self.borders:
            if i[0] == None or i[1] == None:
                self.borders.remove(i)
        for i in self.borders:
            print(i)


if len(argv) == 3:
    config = argv[1]
    file = argv[2]
    obj = ConfigFuzzer(config, file)
    obj.open_file()
    test = obj.compare_two_config()
    print("Differences in configs:", test)
    obj.find_borders()
else:
    print("Usage: ./script.py config file")
    exit(-1)
