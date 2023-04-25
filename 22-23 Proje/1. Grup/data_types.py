#!/usr/bin/env python3
#
#         Ferit Yiğit BALABAN <fybalaban@fybx.dev>
#
from ctypes import c_int32


class Word:
    _value = c_int32(0)
    _width = 32
    _maxvl = 2147483647
    _minvl = -2147483648

    def __init__(self, int_value: int):
        """
        Verilen tam sayı değerini içeren bir kelime nesnesi üretir. Kelimeler 32 bit genişliğindedir.

        :param int_value: Kelimenin tutacağı değer
        """
        self._value = c_int32(int_value)

    def as_binary(self):
        """
        Kelimenin tuttuğu değerin ikinin tümleyeni biçimindeki ikili gösterimini döndürür.

        :return: Kelimenin tuttuğu değerin ikili gösterim string'i.
        :rtype: str
        """
        return format(self._value.value % (1 << self._width), '0{}b'.format(self._width))

    def as_hexadecimal(self):
        return hex(self._value.value)

    @property
    def value(self):
        return self._value.value

    @property
    def width(self):
        return self._width

    @property
    def minvl(self):
        return self._minvl

    @property
    def maxvl(self):
        return self._maxvl