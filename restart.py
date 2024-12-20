from lib.key import *

if __name__ == "__main__":
    key = JsonEncryptor("./saves/open.rng")
    key.encrypt_dict_to_file({"item" : {}},"./saves/item.rng")