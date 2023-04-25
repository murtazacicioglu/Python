#!/usr/bin/env python3
#
#         Ferit Yiğit BALABAN <fybalaban@fybx.dev>
#
import unittest
import data_types as dt


class Test_DataTypes(unittest.TestCase):
    def test_init_with_int(self):
        w = dt.Word(0)
        self.assertEqual(w.value, 0)
        w = dt.Word(2147483647)
        self.assertEqual(w.value, 2147483647)
        w = dt.Word(-2147483647)
        self.assertEqual(w.value, -2147483647)

        # overflow yaşanmalı
        w = dt.Word(4294967296)
        self.assertEqual(w.value, 0)


if __name__ == '__main__':
    unittest.main()
