#!/usr/bin/env python
# -*- coding:utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2015 Zhi-Wei Cai.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from struct import *
import sys
import os

version = '0.1'
copyright = 'Copyright (C) 2015 Zhi-Wei Cai.'

print('\nKWAD Tool v{}'.format(version))
print('{}\n'.format(copyright))

if len(sys.argv) > 1:
    try:
        COUNT_OFFSET = 0x10
        STRUCT_LEN = 0x10
        _file = open(sys.argv[1], 'rb').read()
        _count = unpack('<L', _file[0x10:0x14])[0]
        _offset = _count * STRUCT_LEN + COUNT_OFFSET + 0x4

        print("Total Files: {}".format(_count))
        print("Name Table Offset: {}\n".format(hex(_offset)))

        _lenTable = [0] * _count
        _offsetTable = [0] * _count
        _offsetOffset = COUNT_OFFSET + 0x8
        _nameTable = [''] * _count
        _nameOffset = _offset + 0x4

        print('{:>4} | {:^18} | {:^16} | {:^4} | {:^67}'.format('#', 'Offset', 'Length', 'Type', 'Path'))
        print('{:-<120}'.format(''))
        for _index in xrange(_count):
            _len = unpack('<L', _file[_nameOffset:_nameOffset+0x4])[0]
            _nameOffset += 0x4
            _name = _file[_nameOffset:_nameOffset + _len]
            _nameOffset += _len
            if _nameOffset % 0x4:
                _nameOffset += 0x4 - (_nameOffset % 0x4)
            _nameOffset += 0x4
            _nameTable[_index] = _name

            _lenTable[_index], _offsetTable[_index], _type, _ = unpack('<2L4sL', _file[_offsetOffset:_offsetOffset + STRUCT_LEN])
            print("{:4} | 0x{} | {:>16} | {:4} | {}".format(_index+1, hex(_offsetTable[_index])[2:].zfill(16), _lenTable[_index], _type, _nameTable[_index]))
            _offsetOffset += STRUCT_LEN
            _index += 1
        print('{:-<120}'.format(''))
        if len(sys.argv) > 2:
            print("")
            for _index in xrange(_count):
                output = "{}/{}".format(sys.argv[2], _nameTable[_index])
                print(" > Extracting \"{}\"...".format(output))
                if not os.path.exists(os.path.dirname(output)):
                    os.makedirs(os.path.dirname(output))
                with open(output, "wb") as f:
                    f.write(_file[_offsetTable[_index]:_offsetTable[_index] + _lenTable[_index]])
                    f.close()
                _index += 1
            print('{:-<120}'.format(''))
    except ValueError as err:
        pass
else:
    print('usage: {} kwad_file [extract_dir]\n'.format(sys.argv[0]))