import json
import psycopg2
import threading
import socket

# Socket buffer
BUFFER = 2048

# DB Error Message
serr = '{"status":false, "err":"Server error, please try again."}'
serr = serr.encode()

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
    conn, cursor =  psql_conn()

    if conn:
        print("Processing Register Request.")
        user = data['user']
        email = data['email']
        pswd = data['pswd']
        unique_user = "SELECT COUNT(*) FROM users where username=%s"
        unique_email = "SELECT COUNT(*) FROM users where email=%s"
       
        reg_errs = ['{"status":false, "err":"Username and email is already taken."}',
                    '{"status":false, "err":"Username is already taken."}',
                    '{"status":false, "err":"Email is already taken."}']

        err = None

        try:
            cursor.execute(unique_user, (user,))
            user_row = cursor.fetchone()[0]
            cursor.execute(unique_email, (email,))
            email_row = cursor.fetchone()[0]

            if user_row != 0 and email_row != 0:
                err = reg_errs[0]
            elif user_row != 0:
                err = reg_errs[1]
            elif email_row != 0:
                err = reg_errs[2]

            if err is not None:
                err = err.encode()
                cli_sock.send(err)
            else:
                query ="INSERT INTO users(username, email, password) VALUES (%s, %s, crypt(%s, gen_salt('bf')))"
                cursor.execute(query, (user, email, pswd))
                info = '{"status":true}'
                info = info.encode()
                cli_sock.send(info)

                conn.commit()
        
        except Exception as error:
            print(error)
            cli_sock.send(serr)

        finally:
            conn.close()
            cursor.close()

    else:
        cli_sock.send(serr)
    
    cli_sock.close()

def login(cli_sock, data):
    conn, cursor = psql_conn()
    
    if conn:
        print("Processing Login Request.")
        user = data['user']
        pswd = data['pswd']
        query = "SELECT id, email, notification FROM users WHERE username=%s AND password=crypt(%s, password)"

        try:
            cursor.execute(query, (user, pswd))
            if (cursor.rowcount):
                iD, email, alert = cursor.fetchone()
                if alert:
                    info = f'{{"status":true, "id":{iD}, "email":"{email}", "notification":true}}'
                else:
                    info = f'{{"status":true, "id":{iD}, "email":"{email}", "notification":false}}'

                info = info.encode()
                cli_sock.send(info)

            else:
                err = '{"status":false, "err":"Username and password do not match."}'
                err = err.encode()
                cli_sock.send(err)

        except Exception as error:
                print(error)
                cli_sock.send(serr)
        finally:
            conn.close()
            cursor.close()

    else:
        cli_sock.send(serr)

    cli_sock.close()

def update(cli_sock, data):
    conn, cursor = psql_conn()
    
    if conn:
        attr = data['attr']
        print(f"Processing Update Request: {attr}.")

        iD = data['id']
        old = data['old']
        new = data['new']
        pswd = data['pswd']
       
        try:
            auth = "SELECT * FROM users WHERE id=%s AND password=crypt(%s, password)"
            cursor.execute(auth, (iD, pswd))
            if (cursor.rowcount):
                if attr == "password":
                    query = f"UPDATE users SET {attr}=crypt(%s, gen_salt('bf')) WHERE id=%s AND {attr}=crypt(%s, password)"
                else:
                    query = f"UPDATE users SET {attr}=%s WHERE id=%s AND {attr}=%s"
                
                cursor.execute(query, (new, iD, old))

                if attr == "password":
                    msg = '{"status":true}'
                else:
                    msg = f'{{"status":true, "{attr}":"{new}"}}'

                msg = msg.encode()
                cli_sock.send(msg)
                conn.commit()
            else:
                err = '{"status":false, "err":"Incorrect password"}'
                err = err.encode()
                cli_sock.send(err)
        
        except Exception as error:
            print(error)
            cli_sock.send(serr)

        finally:
            conn.close()
            cursor.close()

    else:
        cli_sock.send(serr)

    cli_sock.close()

def switch_notification(cli_sock, data):
    conn, cursor = psql_conn()

    if conn:
        print(f"Processing Notification Switch Request.")
        iD = data['id']
        notification = data['notification']

        try:
            query = "UPDATE users SET notification=%s WHERE id=%s"
            cursor.execute(query, (notification,iD))
            conn.commit()
 
            if notification:
                msg = '{"status":true, "notificaion":true}'
            else:
                msg = '{"status":true, "notificaion":false}'

            msg = msg.encode()
            cli_sock.send(msg)

        except Exception as error:
            print(error)
            cli_sock.send(serr)

        finally:
            conn.close()
            cursor.close()

    else:
        cli_sock.send(serr)

    cli_sock.close()

def get_email(cli_sock, data):
    conn, cursor = psql_conn()

    if conn:
        print(f"Processing get email request.")
        option = data['option']

        try:
            if option == 2:
                query = "SELECT email FROM users"
            elif option == 1:
                query = "SELECT email FROM users where notification=true"
            else:
                query = "SELECT email FROM users where notification=false"

            cursor.execute(query)
            rows = cursor.fetchall()

            msg = {"status": True, "emails": []}
            for row in rows:
                msg["emails"].append(row[0])

            msg = json.dumps(msg)
            msg = msg.encode()
            cli_sock.send(msg)

        except Exception as error:
            print(error)
            cli_sock.send(serr)

        finally:
            conn.close()
            cursor.close()

    else:
        cli_sock.send(serr)

    cli_sock.close()

def process(cli_sock):
    cli_sock.settimeout(10)
    raw = cli_sock.recv(BUFFER)
    raw = raw.decode()
    data = json.loads(raw)
    func_ptr = None

    func = data["func"]

    if func == "register":
        register(cli_sock, data)

    elif func == "login":
        login(cli_sock, data)
 
    elif func == "update":
        update(cli_sock, data)

    elif func == "switch_notification":
        switch_notification(cli_sock, data)
    
    elif func == "get_email":
        get_email(cli_sock, data)

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
