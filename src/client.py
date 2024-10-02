import socket
import sys


SERVER_PORT = 2223
def main() :
    # Define the server port
    global SERVER_PORT

     # Check the number of command line arguments
    if len(sys.argv) < 2:
        print("Usage: client <Server IP Address>")
        sys.exit(1)
    server_ip = sys.argv[1]
    
    # Try to open a socket to the server
    with socket.create_connection((server_ip, SERVER_PORT)) as client_socket:
        print(f"Connected to {server_ip} on port {SERVER_PORT}")
        while True:
            user_input = input("C: ")
            client_socket.send(user_input.encode())
            server_response = client_socket.recv(4096).decode()
            
            # If no response from the server, break the loop
            if not server_response:
                print("No response from server. Exiting.")
                break
            else:
                print("S", server_response) 

            # Shutdown
            if user_input == "SHUTDOWN" and server_response == "200 OK":
                sys.exit(0)

            # QUIT
            if user_input == "QUIT" and server_response == "200 OK":
                client_socket.close()
                break


if __name__ == "__main__":
    main()