import paramiko
import time

class fetch:
    """
    fetch class include tools for process interaction between local and remote device
        - search_match() can return how many commands not found on device
        - search_config() can return associate commands found on device
        - run_config() can run commands on device one by one
    """
    def __init__(self, hostname, method, username, password, port=22):
        self.hostname = hostname
        self.method = method
        self.username = username
        self.password = password
        # self.port is a bug here, need fix...
        # example: input telnet method & unusual port...
        self.port = port
        if self.method == "telnet":
            self.port = 23
        else:
            pass
            #jump out & log

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def search_match(self, search_list):
        """
        - Input list 'search_list'
        - Return missed count of result for run list 'search_list' on device
        """
        if search_list.__len__() == 0: return 0
        
        flag = 0
        if self.method == "ssh":
            for search_str in search_list:
                self.ssh.connect(hostname=self.hostname, username=self.username, password=self.password, port=self.port)
                stdin, stdout, stderr = self.ssh.exec_command('show running-config | include ' + search_str)
                if stdout.readlines().__len__() == 0:
                    flag += 1
        elif self.method == "telnet":
            pass
        else:
            pass
        return flag

    def search_config(self, search_list):
        """
        - Input list 'search_list'
        - Return result list for run list 'search_list' on device
        """
        if search_list.__len__() == 0: return []
        
        result = []
        if self.method == "ssh":
            for search_str in search_list:
                self.ssh.connect(hostname=self.hostname, username=self.username, password=self.password, port=self.port)
                stdin, stdout, stderr = self.ssh.exec_command('show running-config | include ' + search_str)
                result.extend(stdout.readlines())
        elif self.method == "telnet":
            pass
        else:
            pass
        return result

    def search_running(self):
        if self.method == "ssh":
            self.ssh.connect(hostname=self.hostname, username=self.username, password=self.password, port=self.port)
            stdin, stdout, stderr = self.ssh.exec_command('show running-config')
            return stdout.readlines()
        elif self.method == "telnet":
            pass

    def run_config(self, cmd_list):
        """
        - Input list 'cmd_list'
        - Run commands in list 'cmd_list' on device
        """
        if self.method == "ssh":
            shell = self.ssh.invoke_shell()
            for cmd in cmd_list:
                shell.send(cmd + '\r\n')
                #here will be a lag... is there any other way for waiting device echo?
                time.sleep(1)
                
