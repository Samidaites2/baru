import socket
from asyncio import get_running_loop
from functools import partial

def _netcat(host, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    while True:
        data = s.recv(4096).decode("utf-8").strip("\n\x00")
        if not data:
            break
        return data
    s.close()

async def is_heroku():
    return "heroku" in socket.getfqdn()


async def user_input(input):
    if " " in input or "\n" in input:
        return str(input.split(maxsplit=1)[1].strip())
    return ""

async def paste_queue(content):
    loop = get_running_loop()
    link = await loop.run_in_executor(
        None, partial(_netcat, "ezup.dev", 9999, content)
    )
    return link

