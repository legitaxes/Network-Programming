import socket
import select

port = 60003
sockL = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockL.bind(("localhost", port))
sockL.listen(1)

listOfSockets = [sockL]

print(f"Listening on port {port}")

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
            s.sendall(f"[{addr}] (connected)".encode('ASCII'))

    else:
        # connected clients send data or are disconnecting
        data = sock.recv(2048)
        if not data:
            # client disconnects, close the socket object and remove from listOfSockets
            sock.close()
            listOfSockets.remove(sock)
            # notify all other clients about the disconnected client
            for s in listOfSockets:
                s.sendall(f"[{addr}] (disconnected)".encode('ASCII'))
            
        else:
            # a client sends data, this data is message from a client and will be sent to all other clients connected
            message = input('Chat: ')
            final_message = f"[{addr}] {message}"
            for s in listOfSockets:
                if s != sockL and s != sock:
                    s.sendall(final_message.encode('ASCII'))