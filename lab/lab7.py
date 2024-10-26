### import libraries
import socket
import select


### global variables
PORT = 60003
IP_ADDRESS = "localhost"


### main function
def main():
    sockL = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockL.bind((IP_ADDRESS, PORT))
    sockL.listen(1)

    listOfSockets = [sockL]

    print(f"Listening on port {PORT}")

    while True:
        tup = select.select(listOfSockets, [], [])
        sock = tup[0][0]

        if sock == sockL:
            # new client is connecting
            (sockClient, addr) = sockL.accept()
            # add new socket to listOfSockets
            listOfSockets.append(sockClient)
            # notify all other clients about the new client
            for s in listOfSockets:
                if s != sockL:
                    try:
                        s.sendall(f"[{addr}] (connected)".encode('ASCII'))
                    except Exception as e:
                        print(f"Error sending data: {e}")
                        listOfSockets.remove(s)
                        s.close()

        else:
            # connected clients send data or are disconnecting
            data = sock.recv(2048)
            if not data:
                # client disconnects, close the socket object and remove from listOfSockets
                listOfSockets.remove(sock)
                sock.close()
                # notify all other clients about the disconnected client
                for s in listOfSockets:
                    if s != sockL:
                        s.sendall(f"[{s.getpeername()}] (disconnected)".encode('ASCII'))
                
            else:
                # a client sends data, this data is message from a client and will be sent to all other clients connected
                message = data.decode('ASCII')
                # send the message back to the client 
                sock.sendall(f'{[sock.getpeername()]} {message}'.encode('ASCII'))
                # send the message to all other clients
                for s in listOfSockets:
                    try:
                        # check if the socket is not the server socket and not the client socket
                        if s != sock and s != sockL:
                            s.sendall(f'{[sock.getpeername()]} {message}'.encode('ASCII'))
                    except Exception as e:
                        print(f"Error sending data: {e}")
                        listOfSockets.remove(s)
                        s.close()


if __name__ == "__main__":
    main()