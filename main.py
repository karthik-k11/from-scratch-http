import socket
from http_parser import HttpRequest
from router import Router
import json
import threading
from logger import log_info, log_error

HOST = "127.0.0.1"
PORT = 8080

router = Router()

##Handlers
def home_handler(request):
    return "Welcome to From Scratch HTTP Server"


def hello_handler(request):
    name = request.query_params.get("name", "Guest")
    return f"Hello {name}"


def stats_handler(request):
    return "Server running. Everything OK."


def echo_handler(request):

    if not request.body:
        return "Empty body"

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return "Invalid JSON"

    name = data.get("name", "Unknown")

    return f"Hello {name}, JSON received!"

##Routes
router.add_route("GET", "/", home_handler)
router.add_route("GET", "/hello", hello_handler)
router.add_route("GET", "/stats", stats_handler)
router.add_route("POST", "/echo", echo_handler)

##Server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server running on http://{HOST}:{PORT}")


##Handler 
def handle_client(client_socket, client_address):

    request_data = client_socket.recv(1024)

    if not request_data:
        client_socket.close()
        return

    raw_request = request_data.decode()

    request = HttpRequest(raw_request)

    print("\nParsed Request:")
    print("Client:", client_address)
    print("Method:", request.method)
    print("Path:", request.path)
    print("Query Params:", request.query_params)
    print("Body:", request.body)

    handler = router.resolve(request.method, request.path)

    if handler:
        body = handler(request)
        status_line = "HTTP/1.1 200 OK"
    else:
        body = "404 Not Found"
        status_line = "HTTP/1.1 404 Not Found"

    body_bytes = body.encode()

    response = (
        f"{status_line}\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        "\r\n"
    ).encode() + body_bytes

    client_socket.sendall(response)

    client_socket.close()

while True:

    client_socket, client_address = server_socket.accept()

    thread = threading.Thread(
        target=handle_client,
        args=(client_socket, client_address)
    )

    thread.start()