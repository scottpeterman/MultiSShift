import os
import yaml
from cryptography.fernet import Fernet

def cryptonomicon(to_decrypt, key_path="./crypto.key"):
    from cryptography.fernet import Fernet

    try:
        fhc = open(key_path, "r")
        key = fhc.read()
        key = key.strip()
        cryptonizer = Fernet(key)

        to_decrypt = bytes(to_decrypt, 'utf-8')
        result = cryptonizer.decrypt(to_decrypt)

        return result.decode("utf-8")
    except Exception as e:
        print("error processing crypto key file")
        raise e

def encrypt(to_encrypt):
    from cryptography.fernet import Fernet
    try:
        fhc = open("crypto.key", "r")
        key = fhc.read()
        key = key.strip()
        cryptonizer = Fernet(key)
        to_encrypt = bytes(str(to_encrypt), 'utf-8')
        result = cryptonizer.encrypt(to_encrypt)
        return result
    except Exception as e:
        print("error processing crypto key file")

def generate_key():

    # Check if the file exists
    if os.path.isfile('crypto.key'):
        # Ask the user for confirmation
        confirm = input(
            'The file "crypto.key" already exists, do you want to overwrite it? This will invalidate your currently encrypted passwords. (y/n): ')

        # Check the user's response
        if confirm.lower() != 'y':
            print('Operation cancelled.')
            exit()

    # Generate a key
    key = Fernet.generate_key()

    # Save the key to the file
    with open('crypto.key', 'wb') as file:
        file.write(key)

    print('Key saved to "crypto.key".')

def create_db():
    import sqlite3

    conn = sqlite3.connect('settings.sqlite')
    c = conn.cursor()

    c.execute('''
              CREATE TABLE "creds" (
    	"id" INTEGER NOT NULL  ,
    	"username" TEXT NULL  ,
    	"password" TEXT NULL
    , "displayname"	TEXT)
              ''')
    c.execute('''CREATE TABLE installed_plugins (
    id INTEGER PRIMARY KEY,
    name TEXT,
    package_name TEXT,
    description TEXT,
    import_name TEXT,
    status TEXT
);
''')

    conn.commit()
    print("settings.sqlite created")

def create_session_file(file_path="./sessions/sessions.yaml"):
    if not os.path.exists(file_path):
        os.makedirs('./sessions', exist_ok=True)

        # Define the default content
        default_content = [
            {
                "folder_name": "0 - Linux",
                "sessions": [
                    {
                        "DeviceType": "Linux",
                        "Model": "NUC",
                        "SerialNumber": "",
                        "SoftwareVersion": "22.04",
                        "Vendor": "Ubuntu",
                        "credsid": "1",
                        "display_name": "Example",
                        "host": "10.0.0.12",
                        "port": "22"
                    }
                ]
            }
        ]

        # Create the file with the default content
        with open(file_path, 'w') as file:
            yaml.safe_dump(default_content, file)


def create_sftp_key():
    test_private_key = '''-----BEGIN OPENSSH PRIVATE KEY-----
    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
    -----END OPENSSH PRIVATE KEY-----
    '''

    test_public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC21lgBAFAJvKzwi37YYCtdNf1nIMhuifMBBJkF6ZO2Y3rk1g8RATCgR2+poEEdLr7kIVCedsQUxuSPy6aSNJ7F1d7E/Q+Do3LwgvGTI3nZmoTPUYwGFr5eTrR2cBsmmI8woRM+Hb4i8t3AZwgMPA/tobRkXNXvqZCBPhdf3SdCzjfliW7qAYkexADwlCA9mi2btowbHZMKBHlueP1H7uiRm72nDqqpQvKyQBKIuz3bBKGcXuF7Vvv4lB4XnieDQ8UZjYhHQ0BW21HnxeEeVOk+3Qkql3/+RvIcCU0Y/vjeLNHz5v25YP9Ns/eaeD69CRVoYXC2lsqxa3si8y88eKPD1AtzXPVjj9VKBE0gcjOJyWwokGouelNOppMx3RonPykca1BYgmp8dzWFSc9Q21elvJi1nbDkMRx+7h/E0t/bHvK4gCc/jLAIYiElzaV8Yk6OTXhGL8uiJyCfROaIZsmuHSt8ul9gh6V6dQEJ2ox+cCbH6Gkysl/1MJvSHv8kOnU= columbia\97685@USR-SUMMER-64"
    with open("./test_rsa.key.pub", 'w') as file:
        file.write(test_public_key)
    with open("./test_rsa.key", 'w') as file:
        file.write(test_private_key)

def create_settings():
    content = '''defaults:
  host: "10.0.0.1"
  port: 22
  username: "username"
  key_path: "C:/Users/user/.ssh/id_rsa"
  theme: "dark"  # or "light"'''
    fh = open("settings.yaml", "w")
    fh.write(yaml.safe_dump(content))
    fh.close()
