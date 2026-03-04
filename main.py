import socket
from http_parser import HttpRequest
from router import Router

HOST = "127.0.0.1"
PORT = 8080

router = Router()

##Handlers
def home_handler(request):
    return "Welcome to From Scratch HTTP Server"


def hello_handler(request):
    return "Hello from router!"


def stats_handler(request):
    return "Server running. Everything OK."

##Register routes
router.add_route("GET", "/", home_handler)
router.add_route("GET", "/hello", hello_handler)
router.add_route("GET", "/stats", stats_handler)

##TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server running on http://{HOST}:{PORT}")

while True:
    client_socket, client_address = server_socket.accept()

    request_data = client_socket.recv(1024)

    if not request_data:
        client_socket.close()
        continue

    raw_request = request_data.decode()
    request = HttpRequest(raw_request)

    print("\nParsed Request:")
    print("Method:", request.method)
    print("Path:", request.path)

    handler = router.resolve(request.method, request.path)

    if handler:
        body = handler(request)
    else:
        body = "404 Not Found"

    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(body)}\r\n"
        "\r\n"
        f"{body}"
    )

    client_socket.sendall(response.encode())
    client_socket.close()