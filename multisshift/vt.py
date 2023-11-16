import logging
import os
import re
import sys
from time import sleep
from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
import asyncio
import paramiko
import threading
import base64
from starlette.websockets import WebSocketState

app = FastAPI()

# Get the directory of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Construct paths relative to the script directory
static_path = os.path.join(script_directory, "web/static")
templates_path = os.path.join(script_directory, "web/templates")
app.mount("/static", StaticFiles(directory=static_path), name="static")
templates = Jinja2Templates(directory=templates_path)

class SSHClientManager:
    def __init__(self):
        self.clients = {}
        os.makedirs("logs", exist_ok=True)

    async def create_client(self, websocket):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.clients[websocket] = {
            'client': ssh_client,
            'channel': None
        }
        self.clients[websocket]['log_buffer'] = ''

    async def connect(self, websocket, hostname, port, username, auth_type, auth):
        print(f"hostname: {hostname}")
        print(f"user: {username}, auth_type: {auth_type}")

        ssh_client = self.clients[websocket]['client']
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            if auth_type == 'password':
                ssh_client.connect(hostname, port=int(port), username=username.strip(), password=auth.strip(), look_for_keys=False)
            elif auth_type == 'key':
                private_key = paramiko.RSAKey(filename=auth.strip())
                ssh_client.connect(hostname, port=int(port), username=username.strip(), pkey=private_key, look_for_keys=False)
            else:
                raise ValueError("Invalid authentication type")

            transport = ssh_client.get_transport()
            transport.set_keepalive(60)
            channel = ssh_client.invoke_shell(term="xterm")

            self.clients[websocket]['channel'] = channel

            logger = logging.getLogger(hostname)
            logger.setLevel(logging.INFO)
            fh = logging.FileHandler(f"logs/{hostname}.log")
            # formatter = logging.Formatter('')
            # fh.setFormatter(formatter)
            logger.addHandler(fh)
            self.clients[websocket]['logger'] = logger

            # Start a new thread to listen to responses from the server
            threading.Thread(target=self.listen_to_ssh_output, args=(websocket, channel), daemon=True).start()

        except paramiko.AuthenticationException as e:
            print(f"AuthenticationException: {e}")
            await websocket.send_json({'type': 'ssh_output', 'data': base64.b64encode(f'Connection failed: {e}'.encode('utf-8')).decode('utf-8')})

        except paramiko.SSHException as e:
            print(f"SSHException: {e}")
            await websocket.send_json({'type': 'ssh_output', 'data': base64.b64encode(f'Connection failed: {e}'.encode('utf-8')).decode('utf-8')})

        except ValueError as e:
            print(f"ValueError: {e}")
            await websocket.send_json({'type': 'ssh_output', 'data': base64.b64encode(f'Connection failed: {e}'.encode('utf-8')).decode('utf-8')})
    def listen_to_ssh_output(self, websocket, channel):
        logger = self.clients[websocket]['logger']
        log_buffer = self.clients[websocket]['log_buffer']
        while True:
            sleep(.05)
            if channel.recv_ready():
                data = channel.recv(1024)

                asyncio.run(websocket.send_json({'type': 'ssh_output', 'data': base64.b64encode(data).decode('utf-8')}))

                # Append new data to the buffer
                self.clients[websocket]['log_buffer'] += data.decode('utf-8')

                # Process complete lines for logging
                if '\n' in self.clients[websocket]['log_buffer']:
                    lines = self.clients[websocket]['log_buffer'].split('\n')
                    # Keep the last, possibly incomplete line in the buffer
                    self.clients[websocket]['log_buffer'] = lines[-1]

                    # Log each complete line
                    for line in lines[:-1]:  # Exclude the last line
                        line = line.replace('\r', '')
                        line = re.sub(r'\x1B[@-_][0-?]*[ -/]*[@-~]', '', line)
                        logger.info(line)

    async def send_input(self, websocket, input_data):
        channel = self.clients[websocket]['channel']
        if channel:
            channel.send(base64.b64decode(input_data).decode('utf-8'))

    async def resize_terminal(self, websocket, cols, rows):
        channel = self.clients[websocket]['channel']
        if channel:
            channel.resize_pty(width=cols-1, height=rows-2)

    async def disconnect(self, websocket):
        client_data = self.clients.get(websocket)
        if client_data:
            channel = client_data['channel']
            client = client_data['client']
            if channel:
                channel.close()
            client.close()
            del self.clients[websocket]

ssh_manager = SSHClientManager()


@app.get("/", response_class=HTMLResponse)
async def get_login(request: Request, host: str = "", port: str = "", username: str = "", password: str = ""):

    context = {
        "request": request,
        "host": host,
        "port": port,
        "username": username,
        "password": password  # Strongly consider more secure ways to handle passwords
    }
    return templates.TemplateResponse("login.html", context)

@app.get("/splash", response_class=HTMLResponse)
async def get_login(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("splash.html",context=context)

@app.get("/terminal", response_class=HTMLResponse)
async def get_terminal(request: Request, hostname: str = "", port: str = "", username: str = "", auth: str = "", auth_type: str = "password", key_file: str = ""):
    # auth = password if auth_type == "password" else key_file

    return templates.TemplateResponse("terminal.html", {
        "request": request,
        "hostname": hostname,
        "port": port,
        "username": username,
        "auth_type": auth_type,
        "auth": auth
    })



@app.websocket("/terminal")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await ssh_manager.create_client(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if data['type'] == 'sshconnect':
                await ssh_manager.connect(
                    websocket,
                    data['hostname'],
                    data['port'],
                    data['username'],
                    data['auth_type'],
                    data['auth']  # password or key file path
                )
            elif data['type'] == 'input':
                await ssh_manager.send_input(websocket, data['data'])
            elif data['type'] == 'resize':
                await ssh_manager.resize_terminal(websocket, data['cols'], data['rows'])
    except WebSocketDisconnect:
        pass
        # await ssh_manager.disconnect(websocket)
    except Exception as e:
        await websocket.send_json({
            'type': 'ssh_output',
            'data': base64.b64encode(str(e).encode('utf-8')).decode('utf-8')
        })
    finally:
        await ssh_manager.disconnect(websocket)
        if not websocket.client_state == WebSocketState.DISCONNECTED:
            await websocket.close()


