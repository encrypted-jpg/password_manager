from random import randint
import getpass
import os
import pickle
from twilio.rest import Client
import time
from cryptography.fernet import Fernet

class password():
    def __init__(self):
        self.storage = []
    def store_passwords(self,service,password):
        key = generate()
        encrypted = encrypt(key, password)
        self.storage.append([service,encrypted,key])
    def show_services(self):
        print("All Services: ")
        for x in self.storage:
            print(x[0])
    def show_services_passwords(self):
        print("All Services along with those passwords: ")
        for x in self.storage:
            y = decrypt(x[2], x[1]).decode()
            print(x[0]+': '+y)
    def change_passwords(self,service,password,x):
        key = generate()
        encrypted = encrypt(key, password)
        self.storage[x][1] = encrypted
    def delete(self,x):
        self.storage.pop(x)
    def save(self):
        pickle_out = open("password.jpeg","wb")
        pickle.dump(self.storage,pickle_out)
    
    def load(self):
        if os.path.isfile('password.jpeg'):
            pickle_in = open("password.jpeg","rb")
            self.storage = pickle.load(pickle_in)
        else:
            print("No Passwords Found...")


def encrypt(key,message):
    f = Fernet(key)
    encrypted = f.encrypt(message.encode())
    return encrypted

def generate():
    return Fernet.generate_key()
        
def decrypt(key,pass_hash):
    f = Fernet(key)
    decrypted = f.decrypt(pass_hash)
    return decrypted
    
p = password()

def passgen():
    global p
    service = input('Enter Service: ')
    while True:
        try:
            n = int(input('Enter the number of digit in the password: '))
        except:
            print("Invalid Input!! Please Try Again..")
        else:
            break
    alpha = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_=+,./;}[]{:<>?'
    lst = list(alpha)
    l=0
    while l==0:
        pas = []
        for x in range(n):
        	pas.append(lst[randint(0,len(lst)-1)])
        password = ''.join(pas)
        print('Password: '+password)
        k = input("Enter 'a' to generate another password or any other letter to use the above password: ").lower()
        if k=='a':
            pass
        else:
            l=1       
    p.store_passwords(service,password)    
    
def addpass():
    global p
    service = input('Enter Service: ')
    password = input('Enter Password: ')
    p.store_passwords(service,password)
    print("Password Added")

def delete_pass():
    global p
    service = input('Enter Service: ')
    q=0
    for x in range(len(p.storage)):
        if p.storage[x][0]==service:
            print("Password: "+(decrypt(p.storage[x][2],p.storage[x][1])).decode())
            p.delete(x)
            print("Password Deleted Successfully..")
            q+=1
            break
    if q==0:
        print("Service Not Found..")

def change_pass():
    global p
    service = input('Enter Service: ')
    q=0
    for x in range(len(p.storage)):
        if p.storage[x][0]==service:
            print("Previous Password: "+(decrypt(p.storage[x][2],p.storage[x][1])).decode())
            password = input('Enter New Password: ')
            p.change_passwords(service,password,x)
            print("Password Changed Successfully..")
            q+=1
    if q==0:
        print("Service Not Found..")
    
    
def take_input():
    global p
    while True:
        try:
            i=0
            print("\n1.Add Password\n2.Get Password\n3.Change Password\n4.List all Services\n5.List all Services and Passwords\n6.Delete Password\n7.Quit")
            i = int(input('Enter here: '))
        except:
            print("Invalid Input!! Please Try Again..")
        else:
            pass
        if i==1:
            addpass()
        elif i==2:
            passgen()
        elif i==3:
            change_pass()
        elif i==4:
            p.show_services()
        elif i==5:
            p.show_services_passwords()
        elif i==6:
            delete_pass()
        elif i==7:
            os.system('cls')
            break
        else:
            print("Invalid Input!! Please Try Again..")

k=0
b=0
p.load()
while k>=0:    
    master = getpass.getpass(prompt = 'Enter Master Password: ')
    if master == "Master":  # You can change your master password here
        k=-1
        b=0
        take_input()
    else:
        print("Wrong Passowrd")
        k+=1
        if k>2:
            k=-1
            b=1
        else:
            pass

while b==1:
    print("You have only two attempts to answer the following security question..")
    g=0
    while g<2:
        print(f'Attempt {g+1}')
        sec = input("What is your favourite book? : ").lower()
        if sec=='encyclopedia': ## You can change this security question...
            take_input()
            g=3
            b=0
            break
        else:
            g+=1
    if g==2:
        print("Authorization Failed..")
        b=0
p.save()