import socket
import time
import sys

host = socket.gethostbyname(socket.gethostname())
port = 5011
flag = True

def replacing_punctuations(words:str):
    a  = {',': '',
        '.': ''}
    for key, value in a.items():
        words = words.replace(key, value, -1).lower()
    return words

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket_obj:
    server_socket_obj.bind((host, port))
    server_socket_obj.listen(5)
    print('Open to receiving connection...\n')
    try:
        conn_obj, addr = server_socket_obj.accept()  # we did'nt add this in the `whille loop` as mostly seen since we are expecting just one connection
        print(F'Got connection from {addr}.\n')

        while flag:
            with conn_obj:
                with open('files/text_file.txt', 'r') as file_handler:
                    for (i,lines) in enumerate(file_handler):
                        lines = replacing_punctuations(lines)
                        print('batch', i,lines)     
                        conn_obj.send(bytes(lines, 'utf-8'))
                        time.sleep(5)
                    else:
                        print('End of file(EOF) reached.\n')
                        flag = False # if we got here our text file is already exhausted

    except Exception and KeyboardInterrupt  as err: 
        print('Error occured when connecting or sending data to the client \n', sys.exc_info())
        server_socket_obj.shutdown(socket.SHUT_RDWR)   # our context manager would manage the `server_socket_obj.close()`
        sys.exit()

    else:
        server_socket_obj.shutdown(socket.SHUT_RDWR)  # our context manager would manage the `server_socket_obj.close()
        print('All went good...\n')
        
    finally:
        print('Server connection successfully closed.')