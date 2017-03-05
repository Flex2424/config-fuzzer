import subprocess
from sys import argv, exit
import binascii


class ConfigFuzzer:
    def __init__(self, configfile, binaryfile):
        self.config_name = configfile
        self.file_name = binaryfile

    def execute_program(self):
        proc = subprocess.Popen([self.file_name], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        return out, err

    def fuzzing(self):
        pass



if len(argv) == 3:
    config = argv[1]
    file = argv[2]
    obj = ConfigFuzzer(config, file)
    obj.fuzzing()
else:
    print("Usage: ./script.py config file")
    exit(-1)
