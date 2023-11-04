import socket
import json

def pprint(question):
    print('\n1) %s\r' % question['question'])
    for i in range(4):
        print(f"[{i+1}] {question['choices'][i]}")

    choice = int(input('\nEnter the choice : ').strip())

    input('\nConfirm the Choice %d, press enter.' % choice)

    return choice

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 1111
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))


while True:
    name_prompt = client_socket.recv(1024).decode()
    print(name_prompt, end='')
    
    name = input()
    client_socket.send(name.encode())
    NO_OF_QUES = int(client_socket.recv(1024).decode())
    for i in range(NO_OF_QUES):
        data = client_socket.recv(1024).decode()
        if data != '':
            question = json.loads(data)
            choice = pprint(question)
            client_socket.send(str(choice).encode())
    client_socket.close()
    break
