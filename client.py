import socket

def help_decode(encoded_bytes,index):
    d_length = int.from_bytes(encoded_bytes[index:index+4], byteorder='big')
    index+=4
    d = encoded_bytes[index:index+d_length].decode('utf-8')
    index+=d_length
    
    return d, index

def decode(encoded_bytes):
    decoded_dict = {}
    index = 0

    # To encode the question
    # Extract the key length (4 bytes) and convert it to an integer
    key, index = help_decode(encoded_bytes, index)

    # Extract the value length (4 bytes) and convert it to an integer
    value,index = help_decode(encoded_bytes, index)
    decoded_dict[key] = value

    # Encoding choices
    choices = []
    key, index = help_decode(encoded_bytes, index)
    while index < len(encoded_bytes):
        value, index = help_decode(encoded_bytes,index)
        choices.append(value)
    decoded_dict[key] = choices

    return decoded_dict

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
    try:
        # name_prompt = client_socket.recv(1024).decode('utf-8')
        # print(name_prompt, end='')

       
        name = input('Enter the id. : ')
        client_socket.send(name.encode('utf-8'))
        
        print('Entering into the quiz....')
        NO_OF_QUES = int(client_socket.recv(1024).decode('utf-8'))

        for i in range(NO_OF_QUES):
            data = client_socket.recv(1024)
            if data != '':
                question = decode(data)
                choice = pprint(question)
                client_socket.send(str(choice).encode('utf-8'))

        client_socket.close()
        print("The test completed....")
        break
    except KeyboardInterrupt:
        print("Exited from test...")
        client_socket.close()
        break
    except Exception as e:
        print(e)
        client_socket.close()
        break
