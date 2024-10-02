#Client connecting to the server using socket
#The clients sends commands to the server and server send back the result to client

#Import necessary libraries for socket programming
import socket
import sys

# Constant for server port
SERVER_PORT = 2223

# Defining main function to handle client communication with server
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
            try:
                user_input = input("\nC: ")
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
                    try:
                        client_socket.close()
                    except OSError as e:
                        print("Error occured due to closing the client socket")
                    break

            except Exception as e:
                print(f"An error occurred: {e}")
                break
            
#Starting of the program
if __name__ == "__main__":
    main()