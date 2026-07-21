import socket
import threading

SERVER_ADDRESS = ('localhost', 5001)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(SERVER_ADDRESS)


def send_loop():
    while True:
        try:
            message = input('Enter your message: ')
            client_socket.send(message.encode('utf-8'))
        except (OSError, KeyboardInterrupt):
            break


def recv_loop():
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                print('\nServer closed the connection.')
                break
            print('\n' + message.decode('utf-8'))
        except OSError:
            break


if __name__ == '__main__':
    recv_thread = threading.Thread(target=recv_loop, daemon=True)
    send_thread = threading.Thread(target=send_loop, daemon=True)

    recv_thread.start()
    send_thread.start()

    send_thread.join()  # main thread waits here until send_loop exits (e.g. Ctrl+C or error)

    client_socket.close()