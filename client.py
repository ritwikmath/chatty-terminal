import socket
import threading
from prompt_toolkit import print_formatted_text, HTML, prompt

SERVER_ADDRESS = ('localhost', 5001)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(SERVER_ADDRESS)


def send_loop():
    while True:
        try:
            message = prompt("You: ")
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
            print_formatted_text(HTML(f"<violet>{message.decode('utf-8')}</violet>"))
        except OSError:
            break


if __name__ == '__main__':
    recv_thread = threading.Thread(target=recv_loop, daemon=True)
    send_thread = threading.Thread(target=send_loop, daemon=True)

    recv_thread.start()
    send_thread.start()

    send_thread.join()  # main thread waits here until send_loop exits (e.g. Ctrl+C or error)

    client_socket.close()