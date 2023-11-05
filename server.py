#!/usr/bin/env python

# modules
import socket
import threading
import random

def comput_bytes(data):
    data_bytes = data.encode('utf-8')
    bytes_length = len(data_bytes).to_bytes(4, byteorder='big')

    return data_bytes, bytes_length

def encode(data_dict):
    encoded_bytes = b""  # Initialize an empty byte string

    # value of question key
    value = data_dict[q_KEY]

    # converting question to bytes
    key_bytes, key_length_bytes = comput_bytes(q_KEY)
    value_bytes,value_length_bytes = comput_bytes(value)

    # Append the key length, key, value length, and value to the encoded bytes
    encoded_bytes += key_length_bytes + key_bytes + value_length_bytes + value_bytes

    # Converting to the choices to bytes
    bytes,length_bytes = comput_bytes(c_KEY)
    encoded_bytes += length_bytes + bytes

    # value of choice key
    value = data_dict[c_KEY]

    # converting the list of value to bytes
    for c in value:
        value_bytes, value_length_bytes = comput_bytes(c)
        encoded_bytes += value_length_bytes + value_bytes
    
    return encoded_bytes

def convertQtobQ(questions):
    bquestion = {}
    for i,j in questions.items():
        bquestion.setdefault(i,encode(j))
    return bquestion

def handle_client(client_socket):
    
    try:
        # user_question="Enter your Name: "
        # client_socket.send(user_question.encode('utf-8'))
        # client_id = client_socket.recv(1024).decode('utf-8')
        # print(f"{client_id} trys to connect...")

        client_id=client_socket.recv(1024).decode('utf-8')

        print(f'{client_id.upper()} connected')

        # Initialize the client with no of questions
        client_socket.send(str(NO_OF_QUES).encode('utf-8'))

        # sending questions
        for q_ID in random.sample(q_IDs,NO_OF_QUES):

            # Sending the question of particular question id
            client_socket.send(bquestion[q_ID])

            # receiving the choice sent by the client
            c = int(client_socket.recv(1024).decode('utf-8')) 

            print(f'the {client_id} give the choice {c} for question {q_ID}.')

        print("%s completed." % client_id)
    except Exception as e:
        print(e)
        print("%s exits from test." % client_id)
    finally:
        client_socket.close()

# IP and port number
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 1111

NO_OF_QUES = 5

q_KEY = 'question'
c_KEY = 'choices'

CLIENTS = ('21CS321', '21EE124','21EC231')

questions = {
    1: {
        q_KEY: 'How are you',
        c_KEY: ['fine', 'not bad', 'good', 'can\'t disclose']
    },
    2: {
        q_KEY: 'What is your name',
        c_KEY: ['Alice', 'Bob', 'Charlie', 'David']
    },
    3: {
        q_KEY: 'Where are you from',
        c_KEY: ['USA', 'Canada', 'UK', 'Australia']
    },
    4: {
        q_KEY: 'Favorite color',
        c_KEY: ['Red', 'Blue', 'Green', 'Yellow']
    },
    5: {
        q_KEY: 'What is your favorite food',
        c_KEY: ['Pizza', 'Burger', 'Sushi', 'Pasta']
    },
    6: {
        q_KEY: 'How do you like to spend your weekends',
        c_KEY: ['Reading', 'Hiking', 'Netflix', 'Gaming']
    },
    7: {
        q_KEY: 'Favorite animal',
        c_KEY: ['Dog', 'Cat', 'Dolphin', 'Elephant']
    },
    8: {
        q_KEY: 'Favorite movie genre',
        c_KEY: ['Action', 'Comedy', 'Drama', 'Science Fiction']
    },
    9: {
        q_KEY: 'What\'s your dream travel destination',
        c_KEY: ['Paris', 'Tokyo', 'Hawaii', 'New York']
    },
    10: {
        q_KEY: 'What\'s your preferred way of transportation',
        c_KEY: ['Car', 'Bicycle', 'Public Transit', 'Walking']
    },
    # Add more questions here as needed
}

bquestion = convertQtobQ(questions)
q_IDs = list(questions.keys())

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)

while True:
    # print("Waiting for a client to connect...")
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")
    
    # Create a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    
    # client_threads.append(client_thread)
    client_thread.start()
    