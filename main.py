import socket

HOST = "127.0.0.1"
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server running on http://{HOST}:{PORT}")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"\nConnection received from {client_address}")

    request_data = client_socket.recv(1024)

    if not request_data:
        client_socket.close()
        continue

    print("Raw HTTP request:")
    print(request_data.decode())

    body = "Hi world"

    http_response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(body)}\r\n"
        "\r\n"
        f"{body}"
    )

    client_socket.sendall(http_response.encode())

    client_socket.close()