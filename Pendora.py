import threading, socket, os, sys, colorama, time
from datetime import datetime
from colorama import *

if len(sys.argv) != 2:
    print("This Script Requires 2 Arguments, " + str(len(sys.argv)) + " Were Given\nExample: python3 script.py 127.0.0.1")
    sys.exit()
else:
    pass

target = sys.argv[1]

print("-" * 41)
print("Scanning: " + target)
ts = "Time Started:  " + str(datetime.now())
print(ts[:31])
print("-" * 41)
start = time.time()

ports = []

def scan(port):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)

    try:
        connection.connect((target, port))
        connection.close()
        print(f"{Fore.WHITE}Port {Fore.RED}[{port}]{Fore.WHITE} is open")
        ports.append(port)
    except Exception:
        pass
    
scanned = 1
for port in range(1, 65500):
    thread1 = threading.Thread(target=scan, args=[port])
    scanned +=1
    thread1.start()

print(f"{scanned} ports were scanned")
print(f'Open ports: ' + str(ports))

print("\n"+str(len(ports))+ " port(s) were open")

def bannergrab(port):
    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        connection.connect((target, port))
        connection.send(b'GET HTTP/1.1\n')
        banner = connection.recv(1024)
        print(f'[{port}] Service: '+str(banner.decode('utf-8')))
    except Exception:
        pass


print(f'\n{Fore.GREEN}[+] Fetching more information...\n\n{Fore.WHITE}')

for port in ports:
    thread2 = threading.Thread(target=bannergrab, args=[port])
    thread2.start()


thread2.join()
end = time.time()
total = end - start
print("\n"+str(total)[:4] + " Seconds")
