from lib.key import *

if __name__ == "__main__":
    key = JsonEncryptor("./saves/key.key")
    key.encrypt_dict_to_file({"item" : {}},"./saves/item.json")