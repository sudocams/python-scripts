#pip install colorama

import argparse
import socket
from colorama import init, Fore
from threading import Thread, Lock
from queue import Queue

init()
GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY= Fore.LIGHTBLACK_EX

no_of_threads = 200
q= Queue()
print_lock = Lock()

#colorama will be used to provide colors to the port when open or closed

def port_scan(port):
    

    try:
        #tries to connect to host using that port
        s= socket.socket()
        s.connect((host, port))
    except:
        #if connection is not establishes, it resturns false
        with print_lock:
            print(f"{GRAY} {host:15}:{port:5} is closed   {RESET}", end="\r")
    else:
        #returns true is connection
        with print_lock:
            print(f"{GREEN} {host:15}:{port:5} is open    {RESET}")
    finally:
        s.close()
        

def scan_thread():
    global q
    while True:
        worker = q.get()
        port_scan(worker)
        q.task_done()

def main(host, ports):
    global q

    for t in range(no_of_threads):
        t = Thread(target=scan_thread)
        t.daemon = True
        t.start()
    
    for worker in ports:
        q.put(worker)
    q.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="simple port scanner")
    parser.add_argument("host", help="host to scan")
    parser.add_argument("--ports", "-p", dest="port_range", default="1-65535", help="port range to scan, default is 1-65535 (all ports)")
    args = parser.parse_args()
    host, port_range = args.host, args.port_range

    start_port, end_port = port_range.split("-")
    start_port, end_port = int(start_port), int(end_port)


    ports = [p for p in range(start_port, end_port)]
    main(host, ports)



#python3 port_scanner.py 192.168.0.1 --ports 1-5000