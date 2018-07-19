#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import urllib2

def decode(file):
	try:
		with open(file, "r") as input_text:
			x = input_text.read()
			with open("Decoded.txt", "a") as output_text:
				content = urllib2.unquote(x)
				output_text.write(content)
		
		input_text.close()
		output_text.close()
	except:
		print "Error Occurred"

def encode(file):
	try:
		with open(file, "r") as input_text:
			x = input_text.read()
			with open("Encoded.txt", "a") as output_text:
				content = urllib2.quote(x)
				output_text.write(content)
		
		input_text.close()
		output_text.close()
	except:
		print "Error Occurred"

def main(choice, filename):
	if choice == "1":
		decode(filename)
	elif choice == "2":
		encode(filename)
	else:
		print "Unknown operation"

if __name__ == '__main__':
	chioce = raw_input("Enter 1 to Decode\nEnter 2 to Encode > ")
	filename = raw_input("Enter Filename > ")
	main(chioce, filename)