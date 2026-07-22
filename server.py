import asyncio
import socket
from typing import List

SERVER_ADDRESS = ('localhost', 5001)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(SERVER_ADDRESS)

server_socket.listen()
server_socket.setblocking(False)

queue = asyncio.Queue()

client_sockets: List[socket.socket] = []
receiving_tasks: dict[socket.socket, asyncio.Task] = {}


async def handle_recv(client_socket, loop):
    try:
        while True:
            if client_sockets:
                message = await loop.sock_recv(client_socket, 1024)
                if not message:
                    break
                print(message)
                await queue.put((client_socket, message))
    finally:
        client_sockets.remove(client_socket)
        task = receiving_tasks.get(client_socket)
        task.cancel()
        receiving_tasks.pop(client_socket)
        client_socket.close()



async def broadcast():
    while True:
        current_socket, message = await queue.get()
        for client_socket in filter(lambda x: x != current_socket, client_sockets):
            client_socket.send(message)
        queue.task_done()


async def main():
    loop = asyncio.get_running_loop()
    while True:
        try:
            client_socket, _ = await loop.sock_accept(server_socket)
            client_sockets.append(client_socket)
            task = asyncio.create_task(handle_recv(client_socket, loop))
            receiving_tasks[client_socket] = task
            asyncio.create_task(broadcast())
        except socket.error:
            print('Client disconnected')
            continue
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    asyncio.run(main())
    server_socket.close()