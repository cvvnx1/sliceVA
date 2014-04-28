from time import sleep
from sliceva.models import Device
from paramiko import SSHClient, AutoAddPolicy

class alive:
    def run(self, hostname, username, password):
        method = Device.objects.filter(host=hostname)[0].loginmethod
        if method == "ssh":
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            try:
                ssh.connect(hostname=hostname, username=username, password=password, timeout=2)
                return True
            except:
                return False

class search_config:
    def __init__(self, commands):
        self.commands = commands

    def run(self, hostname, username, password):
        if self.commands.__len__() == 0: return False
        method = Device.objects.filter(host=hostname)[0].loginmethod
        if method == "ssh":
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            try:
                ssh.connect(hostname=hostname, username=username, password=password, timeout=2)
            except:
                return False
            for command in self.commands:
                stdin, stdout, stderr = ssh.exec_command('show running-config | include ' + command)
                if stdout.readlines().__len__() == 0:
                    return False
                ssh.connect(hostname=hostname, username=username, password=password, timeout=2)
            return True
        elif method == "telnet":
            pass

class run_config:
    def __init__(self, commands):
        self.commands = commands

    def run(self, hostname, username, password):
        if self.commands.__len__() == 0: return False
        method = Device.objects.filter(host=hostname)[0].loginmethod
        if method == "ssh":
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            try:
                ssh.connect(hostname=hostname, username=username, password=password, timeout=2)
            except:
                return False
            shell = ssh.invoke_shell()
            shell.send('config terminal' + '\r\n')
            for command in self.commands:
                shell.send(command + '\r\n')
                sleep(0.5)
            return True
        elif method == "telnet":
            pass

class show_running:
    def run(self, hostname, username, password):
        method = Device.objects.filter(host=hostname)[0].loginmethod
        if method == "ssh":
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            try:
                ssh.connect(hostname=hostname, username=username, password=password, timeout=2)
            except:
                return False
            stdin, stdout, stderr = ssh.exec_command('show running-config')
            result = stdout.readlines()
            for i, value in enumerate(result):
                result[i] = value.replace('\r', '')
            return result
        elif method == "telnet":
            pass

