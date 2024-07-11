import socket
import pickle
import threading
import random

# Constants
GRID_SIZE = 10
GRID_WIDTH = 60
GRID_HEIGHT = 40
FPS = 15
SERVER_PORT = 12345

# Initialize sockets
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', SERVER_PORT))
server_socket.listen(2)

# Function to send data to the client
def send_data(conn, data):
    try:
        serialized_data = pickle.dumps(data)
        conn.sendall(serialized_data)
    except Exception as e:
        print(f"Error sending data: {e}")

# Function to receive data from the client
def receive_data(conn):
    try:
        serialized_data = conn.recv(1024)
        data = pickle.loads(serialized_data)
        return data
    except Exception as e:
        print(f"Error receiving data: {e}")
        return None

# Function to handle each client connection
def handle_client(conn, player_number):
    print(f"Player {player_number} connected.")
    if player_number == 1:
        start_pos_player = (5, 5)  # Initial position for player 1
        start_pos_opponent = (GRID_WIDTH - 6, GRID_HEIGHT - 6)  # Initial position for player 2
    else:
        start_pos_player = (GRID_WIDTH - 6, GRID_HEIGHT - 6)  # Initial position for player 2
        start_pos_opponent = (5, 5)  # Initial position for player 1

    player_snake = {"body": [start_pos_player], "direction": (1, 0)}
    opponent_snake = {"body": [start_pos_opponent], "direction": (-1, 0)}
    food_position = {"position": (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))}

    while True:
        try:
            send_data(conn, {"player_snake": player_snake["body"], "opponent_snake": opponent_snake["body"], "food_position": food_position["position"]})
            data = receive_data(conn)
            if data:
                player_snake["body"] = data["player_snake"]
                player_snake["direction"] = data["player_direction"]
                opponent_snake["body"] = data["opponent_snake"]
                food_position["position"] = data["food_position"]
            else:
                break
        except Exception as e:
            print(f"Error handling client {player_number}: {e}")
            break

    print(f"Player {player_number} disconnected.")
    conn.close()

# Main server loop
def main():
    print("Server started. Waiting for connections...")
    player_number = 1
    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr} established.")
        threading.Thread(target=handle_client, args=(conn, player_number)).start()
        player_number += 1
        if player_number > 2:
            break

if __name__ == "__main__":
    main()
