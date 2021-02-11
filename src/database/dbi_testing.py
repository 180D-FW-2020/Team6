import DBInterface
import json

def main():
    # Correct user info
    dbi = DBInterface.DBInterface()
    raw = dbi.login("robertrudio", "test")
    data = json.loads(raw)
    print("Correct user info: " + str(data))

    # Incorrect username
    dbi = DBInterface.DBInterface()
    raw = dbi.login("robertrudi", "test")
    data = json.loads(raw)
    print("Incorrect username: " + str(data))

    # Incorrect password
    dbi = DBInterface.DBInterface()
    raw = dbi.login("robertrudio", "testfda")
    data = json.loads(raw)
    print("Incorrect password: " + str(data))

if __name__ == "__main__":
    main()