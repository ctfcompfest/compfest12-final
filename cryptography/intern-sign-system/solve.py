#!/usr/bin/env python3
from pwn import *
from Crypto.Util.number import long_to_bytes, inverse
import timeit

start = timeit.default_timer()

def gcd(a, b):
    while b != 0:
        x = a
        y = b
        a = y
        b = x % y
    return a

def getN():
    return int(p.recvuntil('> ').split(b'\n')[2][16:].decode())

def getFlag():
    p.sendline(b'2')
    return int(p.recvuntil('> ').split(b'\n')[0][6:].decode())

def getSignature(a, b):
    a = str(a).encode()
    b = str(b).encode()
    p.sendline(b'1')
    p.recvuntil(b'Your signature: ')
    p.sendline(a)
    p.recvuntil(b'Confirm your signature: ')
    p.sendline(b)
    return int(p.recvuntil(b'> ').split(b'\n')[0][11:].decode())

p = process('./prob.py') #remote('103.136.18.212', 3000)
n = getN()
flag = getFlag()
s = getSignature(5, 5)
s1 = getSignature(6, 5)
q = gcd(s1-s,n)
p.close()

t = (q-1) * (n//q - 1)

e_list = []
for d in range(50000, 52000):
    if (gcd(d, t) == 1):
        e_list.append(inverse(d, t))

print('Possibilities of e:', len(e_list))
cnt = 0
for e in e_list:
    cnt += 1
    if (cnt % 100 == 0):
        print('Checking e[' + str(cnt) + '], elapsed time: {:.2f}s'.format(timeit.default_timer() - start))
    try:
        possible = long_to_bytes(pow(flag,e,n)).decode()
        print(cnt, 'Possible flag:', possible)
    except:
        pass
        
stop = timeit.default_timer()
print('Finished in {:.2f}s'.format(stop - start))
