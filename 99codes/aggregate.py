#!/usr/bin/env python3
"""
author: Bill Jameson (jamesw2@rpi.edu)
99codes aggregator: aggregate info on XBLA Minecraft codes different people get from 99codes.mojang.com
"""

import os
import sys

def incorporate_info(current_code, new_info):
    assert len(current_code) == len(new_info), 'code length mismatch'

    new_code = ''

    for i in range(len(current_code)):
        if current_code[i] == '?':
            new_code += new_info[i]
        else:
            new_code += current_code[i]

    return new_code

def aggregate(codedir='codes/'):
    filelist = [file for file in os.listdir(codedir)]
    codelist = ['?????-?????-?????-?????-?????' for i in range(99)]

    for f in filelist:
        contents = open(codedir + f).read()
        codefrags = contents.split()

        assert len(codefrags) == 99, 'series ' + f + ' doesn\' have enough codes'

        for i in range(99):
            try:
                codelist[i] = incorporate_info(codelist[i], codefrags[i])
            except AssertionError as e:
                print('error in series ' + f + ': ' + e.args[0], file=sys.stderr)
                exit(1)

    codescompleted = 0
    for c in codelist:
        if c.find('?') == -1:
            print(c)
            codescompleted += 1

    aggregate_info = open('aggregate_info.txt', mode='w')
    aggregate_info.write('\n'.join(codelist))
    aggregate_info.close()

def main():
    print('aggregating codes...')
    aggregate()

if __name__ == '__main__':
    main()

