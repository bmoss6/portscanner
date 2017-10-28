import ipaddress

for ip in ipaddress.ip_network('192.168.230.0/24'):
    print (str(ip))