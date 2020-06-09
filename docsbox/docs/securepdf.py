<<<<<<< HEAD
from PyPDF3 import PdfFileReader, PdfFileWriter
import PyPDF3
import random
import string
import os

def secure(output_path):
    input_pdf = PdfFileReader(output_path)
    output_pdf = PdfFileWriter()
    output_pdf.appendPagesFromReader(input_pdf)
    output_pdf.encrypt(user_pwd="",owner_pwd=generatePassword(),use_128bit=True,allow_printing=False)
    with open(output_path,"wb") as out_file:
        output_pdf.write(out_file)

# Method to generate random password
# generated password length is (pwd_length + 4)
def generatePassword():
    pwd_length = 6
    randomSource = string.ascii_letters + string.digits + string.punctuation
    password = random.choice(string.ascii_lowercase)
    password += random.choice(string.ascii_uppercase)
    password += random.choice(string.digits)
    password += random.choice(string.punctuation)
    for i in range(pwd_length):
        password += random.choice(randomSource)
    passwordList = list(password)
    random.SystemRandom().shuffle(passwordList)
    password = ''.join(passwordList)
    return password
