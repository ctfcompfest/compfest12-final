#!/usr/bin/env python3

from Crypto.PublicKey import ECC
from Crypto.Cipher import AES
import os, codecs, time, sys

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

class MyECIES:

	def __init__(self):
		self.P = ECC.import_key(open('P.pem','rt').read()).pointQ
		self.Q = ECC.import_key(open('Q.pem','rt').read()).pointQ
		self.G = ECC.import_key(open('G.pem','rt').read()).pointQ
		self.current_state = int.from_bytes(os.urandom(32), 'little')

	def next_random(self):
		s = self.current_state
		s = (s*self.P).x
		r = (s*self.Q).x
		s = (s*self.P).x
		self.current_state = s
		return r

	def get_shared_key(self, r, pubkey):
		return (r*self.G).x, (r*pubkey).x

	def gen_key(self):
		privkey = self.next_random()
		pubkey = privkey*self.G
		return privkey, pubkey

def pad(msg):
	val = 16 - (len(msg) % 16)
	pad_data = msg + (chr(val) * val)
	return pad_data

def send_to_alice(msg, verbose=False):
	iv = os.urandom(16)
	r = ecies.next_random();
	send_key, shared_key = ecies.get_shared_key(r, ALICE_PUB_KEY)
	if(verbose):
		print("r    = ", r)
		print("r*G  = ", send_key)
		print("r*Kb = ", shared_key)
		print("Kb   = ({}, {})".format(ALICE_PUB_KEY.x, ALICE_PUB_KEY.y))

	shared_key = shared_key.to_bytes(32)
	send_key = send_key.to_bytes(32)
	aes = AES.new(shared_key, AES.MODE_CBC, iv)
	enc = send_key + iv + aes.encrypt(codecs.encode(pad(msg)))
	return codecs.encode(enc, 'hex')

def intercept_bob_and_alice_communication():
	print("Intercepting", end='')
	for i in range(3):
		time.sleep(1)
		print(".", end='')
	time.sleep(1)
	res = send_to_alice(FLAG)
	print()
	print("Intercept successsful")
	print("Intercepted Message: ", res)

def menu():
	print("1) Send message to Alice")
	print("2) Intercept Bob and Alice communication")
	print("3) Exit")

def main():
	try:
		while True:
			menu()
			choice = int(input("Choice: "))
			if choice == 1:
				msg = input("Message to send to Alice: ")
				res = send_to_alice(msg, verbose=True)
				print("Sent to Alice: ", res)
			elif choice == 2:
				intercept_bob_and_alice_communication()
			else:
				print("Bye bye~")
				exit()
	except Exception as e:
		print(e)
		print("You broke something...")
		exit()

if __name__=='__main__':
	sys.stdout = Unbuffered(sys.stdout)
	ecies = MyECIES()
	ALICE_PRIV_KEY, ALICE_PUB_KEY = ecies.gen_key()
	FLAG = open('flag.txt', 'r').read()
	main()