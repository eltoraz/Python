"""
Program:     cipher.py
Author:      Bill Jameson (jamesw2@rpi.edu)
Description: Encrypts and decrypts alphanumeric strings using two different ciphers,
             and performs character/word frequency analysis on a string
"""

import random
import math

def subCipherEncrypt(S, key):
    """Encrypts string S using a substitution cipher based on key"""
    if not len(key) == 26:
        print("Substitution key must be exactly 26 characters")
        exit()

    cipher = ''

    for char in S:
        if not char.isalpha():      # don't change non-alpha characters
            cipher += char
        else:
            if char.isupper():
                cipher += key[ord(char)-65].upper()
            else:
                cipher += key[ord(char)-97]

    return cipher

def subCipherDecrypt(S, key):
    """Decrypts string S using the substitution cipher provided in key"""
    if not len(key) == 26:
        print("Substitution key must be exactly 26 characters")
        exit()

    message = ''

    for char in S:
        if not char.isalpha():
            message += char
        else:
            if char.isupper():
                message += chr(key.find(char.lower())+65)
            else:
                message += chr(key.find(char)+97)

    return message

def generateCipherKey(passcode = ''):
    """Generate a 26-character alphabetic string to be used in a substitution cipher"""
    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    key = ''                        # deduplicated passcode
    for char in passcode:           # in addition to removing duplicate letters, also remove the letters
        if key.find(char) == -1:    #   from the set of letters that are to be randomized later
            key += char.lower()
            pos = alphabet.find(char.lower())
            alphabet = alphabet[:pos] + alphabet[(pos+1):]

    for i in range(len(alphabet)):  # randomize the order of the remaining letters
        pos = random.randrange(len(alphabet))
        key += alphabet[pos]
        alphabet = alphabet[:pos] + alphabet[(pos+1):]

    return key

def transposeEvenOdd(S):
    """Transcode the input string S by splitting it into 2 substrings by even/odd indices and concatenating them"""
    even = ''
    odd = ''

    for i in range(len(S)):
        if i % 2 == 0:
            even += S[i]
        else:
            odd += S[i]

    result = even + odd
    return result

def untransposeEvenOdd(S):
    """Decrypts a string encrypted by concatenating the subtring formed from its odd-indexed characters to that
    from its even-indexed characters"""
    even = S[:(math.ceil(len(S)/2))]    # divide the input string, deciding the index to split at based on its length
    odd = S[(math.ceil(len(S)/2)):]
    
    result = ''
    for i in range(len(S)):
        if i % 2 == 0:
            result += even[i//2]
        else:
            result += odd[i//2]

    return result
