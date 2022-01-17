import socket
import time
import random
import threading
import requests
import json
import yaml

global_lock = threading.Lock()

port = input("Port: ")
y = int(input("Threads: "))
retry = int(input("Retries: "))
delay = int(input("Delay: "))
timeout = int(input("Timeout: "))

while True:
    geo = input("Geolocation (t/f): ")
    if geo == "t":
        geolocation = True
        break
    elif geo == "f":
        geolocation = False
        break

def write_to_file():
    with global_lock:
        with open("ips.txt", "a") as file:
            file.write(str(threading.get_ident()))
            file.write("\n")

def isOpen(ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
                s.connect((ip, int(port)))
                s.shutdown(socket.SHUT_RDWR)
                return True
        except:
                return False
        finally:
                s.close()

def checkHost(ip, port):
        ipup = False
        for i in range(retry):
                if isOpen(ip, port):
                        ipup = True
                        break
                else:
                        time.sleep(delay)
        return ipup

def mythread():
    if geolocation == True:
        while True:
            ip = (str(random.randrange(1, 255))+"."+str(random.randrange(1, 255))+"."+str(random.randrange(1, 255))+"."+str(random.randrange(1, 255)))
            if checkHost(ip, port):
                request_url = "http://ip-api.com/json/" + ip
                response = requests.get(request_url)
                result = response.content.decode()
                result = json.loads(result)
                print(yaml.safe_dump(result, allow_unicode=True, default_flow_style=False))
                with global_lock:
                    with open("ips.txt", "a") as file:
                        file.write(yaml.safe_dump(result, allow_unicode=True, default_flow_style=False))
                        file.write("\n")

                
    else:
        while True:
            ip = (str(random.randrange(1, 255))+"."+str(random.randrange(1, 255))+"."+str(random.randrange(1, 255))+"."+str(random.randrange(1, 255)))
            if checkHost(ip, port):
                print(ip)
                with global_lock:
                    with open("ips.txt", "a") as file:
                        file.write(ip)
                        file.write("\n")

def main():
    for i in range(y):
        t = threading.Thread(target=mythread)
        t.start()

if __name__ == "__main__":
    main()