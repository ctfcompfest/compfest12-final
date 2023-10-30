from Crypto.Cipher import AES
from flask import Flask, request, render_template, make_response, url_for
import base64
import os
import random

valid_username = 'you'
passwordfile = open('pass.txt')
valid_password = passwordfile.read().strip()
passwordfile.close()
keyfile = open('key.txt')
key = keyfile.read().strip().encode()
keyfile.close()

app = Flask(__name__)

def encrypt(msg, category):
    iv = []
    for i in range(16):
        iv.append(random.randint(0, 255))
    iv = bytearray(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    msg = msg.encode()
    msg += chr(16 - len(msg)%16).encode() * (16 - len(msg)%16)
    return base64.b64encode(b'iv: ' + iv + b', enc(input_' + category.encode() + b'+valid_' + category.encode() + b'): ' + cipher.encrypt(msg)).decode()
    
def decrypt(msg, category):
    msg = base64.b64decode(msg)
    iv = msg[4:20]
    if (len(iv) != 16):
        return 'Your iv for ' + category + ' is not matched with the required length!'
    enc = msg[20:].replace(b', enc(input_' + category.encode() + b'+valid_' + category.encode() + b'): ', b'')
    if (len(enc) % 16 != 0):
        return 'Your encrypted ' + category + ' is not matched with the required length!'
    cipher = AES.new(key, AES.MODE_CBC ,iv)
    dec = cipher.decrypt(enc)
    unpadded = dec[:-dec[-1]]
    padding = dec[-dec[-1]:]
    if (len(padding) == 0):
        return 'Your ' + category + ' is not properly padded!'
    tmp = -1
    for pad in padding:
        if (tmp == -1):
            tmp = pad
        else:
            if (tmp != pad):
                return 'Your ' + category + ' is not properly padded!'
    if (category == 'username'):
        if (unpadded[:-len(valid_username)]!= valid_username.encode()):
            return 'Your ' + category + ' is wrong!'
    if (category == 'password'):
        if (unpadded[:-len(valid_password)] != valid_password.encode()):
            return 'Your ' + category + ' is wrong!'
    return 'Success'

@app.route('/')
def index():
    if ('error' in request.cookies.keys()):
        return render_template('index.html', message='Please input your credentials properly')
        
    if (('session_username' in request.cookies.keys() and 'session_password' not in request.cookies.keys()) or ('session_username' not in request.cookies.keys() and 'session_password' in request.cookies.keys())):
        return render_template('index.html', message='Please input your credentials properly!')
    if ('session_username' not in request.cookies.keys() and 'session_password' not in request.cookies.keys()):
        return render_template('index.html', message='')
    
    username = request.cookies['session_username']
    password = request.cookies['session_password']
    username_resp = decrypt(username, 'username')
    password_resp = decrypt(password, 'password')
    if (username_resp == 'Success' and password_resp == 'Success'):
        resp = make_response()
        resp.headers['location'] = url_for('success')
        return resp, 302
    if (username_resp == 'Success'):
        return render_template('index.html', message=password_resp)
    if (password_resp == 'Success'):
        return render_template('index.html', message=username_resp)
    return render_template('index.html', message=username_resp + ", " + password_resp)
    
@app.route('/25cbf8edd270309ae16cbba3780112457ab97af1')
def success():
    if (('session_username' in request.cookies.keys() and 'session_password' not in request.cookies.keys()) or ('session_username' not in request.cookies.keys() and 'session_password' in request.cookies.keys())):
        resp = make_response()
        resp.headers['location'] = url_for('index')
        return resp, 302
    if ('session_username' not in request.cookies.keys() and 'session_password' not in request.cookies.keys()):
        resp = make_response()
        resp.headers['location'] = url_for('index')
        return resp, 302
    
    username = request.cookies['session_username']
    password = request.cookies['session_password']
    username_resp = decrypt(username, 'username')
    password_resp = decrypt(password, 'password')
        
    if (username_resp != 'Success' or password_resp != 'Success'):
        resp = make_response()
        resp.headers['location'] = url_for('index')
        return resp, 302
    return render_template('success.html')
    
@app.route('/validate', methods=['POST', 'GET'])
def validate():
    if (request.method == 'POST'):
        try:
            username = request.form['username']
            password = request.form['password']
        except:
            resp = make_response()
            resp.headers['location'] = url_for('/')
            resp.set_cookie('error', '1')
            return resp, 302
        
        resp = make_response()
        resp.set_cookie('session_username', encrypt(username + valid_username, 'username'))
        resp.set_cookie('session_password', encrypt(password + valid_password, 'password'))
        resp.headers['location'] = url_for('index')
        return resp, 302
    else:
        resp = make_response()
        resp.headers['location'] = url_for('index')
        resp.set_cookie('error', '1')
        return resp, 302

if __name__ == '__main__':
    HOST = os.environ['HOST']
    PORT = int(os.environ['PORT'])
    app.run(host=HOST, port=PORT)
