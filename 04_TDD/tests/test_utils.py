import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import (validar_email, validar_entero, validar_entero_positivo, 
                   generar_id_unico)


class TestValidaciones(unittest.TestCase):
    
    def test_validar_email_correcto(self):
        self.assertTrue(validar_email("usuario@example.com"))
        self.assertTrue(validar_email("test.user@domain.co.uk"))
        self.assertTrue(validar_email("user+tag@example.com"))
    
    def test_validar_email_incorrecto(self):
        self.assertFalse(validar_email("usuario"))
        self.assertFalse(validar_email("usuario@"))
        self.assertFalse(validar_email("@example.com"))
        self.assertFalse(validar_email("usuario@example"))
        self.assertFalse(validar_email("usuario example.com"))
    
    def test_validar_entero_correcto(self):
        self.assertTrue(validar_entero("123"))
        self.assertTrue(validar_entero("-45"))
        self.assertTrue(validar_entero("0"))
    
    def test_validar_entero_incorrecto(self):
        self.assertFalse(validar_entero("12.5"))
        self.assertFalse(validar_entero("abc"))
        self.assertFalse(validar_entero("12a"))
        self.assertFalse(validar_entero(""))
    
    def test_validar_entero_positivo_correcto(self):
        self.assertTrue(validar_entero_positivo("1"))
        self.assertTrue(validar_entero_positivo("100"))
        self.assertTrue(validar_entero_positivo("999"))
    
    def test_validar_entero_positivo_incorrecto(self):
        self.assertFalse(validar_entero_positivo("0"))
        self.assertFalse(validar_entero_positivo("-1"))
        self.assertFalse(validar_entero_positivo("abc"))
    
    def test_generar_id_unico_lista_vacia(self):
        id_generado = generar_id_unico([])
        self.assertEqual(id_generado, 1)
    
    def test_generar_id_unico_con_elementos(self):
        lista = [
            {'id': 1, 'nombre': 'Test1'},
            {'id': 3, 'nombre': 'Test2'},
            {'id': 2, 'nombre': 'Test3'}
        ]
        id_generado = generar_id_unico(lista)
        self.assertEqual(id_generado, 4)
    
    def test_generar_id_unico_con_un_elemento(self):
        lista = [{'id': 5, 'nombre': 'Test'}]
        id_generado = generar_id_unico(lista)
        self.assertEqual(id_generado, 6)


if __name__ == '__main__':
    unittest.main()