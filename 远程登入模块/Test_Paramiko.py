import paramiko

def ssh_connect( _host, _username, _password ):
    try:
        _ssh_fd = paramiko.SSHClient()
        _ssh_fd.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
        _ssh_fd.connect( _host, username = _username, password = _password )
    except Exception, e:
        print( 'ssh %s@%s: %s' % (_username, _host, e) )
        exit()
    return _ssh_fd

def ssh_exec_cmd( _ssh_fd, _cmd ):
    return _ssh_fd.exec_command( _cmd )

def ssh_close( _ssh_fd ):
    _ssh_fd.close()

