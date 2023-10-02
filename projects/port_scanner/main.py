from queue import Queue
import socket
import threading

target = '127.0.0.1'
queue = Queue()
open_ports = []


def get_ports(mode):
    match mode:
        case 1:
            for port in range(1, 1024):
                queue.put(port)
        case 2:
            for port in range(1, 49152):
                queue.put(port)
        case 3:
            ports = [20, 21, 22, 23, 25, 53, 80, 110, 443]
            for port in ports:
                queue.put(port)
        case 4:
            ports = input("Enter your ports (seperated by blanks):")
            ports = ports.split()
            ports = list(map(int, ports))
            for port in ports:
                queue.put(port)


def port_scan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        print(f"Port {port} is open!")
        return True
    except:
        print(f"Port {port} is closed!")
        return False


def worker():
    while not queue.empty():
        port = queue.get()
        if port_scan(port):
            print('Port {} is open!'.format(port))
            open_ports.append(port)


def main(threads, mode):
    get_ports(mode)
    thread_list = []

    for t in range(threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()
    print("Open ports are: ", open_ports)


if __name__ == '__main__':
    main()
