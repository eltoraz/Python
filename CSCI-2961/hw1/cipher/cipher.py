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
    # verify validity of key, both length and contents (i.e., all 26 letters)
    if not len(key) == 26:
        print("Error: Substitution key must be exactly 26 characters")
        return -1
    for i in range(26):
        if key.find(chr(i+97)) == -1:
            print("Error: Substitution key must contain all 26 letters in lowercase. Missing: " + chr(i+97))
            return -2

    cipher = ''

    for char in S:
        if not char.isalpha():      # don't change non-alpha characters
            cipher += char
        else:
            if char.isupper():      # insert the corresponding key character
                cipher += key[ord(char)-65].upper()
            else:
                cipher += key[ord(char)-97]

    return cipher

def subCipherDecrypt(S, key):
    """Decrypts string S using the substitution cipher provided in key"""
    # verify validity of key, both length and contents (i.e., all 26 letters)
    if not len(key) == 26:
        print("Error: Substitution key must be exactly 26 characters")
        return -1
    for i in range(26):
        if key.find(chr(i+97)) == -1:
            print("Error: Substitution key must contain all 26 letters in lowercase. Missing: " + chr(i+97))
            return -2

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

    # Original submission: for a non-empty passcode, the remaining characters were randomized
    # Resubmission:        if a passcode is specified, the remaining characters are added in order
    if not passcode == '':
        key += alphabet
    else:
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
    """Decrypt a string encrypted by concatenating the subtring formed from its odd-indexed characters to that
    from its even-indexed characters"""
    even = S[:(math.ceil(len(S)/2))]    # divide the input string, deciding the index to split at based on its length
    odd = S[(math.ceil(len(S)/2)):]     # note: the length of the even substr will always be equal to or 1 greater than the odd
    
    result = ''
    for i in range(len(S)):
        if i % 2 == 0:
            result += even[i//2]
        else:
            result += odd[i//2]

    return result

def transpose(S, n = 2):
    """Transcode the input string S by splitting it into n substrings based on (index % n) and then concatenating them"""
    substrings = []                     # list of substrings
    for i in range(n):
        substrings.append('')

    for i in range(len(S)):             # separate the characters into substrings based on their index modulo the number of substrings to use
        substrings[i%n] += S[i]

    result = ''                         # concatenate the substrings together to form the cipher
    for i in range(n):
        result += substrings[i]

    return result

def untranspose(S, n = 2):
    """Decrypt a transposition cipher S by splitting it up into n substrings and interleave them"""
    remainder = len(S) % n              # number of substrings that have an extra element (for ciphers where len(S) is not a multiple of n)
    code = S                            # scratch copy of cipher
    substrings = []
    m = n

    for i in range(m):                  # separate the substrings
        substrings.append(code[:math.ceil(len(code)/m)])
        code = code[math.ceil(len(code)/m):]
        m -= 1

    result = ''
    for i in range(len(S)):             # decrypt the cipher by interleaving the substrings
        result += substrings[i%n][0]
        substrings[i%n] = substrings[i%n][1:]

    return result

def letterFrequency(S):
    """Calculate the frequency of each letter (case insensitive) that appears in input string S"""
    count = 0                           # tally of number of letters encountered
    letters = {}                        # dictionary matching individual letters to their tallies

    for i in range(26):                 # initialize all entries in the dictionary to 0
        letters[chr(i+97)] = 0

    for char in S:                      # examine each character, but only count the letters (disregarding case)
        if char.isalpha():
            letters[char.lower()] += 1
            count += 1

    # print out the letters and their frequency relative to the other letters
    print("total letters: " + str(count))
    for i in range(len(letters)):
        if count == 0:
            print(chr(i+97) + ": 0.0")
        else:
            print(chr(i+97) + ": " + str(letters[chr(i+97)] / count))

def wordFrequency(S):
    """Calculate the frequency of each word (case insensitive, deliminated by any non-alphabetic character) in S"""
    count = 0                           # number of words encountered
    words = {}
    w = ''

    for char in S:                      # build each word character-by-character
        if char.isalpha():
            w += char.lower()
        else:                           # if not an alphabetic character, tally the word (or skip if multiple sequential non-alpha characters)
            if not w == '':             # note: does not catch contractions and hyphenated words
                count += 1
                if w in words:
                    words[w] += 1
                else:
                    words[w] = 1
                w = ''
    if not w == '':                     # catch words at the very end of the input strings
        count += 1
        if w in words:
            words[w] += 1
        else:
            words[w] = 1
        w = ''

    # print out the words and their relative frequencies
    print("total words: " + str(count))
    for (key, value) in words.items():
        if count == 0:
            print(key + ": 0.0")
        else:
            print(key + ": " + str(value/count))
