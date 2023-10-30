#!/usr/bin/env python3

from Crypto.Util.number import getPrime, bytes_to_long
import random

def customSignature():
    a = bytes_to_long(input('Your signature: ').encode())
    b = bytes_to_long(input('Confirm your signature: ').encode())
    print('Signature:', generateSigneture(a, b))

def flagSignature():
    flag = bytes_to_long(open('flag.txt').read().strip().encode())
    print('Flag:', generateSigneture(flag, flag))
    
def generateSigneture(a, b):
    global p, q, d, n, i
    s1 = pow(a, d%p, p)
    s2 = pow(b, d%q, q)
    return s2 + q * ((i * (s1 - s2)) % p)

def gcd(a, b):
    while b != 0:
        x = a
        y = b
        a = y
        b = x % y
    return a

def extendedGcd(a, b):
    if (a == 0):
        return (b, 0, 1)
    else:
        x, y, z = extendedGcd(b % a, a)
        return (x, z - (b // a) * y, y)

def generate():
    global p, q, d, n, i, e
    p = getPrime(1500)
    q = getPrime(1500)
    while (gcd(p, q) != 1):
        q = getPrime(1500)
    n = p * q
    d = random.randint(50000, 52000)
    t = (p-1) * (q-1)
    if (gcd(d, t) == 1):
        e = extendedGcd(d, t)[1]
    else:
        e = -1
    while (gcd(d, t) != 1 or e < 1):
        d  = random.randint(50000, 52000)
        e = extendedGcd(d, t)[1]
    i = extendedGcd(q, p)[1]
    
def printMenu():
    print('1. Generate signature')
    print('2. Get flag signature')
    print('3. Exit')

def welcome():
    print('Please wait...')
    generate()
    print('Welcome!')
    global n
    print('This is your N:', n)

def main():
    welcome()
    try:
        while True:
            printMenu()
            choice = int(input('> '))
            if (choice == 1):
                customSignature()
            if (choice == 2):
                flagSignature()
            if (choice == 3):
                print('Bye.')
                break
    except:
        print('An error occured.')
        exit(0)
    exit(0)

if __name__ == '__main__':
    main()
