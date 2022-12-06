import time
import json
import pwinput
import bcrypt

creds_file = "creds.json"

def set_creds():
    
    time.sleep(1)
    
    # get credentials from user
    in_username = input("Username: ")
    in_password = pwinput.pwinput(prompt = "Password: ", mask = "*")

    # generate salt
    salt = bcrypt.gensalt()

    # initalize credentials dictionary
    creds_dict = {
        "username": in_username,
        "passwords": None
    }
    
    # initialize passwords dictionary
    creds_dict["passwords"] = {}
    
    # initialize hash_id counter
    hash_id = 0

    # populate passwords dictionary with hashed charachters from user password
    for char in in_password:
        hash_id += 1
        creds_dict["passwords"]["char" + str(hash_id)] = str(bcrypt.hashpw(char.encode('utf-8'), salt).decode("utf-8"))
    
    # save credentials dictionary to json
    with open(creds_file, "w") as outfile:
        json.dump(creds_dict, outfile, indent=2)

def check_creds(in_username, in_password):
    # time.sleep(1)

    # get credentials from user
    # in_username = input("Username: ")
    # in_password = pwinput.pwinput(prompt = "Password: ", mask = "*")

    # open credentials file for comparison
    with open(creds_file) as f:
        creds_dict = json.load(f)  
    
    # if username is incorrect return false
    if not in_username == creds_dict["username"]:
        print("Wrong username!")
        return False

    # # if password lengths mismatch return false
    # if not len(in_password) == len(creds_dict["passwords"]):
    #     print("Wrong password!")
    #     return False

    
    # if paswords value mismatch return false
    counter = 0
    for char, hash in zip(in_password, creds_dict["passwords"].values()):
        if not bcrypt.checkpw(char.encode('utf-8'), hash.encode('utf-8')):
            print("Wrong password!")
            return False
        time.sleep(0.25)
        counter = counter + 1

    if not counter == len(creds_dict["passwords"]):
        print("Wrong password!")
        return False

    # if all credentials are correct, return true
    print("Access granted!")
    return True

def brute_force(seed=""):
    possible_chars = '0123456789abcdefghijklmnopqrstuvwxyz'
    guessed_pass = seed


    pass_guessed = False
    while(not pass_guessed):
        guesses_dict = {}

        for char in possible_chars:
            start_time = time.time()
            pass_guessed = check_creds("tanya", guessed_pass + char)
            if(pass_guessed):
                return guessed_pass + char
            duration = time.time() - start_time
            guesses_dict[char] = duration

        guesses_dict = dict(sorted(guesses_dict.items(), key=lambda x: (x[1], x[0]), reverse=True))
        guessed_pass = guessed_pass + list(guesses_dict.keys())[0]
    
    return guessed_pass

def main():
    # set_creds()

    start_time = time.time()
    print(brute_force())
    print(time.time() - start_time)
          

main()