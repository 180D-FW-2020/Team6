import DBInterface
import json
import random
import string

def main():
    # Create DBInterface object
    dbi = DBInterface.DBInterface()

    # Correct user info
    raw = dbi.login("test_name", "test")
    data = json.loads(raw)
    print("Correct user info: " + str(data))

    # Incorrect username
    raw = dbi.login("incorrect_user", "test")
    data = json.loads(raw)
    print("Incorrect username: " + str(data))

    # Incorrect password
    raw = dbi.login("test_name", "incorrect_pswd")
    data = json.loads(raw)
    print("Incorrect password: " + str(data))

    # Username and email taken
    raw = dbi.register("test_name", "test_email@gmail.com", "temp")
    data = json.loads(raw)
    print("Username and email taken: " + str(data))

    # Username taken
    raw = dbi.register("test_name", "new@gmail.com", "temp")
    data = json.loads(raw)
    print("Username taken: " + str(data))

    # Email taken
    raw = dbi.register("new", "test_email@gmail.com", "temp")
    data = json.loads(raw)
    print("Email taken: " + str(data))

    # Good register
    user = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    email = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    raw = dbi.register(user, email, "temp")
    data = json.loads(raw)
    print("Good register: " + str(data))

if __name__ == "__main__":
    main()