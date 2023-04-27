import unittest
from mx2.enums import Coil, StandardFunctions
from mx2.types import CoilValue, RegisterValue

class TestCoilValue(unittest.TestCase):
    def setUp(self):
        self.cv = CoilValue(coil=Coil.Alarm, value=True)

    def test_create_ok(self):
        CoilValue(coil=Coil.Alarm, value=True)
    
    def test_create_fail(self):
        with self.assertRaises(TypeError):
            CoilValue(0x18, True)
        with self.assertRaises(TypeError):
            CoilValue(Coil.Alarm, 1)

    def test_compare_eq(self):
        other = CoilValue(coil=Coil.Alarm, value=True)
        self.assertTrue(self.cv == other)
        self.assertTrue(self.cv == True)
        other = CoilValue(coil=Coil.Alarm, value=False)
        self.assertFalse(self.cv == other)
        self.assertFalse(self.cv == False)
        other = CoilValue(coil=Coil.BrakeError, value=True)
        self.assertFalse(self.cv == other)
        self.assertFalse(self.cv == 1)
    
    def test_compare_neq(self):
        other = CoilValue(coil=Coil.Alarm, value=True)
        self.assertFalse(self.cv != other)
        self.assertFalse(self.cv != True)
        other = CoilValue(coil=Coil.Alarm, value=False)
        self.assertTrue(self.cv != other)
        self.assertTrue(self.cv != False)
        other = CoilValue(coil=Coil.BrakeError, value=True)
        self.assertTrue(self.cv != other)
        self.assertTrue(self.cv != 1)
    

class TestRegisterValue(unittest.TestCase):
    def setUp(self):
        self.rv = RegisterValue(register=StandardFunctions.A001, value=10)

    def test_create_ok(self):
        RegisterValue(register=StandardFunctions.A001, value=10)

    def test_create_fail(self):
        with self.assertRaises(TypeError):
            RegisterValue(register=1, value=10)
        with self.assertRaises(TypeError):
            RegisterValue(register=StandardFunctions.A001, value=10.1)

    def test_compare_eq(self):
        other = RegisterValue(register=StandardFunctions.A001, value=10)
        self.assertTrue(self.rv == other)
        self.assertTrue(self.rv == 10)
        other = RegisterValue(register=StandardFunctions.A001, value=20)
        self.assertFalse(self.rv == other)
        self.assertFalse(self.rv == 20)
        other = RegisterValue(register=StandardFunctions.A002, value=10)
        self.assertFalse(self.rv == other)
        self.assertFalse(self.rv == 10.1)

    def test_compare_neq(self):
        other = RegisterValue(register=StandardFunctions.A001, value=10)
        self.assertFalse(self.rv != other)
        self.assertFalse(self.rv != 10)
        other = RegisterValue(register=StandardFunctions.A001, value=20)
        self.assertTrue(self.rv != other)
        self.assertTrue(self.rv != 20)
        other = RegisterValue(register=StandardFunctions.A002, value=10)
        self.assertTrue(self.rv != other)
        self.assertTrue(self.rv != 10.1)
    
    def test_compare_lt(self):
        other = RegisterValue(register=StandardFunctions.A002, value=20)
        self.assertTrue(self.rv < other)
        self.assertTrue(self.rv < 20)
        other = RegisterValue(register=StandardFunctions.A002, value=10)
        self.assertFalse(self.rv < other)
        self.assertFalse(self.rv < 10)
        other = RegisterValue(register=StandardFunctions.A002, value=5)
        self.assertFalse(self.rv < other)
        self.assertFalse(self.rv < 5)

    def test_compare_le(self):
        other = RegisterValue(register=StandardFunctions.A002, value=20)
        self.assertTrue(self.rv <= other)
        self.assertTrue(self.rv <= 20)
        other = RegisterValue(register=StandardFunctions.A002, value=10)
        self.assertTrue(self.rv <= other)
        self.assertTrue(self.rv <= 10)
        other = RegisterValue(register=StandardFunctions.A002, value=5)
        self.assertFalse(self.rv <= other)
        self.assertFalse(self.rv <= 5)

    def test_compare_ge(self):
        other = RegisterValue(register=StandardFunctions.A002, value=20)
        self.assertFalse(self.rv >= other)
        self.assertFalse(self.rv >= 20)
        other = RegisterValue(register=StandardFunctions.A002, value=10)
        self.assertTrue(self.rv >= other)
        self.assertTrue(self.rv >= 10)
        other = RegisterValue(register=StandardFunctions.A002, value=5)
        self.assertTrue(self.rv >= other)
        self.assertTrue(self.rv >= 5)

    def test_compare_gt(self):
        other = RegisterValue(register=StandardFunctions.A002, value=20)
        self.assertFalse(self.rv > other)
        self.assertFalse(self.rv > 20)
        other = RegisterValue(register=StandardFunctions.A002, value=10)
        self.assertFalse(self.rv > other)
        self.assertFalse(self.rv > 10)
        other = RegisterValue(register=StandardFunctions.A002, value=5)
        self.assertTrue(self.rv > other)
        self.assertTrue(self.rv > 5)

    def test_lshift(self):
        self.assertEqual(self.rv << 1, 20)

    def test_rshift(self):
        self.assertEqual(self.rv >> 1, 5)

    def test_int_ok(self):
        self.assertIsInstance(int(self.rv), int)

    def test_neg_ok(self):
        self.assertIsInstance(-self.rv, int)
        self.assertEqual(-self.rv, -self.rv.value)

    def test_add_ok(self):
        self.assertIsInstance(self.rv + self.rv, int)
        self.assertIsInstance(self.rv + 10, int)
    
    def test_add_fail(self):
        with self.assertRaises(TypeError):
            self.rv + 0.1

    def test_sub_ok(self):
        self.assertIsInstance(self.rv - self.rv, int)
        self.assertIsInstance(self.rv - 10, int)
    
    def test_sub_fail(self):
        with self.assertRaises(TypeError):
            self.rv - 0.1

    def test_mul_ok(self):
        self.assertIsInstance(self.rv * self.rv, int)
        self.assertIsInstance(self.rv * 10, int)
    
    def test_mul_fail(self):
        with self.assertRaises(TypeError):
            self.rv * 0.1
    
    def test_div_ok(self):
        self.assertIsInstance(self.rv // self.rv, int)
        self.assertIsInstance(self.rv // 10, int)
    
    def test_div_fail(self):
        with self.assertRaises(TypeError):
            self.rv // 0.1

    def test_mod_ok(self):
        self.assertIsInstance(self.rv % self.rv, int)
        self.assertIsInstance(self.rv % 10, int)
    
    def test_mod_fail(self):
        with self.assertRaises(TypeError):
            self.rv % 0.1

    def test_pow_ok(self):
        self.assertIsInstance(self.rv ** self.rv, int)
        self.assertIsInstance(self.rv ** 2, int)
    
    def test_mod_fail(self):
        with self.assertRaises(TypeError):
            self.rv ** 0.1

    def test_or_ok(self):
        self.assertIsInstance(self.rv | self.rv, int)
        self.assertIsInstance(self.rv | 10, int)

    def test_or_fail(self):
        with self.assertRaises(TypeError):
            self.rv | 0.1

    def test_xor_ok(self):
        self.assertIsInstance(self.rv ^ self.rv, int)
        self.assertIsInstance(self.rv ^ 10, int)

    def test_xor_fail(self):
        with self.assertRaises(TypeError):
            self.rv ^ 0.1

    def test_and_ok(self):
        self.assertIsInstance(self.rv & self.rv, int)
        self.assertIsInstance(self.rv & 10, int)

    def test_and_fail(self):
        with self.assertRaises(TypeError):
            self.rv & 0.1

    def test_iadd_ok(self):
        self.rv+=10
        self.assertEqual(self.rv.value, 20)
        self.rv+=self.rv
        self.assertEqual(self.rv.value, 40)

    def test_iadd_fail(self):
        with self.assertRaises(TypeError):
            self.rv+=0.1

    def test_isub_ok(self):
        self.rv-=5
        self.assertEqual(self.rv.value, 5)
        self.rv-=self.rv
        self.assertEqual(self.rv.value, 0)

    def test_isub_fail(self):
        with self.assertRaises(TypeError):
            self.rv-=0.1

    def test_imul_ok(self):
        self.rv*=2
        self.assertEqual(self.rv.value, 20)
        self.rv*=self.rv
        self.assertEqual(self.rv.value, 400)

    def test_imul_fail(self):
        with self.assertRaises(TypeError):
            self.rv*=0.1

    def test_ifloordiv_ok(self):
        self.rv//=2
        self.assertEqual(self.rv.value, 5)
        self.rv//=self.rv
        self.assertEqual(self.rv.value, 1)

    def test_ifloordiv_fail(self):
        with self.assertRaises(TypeError):
            self.rv//=0.1
    
    def test_imod_ok(self):
        self.rv%=3
        self.assertEqual(self.rv.value, 1)
        self.rv%=self.rv
        self.assertEqual(self.rv.value, 0)

    def test_imod_fail(self):
        with self.assertRaises(TypeError):
            self.rv%=0.1
    
    def test_ipow_ok(self):
        self.rv**=3
        self.assertEqual(self.rv.value, 1000)
        self.rv.value = 4
        self.rv**=self.rv
        self.assertEqual(self.rv.value, 256)

    def test_imod_fail(self):
        with self.assertRaises(TypeError):
            self.rv**=0.1
    
    def test_iand_ok(self):
        self.rv&=10
        self.assertEqual(self.rv.value, 10)
        self.rv&=self.rv
        self.assertEqual(self.rv.value, 10)
        self.rv&=3
        self.assertEqual(self.rv.value, 2)

    def test_iand_fail(self):
        with self.assertRaises(TypeError):
            self.rv&=0.1

    def test_ior_ok(self):
        self.rv|=10
        self.assertEqual(self.rv.value, 10)
        self.rv|=self.rv
        self.assertEqual(self.rv.value, 10)
        self.rv|=3
        self.assertEqual(self.rv.value, 11)

    def test_ior_fail(self):
        with self.assertRaises(TypeError):
            self.rv|=0.1

    def test_ixor_ok(self):
        self.rv^=5
        self.assertEqual(self.rv.value, 15)
        self.rv^=self.rv
        self.assertEqual(self.rv.value, 0)
        self.rv^=3
        self.assertEqual(self.rv.value, 3)

    def test_ixor_fail(self):
        with self.assertRaises(TypeError):
            self.rv^=0.1
    
    def test_lshift_ok(self):
        self.rv<<=1
        self.assertEqual(self.rv.value, 20)

    def test_lshift_fail(self):
        with self.assertRaises(TypeError):
            self.rv<<=0.1

    def test_rshift_ok(self):
        self.rv>>=1
        self.assertEqual(self.rv.value, 5)

    def test_rshift_fail(self):
        with self.assertRaises(TypeError):
            self.rv>>=0.1
