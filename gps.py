#!env python3
"""Print the host name and the IP address of the wired ethernet interface"""

import socket

def gps():
    hostname = socket.gethostname()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(('8.8.8.8', 80))
        ipv4_address = s.getsockname()[0]
    return (hostname, ipv4_address)

def selftest():
    hostname, ipv4_address = gps()
    print({'host': hostname, 'ip': ipv4_address})

if __name__ == '__main__':
    selftest()
    
