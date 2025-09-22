import os, sys

if __name__ == '__main__':
    print("Starting the script...")
    
    if sys.version_info[0] == 3 and sys.version_info[1] >= 6:
        print("Python version is 3.6 or later.")

        from baiskoafu_auth import login
        from baiskoafu_download_manager import is_connected
        import config

        if is_connected():
            print("Internet connection is available.")

            username = config.username
            password = config.password

            if username == "" or password == "":
                print("Username or password is empty.")
                input("Enter username and password in 'config.py' file")
            else:
                print("Username and password found in config.")
                if len(sys.argv) == 2:
                    print(f"Logging in with argument: {sys.argv[1]}")
                    login(username, password, sys.argv[1])
                else:
                    print("Logging in without additional arguments.")
                    login(username, password)
        else:
            input("No connection :(")

    else:
        print("Python 3.6 or later version required!")
        if sys.version_info[0] == 2:
            raw_input()
        else:
            input()
