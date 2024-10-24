### import modules
import socket


### functions
def serversideGetPlaySocket():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the address and port
    server_address = ('localhost', 60003)
    print('Starting up on %s port %s' % server_address)
    sock.bind(server_address)
    # Listen for incoming connections
    sock.listen(1)
    return sock


def clientsideGetPlaySocket(host, port=60003):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the port where the server is listening
    server_address = (host, port)
    print(f'Connecting to {host} port {port}')
    sock.connect(server_address)
    return sock


def game_logic(choice: str, opponent_choice: str, score: list):
    """
        This function checks who won the round by 
        comparing the choices of the player and the opponent.
        Returns: score
    """
    choice = choice.upper()
    opponent_choice = opponent_choice.upper()
    if choice == "R" and opponent_choice == "S":
        score[0] += 1
    elif choice == "S" and opponent_choice == "R":
        score[1] += 1
    elif choice == "P" and opponent_choice == "R":
        score[0] += 1
    elif choice == "R" and opponent_choice == "P":
        score[1] += 1
    elif choice == "S" and opponent_choice == "P":
        score[0] += 1
    elif choice == "P" and opponent_choice == "S":
        score[1] += 1
    elif choice == opponent_choice:
        # continue the game if it's a tie
        pass 
    return score


def check_win(score: list):
    if score[0] == 10:
        print(f"You win with {score[0]} against {score[1]}!")
    else:
        print(f"You lost with {score[0]} against {score[1]}!")


def check_valid_choice(choice: str):
    """
        This function checks if the input is valid.
        Returns: True if the input is invalid, False otherwise
    """
    if choice in ["R", "P", "S"]:
        return False
    else:
        print("Invalid input, Enter either 'R', 'P' or 'S'")
        return True


### main
def main():
    answer = "ASDQWERTY"
    score = [0, 0]

    while answer != "C" or answer != "S":
        answer = input("Do you want to be server (S) or client (C): ")
        if answer == "C":
            host = input("Enter the server's name or IP: ")
            sock = clientsideGetPlaySocket(host)
            break

        elif answer == "S":
            sock = serversideGetPlaySocket()
            print("Waiting for a connection...")
            conn, addr = sock.accept()
            break
        else:
            print("Invalid input, Enter either 'C' or 'S'")

    print("Connection established!")
    print("Welcome to Rock Paper Scissors!")

    if answer == "C":
        while 10 not in score:
            validity_input = True
            while validity_input:
                choice = input(f"({score[0]},{score[1]}) Your move: ")
                validity_input = check_valid_choice(choice)
            sock.sendall(choice.encode("ASCII"))
            data = sock.recv(1024)
            # convert bytes to string
            txt = data.decode("ASCII")
            print(f"(opponent's move: {txt})")
            # check who wins
            score = game_logic(choice, txt, score)
            if not data:
                break
    
    
    elif answer == "S":
        with conn:
            print(f'Connected to {addr}...')
            while 10 not in score:
                validity_input = True
                while validity_input:
                    choice = input(f"({score[0]},{score[1]}) Your move: ")
                    validity_input = check_valid_choice(choice)
                data = conn.recv(1024)
                
                conn.sendall(choice.encode("ASCII"))
                # convert bytes to string
                txt = data.decode("ASCII")
                print(f"(opponent's move: {txt})")
                # check who wins
                score = game_logic(choice, txt, score)
                if not data:
                    break

    print("Game Over!")
    check_win(score)


if __name__ == "__main__":
    main()