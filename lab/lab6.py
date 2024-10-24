### import modules
import socket


### global variables
HTML_OK_RESPONSE = "HTTP/1.1 200 ok\n"
HTML_CONTENT = "<html>\n<pre>\n<h1>Your browser sent the following request:</h1>\n"

### functions
def serversideGetPlaySocket():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the address and port
    server_address = ('localhost', 80)
    print('Starting up on %s port %s' % server_address)
    sock.bind(server_address)
    # Listen for incoming connections
    sock.listen(1)
    return sock


def clientsideGetPlaySocket(host, port=80):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the port where the server is listening
    server_address = (host, port)
    print(f'Connecting to {host} port {port}')
    sock.connect(server_address)
    return sock


### main function
def main():
    answer = ""
    while answer != "y" and answer != "n":
        answer = input("Do you want to be the server? (y/n): ")
    
    if answer == "y":
        ### server side code
        sock = serversideGetPlaySocket()
        while True:
            print("Waiting for a connection")
            conn, client_address = sock.accept()
            print(f"Connection from {client_address}")
            data = conn.recv(1024)
            conn.sendall(HTML_OK_RESPONSE.encode("ASCII"))
            conn.sendall("\n".encode("ASCII"))
            conn.sendall(HTML_CONTENT.encode("ASCII"))
            conn.sendall(data)
            conn.sendall("</pre>\n</html>\n".encode("ASCII"))
            txt = data.decode("ASCII")
            print(f"Received: {txt}")
            conn.close()
    else:
        ### client side code
        host = input("Enter the host: ")
        sock = clientsideGetPlaySocket(host)
        print("Connected to the server!")
        text = input("Enter a message: ")
        sock.sendall(text.encode("ASCII"))
        data = sock.recv(1024)
        txt = data.decode("ASCII")
        print(f"Received: {txt}")
        sock.close()



if __name__ == '__main__':
    main()