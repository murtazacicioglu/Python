#!/usr/bin/env python3
#
#       Ferit Yiğit BALABAN <fybalaban@fybx.dev>
#
#       test_data_types_word.py
import unittest
import data_types


class TestInit(unittest.TestCase):
    def test_init_with_positive_value(self):
        instance = data_types.Word(100)
        self.assertEqual(instance.value, 100)

    def test_init_with_negative_value(self):
        instance = data_types.Word(-50)
        self.assertEqual(instance.value, -50)

    def test_init_with_max_value(self):
        instance = data_types.Word(2147483647)
        self.assertEqual(instance.value, 2147483647)

    def test_init_with_min_value(self):
        instance = data_types.Word(-2147483648)
        self.assertEqual(instance.value, -2147483648)


class TestSetRange(unittest.TestCase):
    def test_valid_range(self):
        instance = data_types.Word(16909060)
        instance.set_lrange(8, 23, "1111111100000000")
        self.assertEqual(instance.as_binary(), "00000001111111110000000000000100")
        instance.from_binary("00000000000000000000000000000000")
        instance.set_lrange(28, 31, "1111")
        self.assertEqual(instance.as_binary(), "00000000000000000000000000001111")

    def test_invalid_start(self):
        instance = data_types.Word(16909060)
        with self.assertRaises(ValueError):
            instance.set_lrange(-5, 16, "11111111")

    def test_invalid_end(self):
        instance = data_types.Word(16909060)
        with self.assertRaises(ValueError):
            instance.set_lrange(8, 40, "11111111")

    def test_end_before_start(self):
        instance = data_types.Word(16909060)
        with self.assertRaises(ValueError):
            instance.set_lrange(16, 8, "11111111")


class TestAsBinary(unittest.TestCase):
    def test_as_binary_positive_value(self):
        instance = data_types.Word(100)
        result = instance.as_binary()
        self.assertEqual(result, '00000000000000000000000001100100')

    def test_as_binary_negative_value(self):
        instance = data_types.Word(-50)
        result = instance.as_binary()
        self.assertEqual(result, '11111111111111111111111111001110')

    def test_as_binary_max_value(self):
        instance = data_types.Word(2147483647)
        result = instance.as_binary()
        self.assertEqual(result, '01111111111111111111111111111111')

    def test_as_binary_min_value(self):
        instance = data_types.Word(-2147483648)
        result = instance.as_binary()
        self.assertEqual(result, '10000000000000000000000000000000')


class TestFromBinary(unittest.TestCase):
    def test_from_binary_positive_value(self):
        instance = data_types.Word(0)
        instance.from_binary('00000000000000000000000001100100')
        self.assertEqual(instance.value, 100)

    def test_from_binary_negative_value(self):
        instance = data_types.Word(0)
        instance.from_binary('11111111111111111111111111001110')
        self.assertEqual(instance.value, -50)

    def test_from_binary_max_value(self):
        instance = data_types.Word(0)
        instance.from_binary('01111111111111111111111111111111')
        self.assertEqual(instance.value, 2147483647)

    def test_from_binary_min_value(self):
        instance = data_types.Word(0)
        instance.from_binary('10000000000000000000000000000000')
        self.assertEqual(instance.value, -2147483648)


class TestAsHexadecimal(unittest.TestCase):
    def test_as_hexadecimal_positive_value(self):
        instance = data_types.Word(100)
        result = instance.as_hexadecimal()
        self.assertEqual(result, '0x64')

    def test_as_hexadecimal_negative_value(self):
        instance = data_types.Word(-50)
        result = instance.as_hexadecimal()
        self.assertEqual(result, '-0x32')

    def test_as_hexadecimal_zero_value(self):
        instance = data_types.Word(0)
        result = instance.as_hexadecimal()
        self.assertEqual(result, '0x0')


if __name__ == '__main__':
    unittest.main()
