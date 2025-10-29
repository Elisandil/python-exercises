import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_handler import Alumno, Modulo, Matricula_handler, save_data_to_file, load_data_from_file


class TestAlumno(unittest.TestCase):
    
    def test_crear_alumno(self):
        alumno = Alumno(1, "Juan", "Pérez García", "juan@example.com")
        self.assertEqual(alumno.id, 1)
        self.assertEqual(alumno.nombre, "Juan")
        self.assertEqual(alumno.apellidos, "Pérez García")
        self.assertEqual(alumno.email, "juan@example.com")
        self.assertEqual(alumno.modulos, [])
    
    def test_alumno_to_dict(self):
        alumno = Alumno(1, "Juan", "Pérez", "juan@example.com", [1, 2])
        alumno_dict = alumno.to_dict()
        self.assertEqual(alumno_dict['id'], 1)
        self.assertEqual(alumno_dict['nombre'], "Juan")
        self.assertListEqual(alumno_dict['modulos'], [1, 2])
    
    def test_alumno_from_dict(self):
        data = {
            'id': 2,
            'nombre': "María",
            'apellidos': "López",
            'email': "maria@example.com",
            'modulos': [3, 4]
        }
        alumno = Alumno.from_dict(data)
        self.assertEqual(alumno.id, 2)
        self.assertEqual(alumno.nombre, "María")
        self.assertListEqual(alumno.modulos, [3, 4])


class TestModulo(unittest.TestCase):
    
    def test_crear_modulo(self):
        modulo = Modulo(1, "Programación", "PRG101", 6, 1)
        self.assertEqual(modulo.id, 1)
        self.assertEqual(modulo.nombre, "Programación")
        self.assertEqual(modulo.codigo, "PRG101")
        self.assertEqual(modulo.creditos, 6)
        self.assertEqual(modulo.curso, 1)
    
    def test_modulo_to_dict(self):
        modulo = Modulo(1, "Programación", "PRG101", 6, 1)
        modulo_dict = modulo.to_dict()
        self.assertEqual(modulo_dict['id'], 1)
        self.assertEqual(modulo_dict['codigo'], "PRG101")
        self.assertEqual(modulo_dict['creditos'], 6)
    
    def test_modulo_from_dict(self):
        data = {
            'id': 2,
            'nombre': "Bases de Datos",
            'codigo': "BD201",
            'creditos': 8,
            'curso': 2
        }
        modulo = Modulo.from_dict(data)
        self.assertEqual(modulo.id, 2)
        self.assertEqual(modulo.nombre, "Bases de Datos")
        self.assertEqual(modulo.creditos, 8)


class TestMatriculaHandler(unittest.TestCase):
    
    def setUp(self):
        self.handler = Matricula_handler()
    
    # Tests de Alumnos
    def test_add_alumno(self):
        alumno = Alumno(1, "Juan", "Pérez", "juan@example.com")
        result = self.handler.add_alumno(alumno)
        self.assertTrue(result)
        self.assertEqual(len(self.handler.get_all_alumnos()), 1)
    
    def test_add_alumno_duplicado(self):
        alumno1 = Alumno(1, "Juan", "Pérez", "juan@example.com")
        alumno2 = Alumno(1, "Pedro", "García", "pedro@example.com")
        self.handler.add_alumno(alumno1)
        result = self.handler.add_alumno(alumno2)
        self.assertFalse(result)
        self.assertEqual(len(self.handler.get_all_alumnos()), 1)
    
    def test_get_alumno_by_id(self):
        alumno = Alumno(5, "María", "López", "maria@example.com")
        self.handler.add_alumno(alumno)
        found = self.handler.get_alumno_by_id(5)
        self.assertIsNotNone(found)
        self.assertEqual(found['id'], 5)
        self.assertEqual(found['nombre'], "María")
    
    def test_get_alumno_by_id_no_existe(self):
        found = self.handler.get_alumno_by_id(999)
        self.assertIsNone(found)
    
    def test_update_alumno(self):
        alumno = Alumno(10, "Carlos", "Ruiz", "carlos@example.com")
        self.handler.add_alumno(alumno)
        result = self.handler.update_alumno(10, nombre="Carlos Alberto", email="nuevo@example.com")
        self.assertTrue(result)
        updated = self.handler.get_alumno_by_id(10)
        self.assertEqual(updated['nombre'], "Carlos Alberto")
        self.assertEqual(updated['email'], "nuevo@example.com")
        self.assertEqual(updated['apellidos'], "Ruiz")
    
    def test_delete_alumno(self):
        alumno = Alumno(15, "Ana", "Martín", "ana@example.com")
        self.handler.add_alumno(alumno)
        result = self.handler.delete_alumno(15)
        self.assertTrue(result)
        self.assertEqual(len(self.handler.get_all_alumnos()), 0)
    
    # Tests de Módulos
    def test_add_modulo(self):
        modulo = Modulo(1, "Programación", "PRG101", 6, 1)
        result = self.handler.add_modulo(modulo)
        self.assertTrue(result)
        self.assertEqual(len(self.handler.get_all_modulos()), 1)
    
    def test_add_modulo_duplicado(self):
        modulo1 = Modulo(1, "Programación", "PRG101", 6, 1)
        modulo2 = Modulo(1, "Otro", "OTR102", 4, 2)
        self.handler.add_modulo(modulo1)
        result = self.handler.add_modulo(modulo2)
        self.assertFalse(result)
        self.assertEqual(len(self.handler.get_all_modulos()), 1)
    
    def test_get_modulo_by_id(self):
        modulo = Modulo(20, "Bases de Datos", "BD201", 8, 2)
        self.handler.add_modulo(modulo)
        found = self.handler.get_modulo_by_id(20)
        self.assertIsNotNone(found)
        self.assertEqual(found['id'], 20)
        self.assertEqual(found['nombre'], "Bases de Datos")
    
    def test_update_modulo(self):
        modulo = Modulo(25, "Sistemas", "SIS301", 5, 3)
        self.handler.add_modulo(modulo)
        result = self.handler.update_modulo(25, nombre="Sistemas Operativos", creditos=7)
        self.assertTrue(result)
        updated = self.handler.get_modulo_by_id(25)
        self.assertEqual(updated['nombre'], "Sistemas Operativos")
        self.assertEqual(updated['creditos'], 7)
        self.assertEqual(updated['codigo'], "SIS301")
    
    def test_delete_modulo(self):
        modulo = Modulo(30, "Redes", "RED401", 6, 4)
        self.handler.add_modulo(modulo)
        result = self.handler.delete_modulo(30)
        self.assertTrue(result)
        self.assertEqual(len(self.handler.get_all_modulos()), 0)
    
    def test_delete_modulo_elimina_matriculas(self):
        alumno = Alumno(40, "Luis", "Gómez", "luis@example.com")
        modulo = Modulo(40, "Test", "TST401", 5, 1)
        self.handler.add_alumno(alumno)
        self.handler.add_modulo(modulo)
        self.handler.matricular_alumno(40, 40)
        
        self.handler.delete_modulo(40)
        alumno_updated = self.handler.get_alumno_by_id(40)
        self.assertNotIn(40, alumno_updated['modulos'])
    
    # Tests de Matrículas
    def test_matricular_alumno(self):
        alumno = Alumno(50, "Elena", "Sanz", "elena@example.com")
        modulo = Modulo(50, "Matemáticas", "MAT101", 6, 1)
        self.handler.add_alumno(alumno)
        self.handler.add_modulo(modulo)
        
        result = self.handler.matricular_alumno(50, 50)
        self.assertTrue(result)
        
        alumno_updated = self.handler.get_alumno_by_id(50)
        self.assertIn(50, alumno_updated['modulos'])
    
    def test_matricular_alumno_no_existe(self):
        modulo = Modulo(60, "Física", "FIS101", 6, 1)
        self.handler.add_modulo(modulo)
        result = self.handler.matricular_alumno(999, 60)
        self.assertFalse(result)
    
    def test_matricular_modulo_no_existe(self):
        alumno = Alumno(70, "Pedro", "Díaz", "pedro@example.com")
        self.handler.add_alumno(alumno)
        result = self.handler.matricular_alumno(70, 999)
        self.assertFalse(result)
    
    def test_matricular_alumno_duplicado(self):
        alumno = Alumno(80, "Sara", "Torres", "sara@example.com")
        modulo = Modulo(80, "Historia", "HIS101", 4, 1)
        self.handler.add_alumno(alumno)
        self.handler.add_modulo(modulo)
        
        self.handler.matricular_alumno(80, 80)
        result = self.handler.matricular_alumno(80, 80)
        self.assertFalse(result)
    
    def test_desmatricular_alumno(self):
        alumno = Alumno(90, "Jorge", "Vega", "jorge@example.com")
        modulo = Modulo(90, "Inglés", "ING101", 4, 1)
        self.handler.add_alumno(alumno)
        self.handler.add_modulo(modulo)
        self.handler.matricular_alumno(90, 90)
        
        result = self.handler.desmatricular_alumno(90, 90)
        self.assertTrue(result)
        
        alumno_updated = self.handler.get_alumno_by_id(90)
        self.assertNotIn(90, alumno_updated['modulos'])
    
    def test_get_modulos_alumno(self):
        alumno = Alumno(100, "Laura", "Ramos", "laura@example.com")
        modulo1 = Modulo(100, "Módulo 1", "MOD101", 6, 1)
        modulo2 = Modulo(101, "Módulo 2", "MOD102", 5, 1)
        
        self.handler.add_alumno(alumno)
        self.handler.add_modulo(modulo1)
        self.handler.add_modulo(modulo2)
        self.handler.matricular_alumno(100, 100)
        self.handler.matricular_alumno(100, 101)
        
        modulos = self.handler.get_modulos_alumno(100)
        self.assertEqual(len(modulos), 2)
        nombres = [m['nombre'] for m in modulos]
        self.assertIn("Módulo 1", nombres)
        self.assertIn("Módulo 2", nombres)


class TestFileOperations(unittest.TestCase):
    
    def setUp(self):
        self.test_file = 'test_matriculas.json'
    
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_save_and_load(self):
        handler = Matricula_handler()
        
        alumno = Alumno(1, "Test", "User", "test@example.com")
        modulo = Modulo(1, "Test Module", "TST101", 5, 1)
        
        handler.add_alumno(alumno)
        handler.add_modulo(modulo)
        handler.matricular_alumno(1, 1)
        
        result = save_data_to_file(handler, self.test_file)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_file))
        
        new_handler = load_data_from_file(self.test_file)
        
        alumnos = new_handler.get_all_alumnos()
        modulos = new_handler.get_all_modulos()
        
        self.assertEqual(len(alumnos), 1)
        self.assertEqual(len(modulos), 1)
        self.assertEqual(alumnos[0]['nombre'], "Test")
        self.assertEqual(modulos[0]['nombre'], "Test Module")
        self.assertIn(1, alumnos[0]['modulos'])
    
    def test_load_file_not_exists(self):
        handler = load_data_from_file('archivo_no_existe.json')
        self.assertIsInstance(handler, Matricula_handler)
        self.assertEqual(len(handler.get_all_alumnos()), 0)
        self.assertEqual(len(handler.get_all_modulos()), 0)


if __name__ == '__main__':
    unittest.main()