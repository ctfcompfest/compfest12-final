import requests
import base64
import timeit

START = timeit.default_timer()

# tes untuk mencari panjang username dan password dari panjang enc aes nya
# dari tes di bawah ini, terlihat bahwa panjang valid_password adalah 40
# karena bagian aes berubah dari 48 menjadi 64 saat panjang input == 8
# sementara panjang valid username adalah 3 karena bagian aes berubah dari 16 menjadi 32 saat panjang input == 13
URL = 'http://0.0.0.0:5000/validate'
for i in range(20):
    payload = {
        "username":"a"*i,
        "password":"a"*i
    }
    sess = requests.Session()
    r = sess.post(URL, payload)
    username = sess.cookies["session_username"]
    aes_part_username = base64.b64decode(username)[58:]
    password = sess.cookies["session_password"]
    aes_part_password = base64.b64decode(password)[58:]
    print('panjang payload: {:d}, panjang enc(input_username+valid_username): {:d}, panjang enc(input_password+valid_password): {:d}'.format(i, len(aes_part_username), len(aes_part_password)))

# preparasi oracle padding attack
URL = 'http://0.0.0.0:5000/validate'
payload = {
    "username":"a",
    "password":"a"
}
sess = requests.Session()
r = sess.post(URL, payload)
username = sess.cookies["session_username"]
password = sess.cookies["session_password"]
URL = 'http://0.0.0.0:5000/'

# mencari username
iv_part = base64.b64decode(username)[:58]
aes_part = base64.b64decode(username)[58:]

known = iv_part[4:20]
enc_user = aes_part

new_known = [0 for i in range(4)]
for i in range(4,16):
    new_known.append(12)
i = 3
cnt = 0
while (i >= 0):
    now = known[:i+1]
    for j in range(i+1, 16):
        now += bytearray([known[j] ^ new_known[j] ^ (16-i)])
    for j in range(256):
        forged = now[:i] + bytearray([now[i] ^ j]) + now[i+1:]
        new_cookie = base64.b64encode(iv_part + forged + enc_user).decode()
        cookies = {'session_username': new_cookie, 'session_password': password}
        r = requests.get(URL, cookies=cookies)
        cnt += 1
        if (b'padded' not in r.content):
            new_known[i] = j^(16-i)
            break
    i -= 1
username = bytearray(new_known)[:4].decode()
print('user:', username[1:])
print("jumlah requests:", cnt)

# mencari password (flag)
iv_part = base64.b64decode(password)[:58]
aes_part = base64.b64decode(password)[58:]
block = iv_part[4:20] + aes_part
flag = b''
cnt = 0
for block_num in range(3,0,-1):
    dec_block = block[16*block_num : 16*(block_num+1)]
    xor_block = block[16*(block_num - 1) : 16*block_num]
    if (block_num == 3):
        new_known = [0 for i in range(9)]
        for _ in range(7):
            new_known.append(7)
        i = 8
    else:
        new_known = [0 for i in range(16)]
        i = 15
    
    while (i >= 0):
        now = xor_block[:i+1]
        for j in range(i+1, 16):
            now += bytearray([xor_block[j] ^ new_known[j] ^ (16-i)])
        for j in range(256):
            forged = block[16:16*(block_num-1)] + now[:i] + bytearray([now[i] ^ j]) + now[i+1:]
            new_cookie = base64.b64encode(iv_part + forged + dec_block).decode()
            cookies = {'session_username': username, 'session_password': new_cookie}
            r = requests.get(URL, cookies=cookies)
            cnt += 1
            if (b'padded' not in r.content):
                new_known[i] = j^(16-i)
                break
        i -= 1
    flag = bytearray(new_known) + flag
    
flag = flag[1:-7].decode()
print('password: ' + flag)
print("jumlah requests:", cnt)
print('flag: COMPFEST12{' + flag + '}')

STOP = timeit.default_timer()
print('Finished in {:.2f}s'.format(STOP - START))
