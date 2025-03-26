import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from flask import Flask,render_template,request
from Crypto.Util.number import bytes_to_long,long_to_bytes
import AES_encrypt
import base64

app=Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt',methods=['POST'])
def encrypt():
    key=long_to_bytes(int(request.form.get('key')))
    image = request.files['image']
    image.save(f"./uploads/{image.filename}")
    iv=get_random_bytes(16)
    AES_encrypt.encrypt_image(f"./uploads/{image.filename}",key,f"./uploads/en{image.filename}",iv)
    with open(f"./uploads/en{image.filename}",'rb') as image_file:
        img_data=image_file.read()
    base64_str = base64.b64encode(img_data).decode('utf-8')
    return {'image':str(base64_str)}

@app.route('/decrypt',methods=['POST'])
def decrypt():
    key=long_to_bytes(int(request.form.get('key')))
    image = request.files['image']
    image.save(f"./uploads/{image.filename}")
    iv=get_random_bytes(16)
    AES_encrypt.decrypt_image(f"./uploads/{image.filename}",key,f"./uploads/de{image.filename}")
    with open(f"./uploads/de{image.filename}",'rb') as image_file:
        img_data=image_file.read()
    base64_str = base64.b64encode(img_data).decode('utf-8')
    return {'image':str(base64_str)}

@app.route('/key',methods=['POST'])
def get_key():
    key=bytes_to_long(get_random_bytes(16))
    str1=str(key)
    print(key)
    return {'key':str1},200

if __name__=='__main__': 
    app.run(port=5000)