import ipaddress
from datetime import datetime

from django.shortcuts import render


def sshView(request):
    ssh_snippet, need_telnet, privilege = '', '', ''
    ip_error = False
    if request.method == 'POST':
        try:
            ip_addr = ipaddress.ip_network(f"{request.POST.get('ip')}/{request.POST.get('mask')}")
        except ValueError:
            ip_addr = ipaddress.ip_network('192.168.1.0/24')
            ip_error = True
        if request.POST.get('need_telnet'):
            need_telnet = 'telnet'
        if request.POST.get('privilege'):
            privilege = '\nprivilege level 15'
        ssh_snippet = f'''
enable
clock set {datetime.now().strftime('%H:%M:%S %d %b %Y')}
conf t
ip domain name {request.POST.get('domain', 'test.site')}
hostname {request.POST.get('hostname', 'cisco')}
crypto key generate rsa modulus {request.POST.get('key_length', '1024')}
ip ssh time-out 60
ip ssh authentication-retries 2
ip ssh version 2
service password-encryption
username {request.POST.get('username', 'admin')} privilege 15 secret {request.POST.get('user_password', 'cisco')}
enable secret {request.POST.get('enable_password', 'cisco')}
aaa new-model
access-list 23 permit {ip_addr.network_address} {ip_addr.hostmask}
line vty 0 4
transport input ssh {need_telnet}
logging synchronous{privilege}
exec-timeout 60 0
access-class 23 in
end
copy run start
        '''
    return render(request, 'ssh/ssh.html', {'text': ssh_snippet, 'ip_error': ip_error})
