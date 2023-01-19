from socket import *
from colors import colors
from dataclasses import dataclass
import os


@dataclass
class Connection:
    host: str
    port: int
    request: str


def validate_arguments(host, port, method, request):
    if any(i == "" for i in (host, port, method, request)):
        raise Exception("Invalid arguments")
    
    if not port.isdigit():
        raise Exception("Invalid port")
    
    if method.upper() not in ("GET", "POST", "PUT", "DELETE", "HEAD", "PATCH"):
        raise Exception("Invalid method")
    
    if not request.startswith("/"):
        raise Exception("Invalid request")
    

def main():
    while True:
        try:
            host = input('[HOST] ')
            port = input('[PORT] ')
            method = input('[METHOD] ')
            request = input('[REQUEST] ')
            validate_arguments(host, port, method, request)

            conn = Connection(host.lower(), int(port), f"{method.upper()} {request.lower()} HTTP/1.1")
            http_request(conn)

        except KeyboardInterrupt:
            break

        except Exception as e:
            print(colors.red, f"\nThe following error occurred: {e}")
            print(colors.lightgrey, "")

        

def send_request(conn: Connection, sck: socket):
    sck.send(conn.request.encode())
    sck.send('\r\n'.encode())
    sck.send(("HOST:" + conn.host).encode())
    sck.send('\r\n'.encode())
    sck.send('\r\n'.encode())


def get_response(conn: Connection, sck: socket):
    req = conn.request.split(" ")
    req[1] = f"{conn.host}:{conn.port}{req[1]}"
    print(f'\nFROM CLIENT:\n{" ".join(req)}\n')
    response = sck.recv(9000)
    print(f'FROM SERVER:\n{response.decode()}\n')
    sck.close()
    

def http_request(conn: Connection):
    sck = socket(AF_INET, SOCK_STREAM)
    sck.connect((conn.host,conn.port))
    send_request(conn, sck)
    get_response(conn, sck)


if __name__ == "__main__":
    os.system('cls')
    f = open("logo.txt","r")
    print("\n" + f.read())
    main() 
