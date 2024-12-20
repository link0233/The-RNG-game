import json
from cryptography.fernet import Fernet

class JsonEncryptor:
    def __init__(self, key_file='key.key'):
        self.key_file = key_file
        self.key = None
        self.load_or_generate_key()

    def load_or_generate_key(self):
        """加載現有密鑰或生成新密鑰"""
        try:
            with open(self.key_file, 'rb') as file:
                self.key = file.read()
        except FileNotFoundError:
            self.key = Fernet.generate_key()
            with open(self.key_file, 'wb') as file:
                file.write(self.key)

    def new_key(self):
        self.key = Fernet.generate_key()
        with open(self.key_file, 'wb') as file:
            file.write(self.key)

    def encrypt_dict_to_file(self, data_dict, file_name):
        """將字典加密並存儲為指定文件"""
        fernet = Fernet(self.key)
        json_data = json.dumps(data_dict)
        encrypted_data = fernet.encrypt(json_data.encode('utf-8'))
        with open(file_name, 'wb') as file:
            file.write(encrypted_data)

    def decrypt_file_to_dict(self, file_name):
        """解密文件並還原為字典"""
        fernet = Fernet(self.key)
        with open(file_name, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = fernet.decrypt(encrypted_data).decode('utf-8')
        return json.loads(decrypted_data)