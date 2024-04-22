import os
import re
import bcrypt
import base64
import mysql.connector
import tkinter.messagebox as messagebox
from AES256test import *
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


# function to login
def login(username, password):

    # Connect to the database
    cnx = mysql.connector.connect(user='root', password="#!y%f76$v33aXU", #os.environ.get('MYSQL_PASSWORD')
                                  host='localhost', database='account_info') 

    # Create a cursor object
    cursor = cnx.cursor()

    try:
        # Retrieve the encrypted password, salt, and IV from the master_account table
        query = "SELECT accountnum, password, salt, iv FROM master_account WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result is None:
            return {"message": "Invalid username."}, 400
        else:
            # Decode the salt and IV
            id = result[0]
            salt = base64.b64decode(result[2])
            iv = base64.b64decode(result[3])

            # Derive the key from the password and salt
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            key = kdf.derive(password.encode('utf-8'))

            # Decrypt the password with AES256
            decrypted_password = AES_decrypt(result[1], key, iv)

            # Verify the user's plaintext password against the decrypted, hashed password with bcrypt
            compare = bcrypt.checkpw(password.encode('utf-8'), decrypted_password.encode('utf-8'))

            # If the passwords match, retrieve the stored accounts for the user
            if compare:
                query = "SELECT accountnum, username, password, websiteURL FROM stored_accounts WHERE master_accountnum = %s"
                cursor.execute(query, (id,))
                results = cursor.fetchall()

            # Decrypt each stored account password with AES256
            stored_accounts = []
            for row in results:
                try:
                    accountum = row[0]
                    decrypted_stored_username = AES_decrypt(row[1], key, iv) if row[1] is not None else None
                    decrypted_stored_password = AES_decrypt(row[2], key, iv) if row[2] is not None else None
                    decrypted_stored_email = AES_decrypt(row[3], key, iv) if row[3] is not None else None
                    stored_accounts.append({"accountnum": accountum, "username": decrypted_stored_username, "password": decrypted_stored_password, "email": decrypted_stored_email})
                except ValueError:
                    print(f"Error: Could not decrypt password for {row[1]}. The password may be corrupted or the wrong key or IV may have been used.")
            if compare:
                return {"message": "Password is correct", "stored_accounts": stored_accounts, "key": key, "iv": iv, "id": id}, 200
            else:
                return {"message": "Password is incorrect"}, 400
    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
        return {"message": "An error occurred while retrieving the account information."}, 500

def get_stored_accounts(key, iv, id):
    cnx = mysql.connector.connect(user='root', password="#!y%f76$v33aXU",
                                   host='localhost', database='account_info')

    # Create a cursor object
    cursor = cnx.cursor()

    # Fetch the stored accounts for the given id from the stored_accounts table
    query = "SELECT accountnum, username, password, websiteURL FROM stored_accounts WHERE master_accountnum = %s"
    cursor.execute(query, (id,))

    # Decrypt the stored accounts and add them to a list
    stored_accounts = []
    for (accountnum, username, password, email) in cursor:
        decrypted_username = AES_decrypt(username, key, iv) if username is not None else None
        decrypted_password = AES_decrypt(password, key, iv) if password is not None else None
        decrypted_email = AES_decrypt(email, key, iv) if email is not None else None
        account = {"accountnum": accountnum, "username": decrypted_username, "password": decrypted_password, "email": decrypted_email}
        #print(account)  # Print the account to debug
        stored_accounts.append(account)

    return stored_accounts

# function to add a new account
def add_new_account(new_username, new_password, new_email, key, iv, id, add_account_window):
    cnx = mysql.connector.connect(user='root', password="#!y%f76$v33aXU",#os.environ.get('MYSQL_PASSWORD'),
                                  host='localhost', database='account_info')

    # Create a cursor object
    cursor = cnx.cursor()

    # Use the provided key and IV to encrypt the new password
    encrypted_new_username = AES_encrypt(new_username, key, iv)
    encrypted_new_password = AES_encrypt(new_password, key, iv)
    encrypted_new_email = AES_encrypt(new_email, key, iv)

    # Insert the new stored account into the stored_accounts table
    query = "INSERT INTO stored_accounts (username, password, websiteURL, master_accountnum) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (encrypted_new_username, encrypted_new_password, encrypted_new_email, id))

    # Commit the transaction
    cnx.commit()

    add_account_window.destroy()

    return {"message": "Stored account created successfully."}, 200

def edit_account(new_username, new_password, new_email, key, iv, id, accountnum, edit_account_window):
    cnx = mysql.connector.connect(user='root', password="#!y%f76$v33aXU",
                                  host='localhost', database='account_info')

    # Create a cursor object
    cursor = cnx.cursor()

    # Use the provided key and IV to encrypt the new password
    encrypted_new_username = AES_encrypt(new_username, key, iv)
    encrypted_new_password = AES_encrypt(new_password, key, iv)
    encrypted_new_email = AES_encrypt(new_email, key, iv)

    # Update the stored account into the stored_accounts table
    query = "UPDATE stored_accounts SET username = %s, password = %s, websiteURL = %s WHERE accountnum = %s AND master_accountnum = %s"    
    cursor.execute(query, (encrypted_new_username, encrypted_new_password, encrypted_new_email, accountnum, id))

    # Commit the transaction
    cnx.commit()

    edit_account_window.destroy()

    return {"message": "Stored account updated successfully."}, 200

def delete_account(accountnum):
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this account?")
    if confirm:
        cnx = mysql.connector.connect(user='root', password="#!y%f76$v33aXU", 
                                  host='localhost', database='account_info')

        # Create a cursor object
        cursor = cnx.cursor()

        # Create the SQL DELETE query
        query = "DELETE FROM stored_accounts WHERE accountnum = %s"

        # Execute the SQL DELETE query
        cursor.execute(query, (accountnum,))

        # Commit the changes
        cnx.commit()

def delete_null_rows():
    cnx = mysql.connector.connect(user='root', password="#!y%f76$v33aXU", host='localhost', database='account_info')

    # Create a cursor object
    cursor = cnx.cursor()

    # Create the SQL DELETE query
    query = "DELETE FROM stored_accounts WHERE username IS NULL AND password IS NULL AND accountnum IS NULL AND master_accountnum IS NULL AND websiteURL IS NULL"

    # Execute the SQL DELETE query
    cursor.execute(query)

    # Commit the changes
    cnx.commit()

    print("Null rows deleted.")


def register(password, username, register_window):
    
    # Check if the username or password is empty
    if not username or not password:
        messagebox.showerror("Registration Error", "Username or password cannot be empty.")
        return
   
    # Connect to the database
    cnx = mysql.connector.connect(user='root', password='#!y%f76$v33aXU',
                              host='localhost', database='account_info')

    # Create a cursor object
    cursor = cnx.cursor()

    # Check if the username already exists in the master_account table
    query = "SELECT * FROM master_account WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    if result is not None:
        messagebox.showerror("Registration Error", "Username already in use.")
    else:
        # Check the strength of the password
        if len(password) < 8 or not re.search("[a-z]", password) or not re.search("[A-Z]", password) or not re.search("[0-9]", password):
            messagebox.showerror("Registration Error", "Password is not strong enough.")
        else:
            # Hash the password with bcrypt
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            # Generate an IV
            iv = os.urandom(16)
            encoded_iv = base64.b64encode(iv).decode('utf-8')
            # Encode the salt to a string
            encoded_salt = base64.b64encode(salt).decode('utf-8')

            # Derive a key from the password and salt
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            key = kdf.derive(password.encode('utf-8'))

            # Encrypt the hashed password with AES256
            encrypted_password = AES_encrypt(hashed_password, key, iv)

            # Store the encrypted, hashed password, the IV, and the salt in the master_account table
            query = "INSERT INTO master_account (username, password, iv, salt) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (username, encrypted_password, encoded_iv, encoded_salt))
            cnx.commit()

            register_window.destroy()
