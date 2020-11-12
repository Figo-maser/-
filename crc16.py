# -*- coding: utf-8 -*-
"""
@Time:2019/5/24 14:16
@Author: Cai jz
"""
from binascii import *
from crcmod import *
import time

# CRC16-MODBUS
def crc16Add(read):
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    data = read.replace(" ", "")
    readcrcout = hex(crc16(unhexlify(data))).upper()
    str_list = list(readcrcout)
    if len(str_list) == 5:
        str_list.insert(2, '0')  # 位数不足补0
    crc_data = "".join(str_list)
    read = read.strip()  + crc_data[4:]  + crc_data[2:4]
    print(read)
    return read


if __name__ == '__main__':
    numble = '010361000012'
    crc_numle = crc16Add(numble)
    print(crc_numle)