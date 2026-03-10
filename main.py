import socket
from http_parser import HttpRequest
from router import Router
import json
import threading
from logger import log_info, log_error
from database.minidb import MiniDB
from middleware import MiddlewareManager, logging_middleware, timing_middleware

HOST = "127.0.0.1"
PORT = 8080

router = Router()
db = MiniDB()

middleware = MiddlewareManager()
middleware.add(logging_middleware)
middleware.add(timing_middleware)


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


def insert_handler(request):

    if not request.body:
        return "Empty body"

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return "Invalid JSON"

    key = data.get("key")
    value = data.get("value")

    if not key or not value:
        return "Missing key/value"

    db.insert(key, value)

    return "Inserted successfully"


def select_handler(request):

    key = request.query_params.get("key")

    if not key:
        return "Key required"

    value = db.select(key)

    if value is None:
        return "Key not found"

    return f"{key} = {value}"


def db_stats_handler(request):

    stats = db.stats()

    return f"Total keys: {stats['total_keys']}"


##Routes
router.add_route("GET", "/", home_handler)
router.add_route("GET", "/hello", hello_handler)
router.add_route("GET", "/stats", stats_handler)
router.add_route("POST", "/echo", echo_handler)

router.add_route("POST", "/insert", insert_handler)
router.add_route("GET", "/select", select_handler)
router.add_route("GET", "/dbstats", db_stats_handler)




##Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(100)

print(f"Server running on http://{HOST}:{PORT}")


##Client handler
def handle_client(client_socket, client_address):

    while True:

        request_data = client_socket.recv(1024)

        if not request_data:
            break

        raw_request = request_data.decode()

        request = HttpRequest(raw_request)
        middleware.run_before(request)

        log_info(f"{client_address} {request.method} {request.path}")

        handler = router.resolve(request.method, request.path)

        if handler:
            body = handler(request)
            status_line = "HTTP/1.1 200 OK"
            log_info(f"{request.method} {request.path} 200")
        else:
            body = "404 Not Found"
            status_line = "HTTP/1.1 404 Not Found"
            log_error(f"{request.method} {request.path} 404")

        body_bytes = body.encode()

        response = (
            f"{status_line}\r\n"
            "Content-Type: text/plain\r\n"
            f"Content-Length: {len(body_bytes)}\r\n"
            "\r\n"
        ).encode() + body_bytes

        client_socket.sendall(response)

        connection_header = request.headers.get("Connection", "").lower()

        if connection_header != "keep-alive":
            break

    client_socket.close()

while True:

    client_socket, client_address = server_socket.accept()

    thread = threading.Thread(
        target=handle_client,
        args=(client_socket, client_address)
    )

    thread.start()