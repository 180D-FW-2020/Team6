import json
import psycopg2
import threading
import socket

# Socket buffer
BUFFER = 2048

# Psql cred
with open('psql_cred.json') as f:
    cred = json.load(f)

def psql_conn():
    conn, cursor = None, None
    try:
        conn = psycopg2.connect(user=cred['username'],
                                password=cred['password'],
                                host=cred['host'],
                                port=cred['port'],
                                database=cred['dbname'])
        cursor = conn.cursor()
    except Exception as error:
        print("Error while connecting to PostgreSQL", error)
         
    return (conn, cursor)

def register(cli_sock, data):
    pass

def login(cli_sock, data):
    conn, cursor = psql_conn()
    err = '{"status":false, "err":"Server error, please try again."}'
    err = err.encode()
    
    if conn:
        print("Processing Login Request")
        user = data['user']
        pswd = data['pswd']
        query = "SELECT notification FROM users WHERE username=%s AND password=crypt(%s, password)"

        try:
            cursor.execute(query, (user, pswd))
            if (cursor.rowcount):
                alert = cursor.fetchone()[0]

                if alert:
                    info = '{"status":true, "notification":true}'
                else:
                    info = '{"status":true, "notification":false}'
                info = info.encode()
                cli_sock.send(info)
            else:
                err = '{"status":false, "err":"Username and email do not match."}'
                err = err.encode()
                cli_sock.send(err)

        except Exception as error:
                print(error)
                cli_sock.send(err)
        finally:
            conn.close()
            cursor.close()
            cli_sock.close()

    else:
        cli_sock.send(err)

def process(cli_sock):
    cli_sock.settimeout(10)
    raw = cli_sock.recv(BUFFER)
    raw = raw.decode()
    data = json.loads(raw)
    func = None
    if data["func"] == "login":
        func = login

    if func:
        func_thread = threading.Thread(target=func, args=(cli_sock,data))
        func_thread.start()
    

def client_connection():
    addr = '0.0.0.0'
    port = 3333
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_sock.bind((addr, port))
    listen_sock.listen(10)
    print(f"Listening on port: {port}")
    
    while True:
        client, addr = listen_sock.accept()
        print(f"Accepted connection from {addr}")
        
        process_thread = threading.Thread(target=process, args=(client,))
        process_thread.start()

    listen_sock.close()


def main():
    _thread = threading.Thread(target=client_connection)
    _thread.start()

if __name__ == "__main__":
    main()
