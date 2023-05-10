from unittest import TestCase

import processor
from data_types import Word
from isa import isa_add


class TestIsaAdd(TestCase):
    def test_isa_add_positive_numbers(self):
        proc = processor.Processor()
        proc.registers['x1'] = Word(10)
        proc.registers['x2'] = Word(20)
        isa_add(proc, 'x3', 'x1', 'x2')
        assert proc.registers['x3'].value == 30

    def test_isa_add_negative_numbers(self):
        proc = processor.Processor()
        proc.registers['x1'] = Word(-10)
        proc.registers['x2'] = Word(-20)
        isa_add(proc, 'x3', 'x1', 'x2')
        assert proc.registers['x3'].value == -30

    def test_isa_add_mixed_numbers(self):
        proc = processor.Processor()
        proc.registers['x1'] = Word(10)
        proc.registers['x2'] = Word(-20)
        isa_add(proc, 'x3', 'x1', 'x2')
        assert proc.registers['x3'].value == -10

    def test_isa_add_zero(self):
        proc = processor.Processor()
        proc.registers['x1'] = Word(10)
        proc.registers['x2'] = Word(0)
        isa_add(proc, 'x3', 'x1', 'x2')
        assert proc.registers['x3'].value == 10
