import paramiko


class Ssh:

    def __init__(self, host, port, login, password):
        try:
            self.connection = paramiko.SSHClient()
            self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.connection.connect(hostname=host, username=login, password=password, port=port)
        except paramiko.ssh_exception.AuthenticationException as e:
            print(e)

    def remote_cmd(self, cmd):
        stdin, stdout, stderr = self.connection.exec_command(cmd)
        data = stdout.read().decode('utf-8').split("\n")
        data.pop(len(data) - 1)
        error_data = stderr.read().decode('utf-8').replace("\n", "")
        if len(error_data) > 1:
            raise ValueError(error_data)
        return data
