from app_handler import App_handler
from utils import limpiar_pantalla, solicitar_entero, pausar


def mostrar_menu_principal():
    """Muestra el menú principal"""
    print("\n" + "=" * 60)
    print("SISTEMA DE GESTIÓN DE MATRICULACIÓN".center(60))
    print("=" * 60)
    print("\n1. Gestión de Alumnos")
    print("2. Gestión de Módulos")
    print("3. Gestión de Matrículas")
    print("4. Guardar datos")
    print("5. Recargar datos")
    print("0. Salir")
    print("-" * 60)


def mostrar_menu_alumnos():
    """Muestra el menú de gestión de alumnos"""
    print("\n" + "=" * 60)
    print("GESTIÓN DE ALUMNOS".center(60))
    print("=" * 60)
    print("\n1. Listar alumnos")
    print("2. Insertar alumno")
    print("3. Modificar alumno")
    print("4. Borrar alumno")
    print("0. Volver al menú principal")
    print("-" * 60)


def mostrar_menu_modulos():
    """Muestra el menú de gestión de módulos"""
    print("\n" + "=" * 60)
    print("GESTIÓN DE MÓDULOS".center(60))
    print("=" * 60)
    print("\n1. Listar módulos")
    print("2. Insertar módulo")
    print("3. Modificar módulo")
    print("4. Borrar módulo")
    print("0. Volver al menú principal")
    print("-" * 60)


def mostrar_menu_matriculas():
    """Muestra el menú de gestión de matrículas"""
    print("\n" + "=" * 60)
    print("GESTIÓN DE MATRÍCULAS".center(60))
    print("=" * 60)
    print("\n1. Matricular alumno en módulo")
    print("2. Desmatricular alumno de módulo")
    print("3. Ver módulos de un alumno")
    print("0. Volver al menú principal")
    print("-" * 60)


def menu_alumnos(app: App_handler):
    """Gestiona el menú de alumnos"""
    while True:
        limpiar_pantalla()
        mostrar_menu_alumnos()
        
        opcion = solicitar_entero("Selecciona una opción: ", min_val=0, max_val=4)
        
        if opcion == 1:
            limpiar_pantalla()
            app.listar_alumnos()
        elif opcion == 2:
            limpiar_pantalla()
            app.insertar_alumno()
        elif opcion == 3:
            limpiar_pantalla()
            app.modificar_alumno()
        elif opcion == 4:
            limpiar_pantalla()
            app.borrar_alumno()
        elif opcion == 0:
            break


def menu_modulos(app: App_handler):
    """Gestiona el menú de módulos"""
    while True:
        limpiar_pantalla()
        mostrar_menu_modulos()
        
        opcion = solicitar_entero("Selecciona una opción: ", min_val=0, max_val=4)
        
        if opcion == 1:
            limpiar_pantalla()
            app.listar_modulos()
        elif opcion == 2:
            limpiar_pantalla()
            app.insertar_modulo()
        elif opcion == 3:
            limpiar_pantalla()
            app.modificar_modulo()
        elif opcion == 4:
            limpiar_pantalla()
            app.borrar_modulo()
        elif opcion == 0:
            break


def menu_matriculas(app: App_handler):
    """Gestiona el menú de matrículas"""
    while True:
        limpiar_pantalla()
        mostrar_menu_matriculas()
        
        opcion = solicitar_entero("Selecciona una opción: ", min_val=0, max_val=3)
        
        if opcion == 1:
            limpiar_pantalla()
            app.matricular_alumno_modulo()
        elif opcion == 2:
            limpiar_pantalla()
            app.desmatricular_alumno_modulo()
        elif opcion == 3:
            limpiar_pantalla()
            app.ver_modulos_alumno()
        elif opcion == 0:
            break


def main():
    """Función principal de la aplicación"""
    limpiar_pantalla()
    print("\n" + "=" * 60)
    print("BIENVENIDO AL SISTEMA DE GESTIÓN DE MATRICULACIÓN".center(60))
    print("=" * 60)
    pausar()
    
    app = App_handler()
    
    while True:
        limpiar_pantalla()
        mostrar_menu_principal()
        
        opcion = solicitar_entero("Selecciona una opción: ", min_val=0, max_val=5)
        
        if opcion == 1:
            menu_alumnos(app)
        elif opcion == 2:
            menu_modulos(app)
        elif opcion == 3:
            menu_matriculas(app)
        elif opcion == 4:
            limpiar_pantalla()
            app.guardar_datos()
        elif opcion == 5:
            limpiar_pantalla()
            app.recargar_datos()
        elif opcion == 0:
            limpiar_pantalla()
            print("\n¡Gracias por usar el sistema de gestión de matriculación!")
            print("¡Hasta pronto!\n")
            break


if __name__ == "__main__":
    main()