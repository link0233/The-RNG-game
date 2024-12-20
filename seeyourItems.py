from lib.key import *

key = JsonEncryptor("./saves/key.key")
print(key.decrypt_file_to_dict("./saves/item.json"))
input()