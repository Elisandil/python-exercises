from data_handler import Alumno, Modulo, Matricula_handler, save_data_to_file, load_data_from_file
from utils import (solicitar_entero, solicitar_texto, solicitar_email, 
                   confirmar_accion, pausar, mostrar_tabla, generar_id_unico)


class App_handler:
    def __init__(self):
        self.handler = Matricula_handler()
        self.cargar_datos_iniciales()
    
    def cargar_datos_iniciales(self):
        """Carga los datos desde el archivo JSON al iniciar"""
        self.handler = load_data_from_file()
        print("Datos cargados correctamente.")
    
    def recargar_datos(self):
        """Recarga los datos desde el archivo JSON"""
        if confirmar_accion("¿Estás seguro de recargar los datos? Se perderán los cambios no guardados."):
            self.handler = load_data_from_file()
            print("Datos recargados correctamente.")
        pausar()
    
    def guardar_datos(self):
        """Guarda los datos en el archivo JSON"""
        if save_data_to_file(self.handler):
            print("Datos guardados correctamente.")
        else:
            print("Error al guardar los datos.")
        pausar()
    
    # Gestión de Alumnos
    def listar_alumnos(self):
        """Lista todos los alumnos"""
        alumnos = self.handler.get_all_alumnos()
        if not alumnos:
            print("\nNo hay alumnos registrados.")
            pausar()
            return
        
        rows = []
        for alumno in alumnos:
            num_modulos = len(alumno['modulos'])
            rows.append([
                alumno['id'],
                alumno['nombre'],
                alumno['apellidos'],
                alumno['email'],
                num_modulos
            ])
        
        mostrar_tabla(
            ['ID', 'Nombre', 'Apellidos', 'Email', 'Módulos'],
            rows,
            'LISTADO DE ALUMNOS'
        )
        pausar()
    
    def insertar_alumno(self):
        """Inserta un nuevo alumno"""
        print("\n=== INSERTAR NUEVO ALUMNO ===")
        
        id_nuevo = generar_id_unico(self.handler.get_all_alumnos())
        nombre = solicitar_texto("Nombre: ")
        apellidos = solicitar_texto("Apellidos: ")
        email = solicitar_email("Email: ")
        
        alumno = Alumno(id_nuevo, nombre, apellidos, email)
        
        if self.handler.add_alumno(alumno):
            print(f"\nAlumno '{nombre} {apellidos}' añadido correctamente con ID {id_nuevo}.")
        else:
            print("\nError al añadir el alumno.")
        
        pausar()
    
    def modificar_alumno(self):
        """Modifica un alumno existente"""
        print("\n=== MODIFICAR ALUMNO ===")
        
        self.listar_alumnos()
        
        alumno_id = solicitar_entero("ID del alumno a modificar: ", min_val=1)
        alumno = self.handler.get_alumno_by_id(alumno_id)
        
        if not alumno:
            print(f"\nNo existe un alumno con ID {alumno_id}.")
            pausar()
            return
        
        print(f"\nAlumno actual: {alumno['nombre']} {alumno['apellidos']} ({alumno['email']})")
        print("\nDeja en blanco para mantener el valor actual.")
        
        nombre = input(f"Nuevo nombre [{alumno['nombre']}]: ").strip()
        apellidos = input(f"Nuevos apellidos [{alumno['apellidos']}]: ").strip()
        email = input(f"Nuevo email [{alumno['email']}]: ").strip()
        
        if self.handler.update_alumno(
            alumno_id,
            nombre if nombre else None,
            apellidos if apellidos else None,
            email if email else None
        ):
            print("\nAlumno modificado correctamente.")
        else:
            print("\nError al modificar el alumno.")
        
        pausar()
    
    def borrar_alumno(self):
        """Borra un alumno"""
        print("\n=== BORRAR ALUMNO ===")
        
        self.listar_alumnos()
        
        alumno_id = solicitar_entero("ID del alumno a borrar: ", min_val=1)
        alumno = self.handler.get_alumno_by_id(alumno_id)
        
        if not alumno:
            print(f"\nNo existe un alumno con ID {alumno_id}.")
            pausar()
            return
        
        if confirmar_accion(f"¿Estás seguro de borrar a {alumno['nombre']} {alumno['apellidos']}?"):
            if self.handler.delete_alumno(alumno_id):
                print("\nAlumno borrado correctamente.")
            else:
                print("\nError al borrar el alumno.")
        
        pausar()
    
    # Gestión de Módulos
    def listar_modulos(self):
        """Lista todos los módulos"""
        modulos = self.handler.get_all_modulos()
        if not modulos:
            print("\nNo hay módulos registrados.")
            pausar()
            return
        
        rows = []
        for modulo in modulos:
            rows.append([
                modulo['id'],
                modulo['codigo'],
                modulo['nombre'],
                modulo['creditos'],
                modulo['curso']
            ])
        
        mostrar_tabla(
            ['ID', 'Código', 'Nombre', 'Créditos', 'Curso'],
            rows,
            'LISTADO DE MÓDULOS'
        )
        pausar()
    
    def insertar_modulo(self):
        """Inserta un nuevo módulo"""
        print("\n=== INSERTAR NUEVO MÓDULO ===")
        
        id_nuevo = generar_id_unico(self.handler.get_all_modulos())
        nombre = solicitar_texto("Nombre del módulo: ")
        codigo = solicitar_texto("Código del módulo: ")
        creditos = solicitar_entero("Créditos: ", min_val=1)
        curso = solicitar_entero("Curso: ", min_val=1, max_val=4)
        
        modulo = Modulo(id_nuevo, nombre, codigo, creditos, curso)
        
        if self.handler.add_modulo(modulo):
            print(f"\nMódulo '{nombre}' añadido correctamente con ID {id_nuevo}.")
        else:
            print("\nError al añadir el módulo.")
        
        pausar()
    
    def modificar_modulo(self):
        """Modifica un módulo existente"""
        print("\n=== MODIFICAR MÓDULO ===")
        
        self.listar_modulos()
        
        modulo_id = solicitar_entero("ID del módulo a modificar: ", min_val=1)
        modulo = self.handler.get_modulo_by_id(modulo_id)
        
        if not modulo:
            print(f"\nNo existe un módulo con ID {modulo_id}.")
            pausar()
            return
        
        print(f"\nMódulo actual: {modulo['nombre']} ({modulo['codigo']}) - {modulo['creditos']} créditos - Curso {modulo['curso']}")
        print("\nDeja en blanco para mantener el valor actual.")
        
        nombre = input(f"Nuevo nombre [{modulo['nombre']}]: ").strip()
        codigo = input(f"Nuevo código [{modulo['codigo']}]: ").strip()
        creditos = input(f"Nuevos créditos [{modulo['creditos']}]: ").strip()
        curso = input(f"Nuevo curso [{modulo['curso']}]: ").strip()
        
        if self.handler.update_modulo(
            modulo_id,
            nombre if nombre else None,
            codigo if codigo else None,
            int(creditos) if creditos else None,
            int(curso) if curso else None
        ):
            print("\nMódulo modificado correctamente.")
        else:
            print("\nError al modificar el módulo.")
        
        pausar()
    
    def borrar_modulo(self):
        """Borra un módulo"""
        print("\n=== BORRAR MÓDULO ===")
        
        self.listar_modulos()
        
        modulo_id = solicitar_entero("ID del módulo a borrar: ", min_val=1)
        modulo = self.handler.get_modulo_by_id(modulo_id)
        
        if not modulo:
            print(f"\nNo existe un módulo con ID {modulo_id}.")
            pausar()
            return
        
        if confirmar_accion(f"¿Estás seguro de borrar el módulo {modulo['nombre']}? Se eliminará de las matrículas."):
            if self.handler.delete_modulo(modulo_id):
                print("\nMódulo borrado correctamente.")
            else:
                print("\nError al borrar el módulo.")
        
        pausar()
    
    # Gestión de Matrículas
    def matricular_alumno_modulo(self):
        """Matricula un alumno en un módulo"""
        print("\n=== MATRICULAR ALUMNO EN MÓDULO ===")
        
        self.listar_alumnos()
        alumno_id = solicitar_entero("ID del alumno: ", min_val=1)
        
        alumno = self.handler.get_alumno_by_id(alumno_id)
        if not alumno:
            print(f"\nNo existe un alumno con ID {alumno_id}.")
            pausar()
            return
        
        self.listar_modulos()
        modulo_id = solicitar_entero("ID del módulo: ", min_val=1)
        
        modulo = self.handler.get_modulo_by_id(modulo_id)
        if not modulo:
            print(f"\nNo existe un módulo con ID {modulo_id}.")
            pausar()
            return
        
        if self.handler.matricular_alumno(alumno_id, modulo_id):
            print(f"\nAlumno {alumno['nombre']} matriculado en {modulo['nombre']} correctamente.")
        else:
            print("\nError: El alumno ya está matriculado en este módulo o el módulo no existe.")
        
        pausar()
    
    def desmatricular_alumno_modulo(self):
        """Desmatricula un alumno de un módulo"""
        print("\n=== DESMATRICULAR ALUMNO DE MÓDULO ===")
        
        self.listar_alumnos()
        alumno_id = solicitar_entero("ID del alumno: ", min_val=1)
        
        alumno = self.handler.get_alumno_by_id(alumno_id)
        if not alumno:
            print(f"\nNo existe un alumno con ID {alumno_id}.")
            pausar()
            return
        
        modulos_alumno = self.handler.get_modulos_alumno(alumno_id)
        if not modulos_alumno:
            print(f"\nEl alumno {alumno['nombre']} no está matriculado en ningún módulo.")
            pausar()
            return
        
        print(f"\nMódulos de {alumno['nombre']}:")
        rows = [[m['id'], m['codigo'], m['nombre']] for m in modulos_alumno]
        mostrar_tabla(['ID', 'Código', 'Nombre'], rows)
        
        modulo_id = solicitar_entero("ID del módulo a desmatricular: ", min_val=1)
        
        if self.handler.desmatricular_alumno(alumno_id, modulo_id):
            print(f"\nAlumno desmatriculado correctamente.")
        else:
            print("\nError al desmatricular el alumno.")
        
        pausar()
    
    def ver_modulos_alumno(self):
        """Muestra los módulos de un alumno"""
        print("\n=== VER MÓDULOS DE ALUMNO ===")
        
        self.listar_alumnos()
        alumno_id = solicitar_entero("ID del alumno: ", min_val=1)
        
        alumno = self.handler.get_alumno_by_id(alumno_id)
        if not alumno:
            print(f"\nNo existe un alumno con ID {alumno_id}.")
            pausar()
            return
        
        modulos = self.handler.get_modulos_alumno(alumno_id)
        if not modulos:
            print(f"\nEl alumno {alumno['nombre']} {alumno['apellidos']} no está matriculado en ningún módulo.")
            pausar()
            return
        
        rows = []
        total_creditos = 0
        for modulo in modulos:
            rows.append([
                modulo['codigo'],
                modulo['nombre'],
                modulo['creditos'],
                modulo['curso']
            ])
            total_creditos += modulo['creditos']
        
        mostrar_tabla(
            ['Código', 'Nombre', 'Créditos', 'Curso'],
            rows,
            f"MÓDULOS DE {alumno['nombre'].upper()} {alumno['apellidos'].upper()}"
        )
        print(f"Total de créditos: {total_creditos}\n")
        pausar()