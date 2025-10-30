from data_handler import Task, Task_handler, load_tasks_from_file, save_tasks_to_file
from reports import generate_pdf_report
import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_menu():
    print("\n" + "="*50)
    print("     SISTEMA DE GESTIÓN DE TAREAS")
    print("="*50)
    print("\n1.  Añadir nueva tarea")
    print("2.  Ver todas las tareas")
    print("3.  Buscar tarea por ID")
    print("4.  Actualizar tarea")
    print("5.  Completar tarea")
    print("6.  Eliminar tarea")
    print("7.  Buscar tareas por categoría")
    print("8.  Generar reporte PDF")
    print("9.  Guardar tareas")
    print("10. Cargar tareas")
    print("0.  Salir")
    print("="*50)


def add_task(handler: Task_handler):
    print("\n--- AÑADIR NUEVA TAREA ---")
    
    try:
        task_id = int(input("ID de la tarea: "))
        name = input("Nombre: ")
        description = input("Descripción: ")
        
        print("\nPrioridad: 1=Alta, 2=Media, 3=Baja")
        priority = int(input("Prioridad (1-3): "))
        
        print("\nCategorías disponibles: Trabajo, Personal, Salud, Educación")
        primary_cat = input("Categoría primaria: ")
        
        print("\nEtiquetas secundarias (separadas por comas): Urgente, Media, Baja")
        secondary_input = input("Etiquetas secundarias: ")
        secondary_cat = [tag.strip() for tag in secondary_input.split(",")] if secondary_input else []
        
        category = {
            "primaria": primary_cat,
            "secundaria": secondary_cat
        }
        
        task = Task(task_id, name, description, priority, False, category)
        handler.add_task(task)
        
        print(f"\n✓ Tarea '{name}' añadida exitosamente!")
        
    except ValueError:
        print("\n✗ Error: Entrada inválida. Intente de nuevo.")
    except Exception as e:
        print(f"\n✗ Error al añadir tarea: {e}")


def view_all_tasks(handler: Task_handler):
    print("\n--- TODAS LAS TAREAS ---")
    tasks = handler.get_all_tasks()
    
    if not tasks:
        print("\nNo hay tareas registradas.")
        return
    
    for task in tasks:
        print_task(task)


def print_task(task: dict):
    status = "✓ COMPLETADA" if task['completada'] else "○ PENDIENTE"
    priority_map = {1: "Alta", 2: "Media", 3: "Baja"}
    priority = priority_map.get(task['prioridad'], str(task['prioridad']))
    
    print(f"\n{'─'*50}")
    print(f"ID: {task['id']} | {status}")
    print(f"Nombre: {task['nombre']}")
    print(f"Descripción: {task['descripcion']}")
    print(f"Prioridad: {priority}")
    print(f"Categoría: {task['categoria']['primaria']}")
    if task['categoria']['secundaria']:
        print(f"Etiquetas: {', '.join(task['categoria']['secundaria'])}")


def search_task_by_id(handler: Task_handler):
    print("\n--- BUSCAR TAREA POR ID ---")
    
    try:
        task_id = int(input("ID de la tarea: "))
        task = handler.get_task_by_id(task_id)
        
        if task:
            print_task(task)
        else:
            print(f"\n✗ No se encontró tarea con ID {task_id}")
            
    except ValueError:
        print("\n✗ Error: ID inválido.")


def update_task(handler: Task_handler):
    print("\n--- ACTUALIZAR TAREA ---")
    
    try:
        task_id = int(input("ID de la tarea a actualizar: "))
        task = handler.get_task_by_id(task_id)
        
        if not task:
            print(f"\n✗ No se encontró tarea con ID {task_id}")
            return
        
        print("\nDeje en blanco los campos que no desee actualizar")
        
        name = input(f"Nuevo nombre [{task['nombre']}]: ").strip()
        description = input(f"Nueva descripción [{task['descripcion']}]: ").strip()
        
        priority_input = input(f"Nueva prioridad (1-3) [{task['prioridad']}]: ").strip()
        priority = int(priority_input) if priority_input else None
        
        status_input = input(f"¿Completada? (s/n) [{'s' if task['completada'] else 'n'}]: ").strip().lower()
        status = True if status_input == 's' else False if status_input == 'n' else None
        
        cat_input = input(f"Nueva categoría primaria [{task['categoria']['primaria']}]: ").strip()
        
        category = None
        if cat_input:
            sec_input = input("Nuevas etiquetas secundarias (separadas por comas): ").strip()
            secondary = [tag.strip() for tag in sec_input.split(",")] if sec_input else []
            category = {"primaria": cat_input, "secundaria": secondary}
        
        handler.update_task(
            task_id,
            name=name if name else None,
            description=description if description else None,
            priority=priority,
            status=status,
            category=category
        )
        
        print("\n✓ Tarea actualizada exitosamente!")
        
    except ValueError:
        print("\n✗ Error: Entrada inválida.")


def complete_task(handler: Task_handler):
    print("\n--- COMPLETAR TAREA ---")
    
    try:
        task_id = int(input("ID de la tarea: "))
        
        if handler.complete_task(task_id):
            print(f"\n✓ Tarea {task_id} marcada como completada!")
        else:
            print(f"\n✗ No se encontró tarea con ID {task_id}")
            
    except ValueError:
        print("\n✗ Error: ID inválido.")


def delete_task(handler: Task_handler):
    print("\n--- ELIMINAR TAREA ---")
    
    try:
        task_id = int(input("ID de la tarea a eliminar: "))
        
        for task in handler.tasks:
            if task.id == task_id:
                confirm = input(f"¿Seguro que desea eliminar '{task.name}'? (s/n): ").strip().lower()
                if confirm == 's':
                    handler.delete_task(task)
                    print(f"\n✓ Tarea eliminada exitosamente!")
                else:
                    print("\n○ Operación cancelada.")
                return
        
        print(f"\n✗ No se encontró tarea con ID {task_id}")
        
    except ValueError:
        print("\n✗ Error: ID inválido.")


def search_by_category(handler: Task_handler):
    print("\n--- BUSCAR POR CATEGORÍA ---")
    
    category = input("Nombre de la categoría: ").strip()
    tasks = handler.search_tasks_by_category(category)
    
    if tasks:
        print(f"\nSe encontraron {len(tasks)} tarea(s) en la categoría '{category}':")
        for task in tasks:
            print_task(task)
    else:
        print(f"\n○ No se encontraron tareas en la categoría '{category}'")


def generate_report(handler: Task_handler):
    print("\n--- GENERAR REPORTE PDF ---")
    
    tasks = handler.get_all_tasks()
    
    if not tasks:
        print("\n✗ No hay tareas para generar reporte.")
        return
    
    filename = input("Nombre del archivo (default: task_report.pdf): ").strip()
    if not filename:
        filename = "task_report.pdf"
    
    if not filename.endswith('.pdf'):
        filename += '.pdf'
    
    try:
        generate_pdf_report(tasks, filename)
        print(f"\n✓ Reporte generado exitosamente: {filename}")
    except Exception as e:
        print(f"\n✗ Error al generar reporte: {e}")


def save_tasks(handler: Task_handler):
    """Guarda las tareas en un archivo"""
    print("\n--- GUARDAR TAREAS ---")
    
    filename = input("Nombre del archivo (default: tasks.json): ").strip()
    if not filename:
        filename = "tasks.json"
    
    if not filename.endswith('.json'):
        filename += '.json'
    
    try:
        save_tasks_to_file(handler, filename)
        print(f"\n✓ Tareas guardadas en: {filename}")
    except Exception as e:
        print(f"\n✗ Error al guardar: {e}")


def load_tasks(handler: Task_handler):
    print("\n--- CARGAR TAREAS ---")
    
    filename = input("Nombre del archivo (default: tasks.json): ").strip()
    if not filename:
        filename = "tasks.json"
    
    if not filename.endswith('.json'):
        filename += '.json'
    
    if not os.path.exists(filename):
        print(f"\n✗ El archivo '{filename}' no existe.")
        return handler
    
    try:
        new_handler = load_tasks_from_file(filename)
        print(f"\n✓ Tareas cargadas desde: {filename}")
        print(f"Total de tareas cargadas: {len(new_handler.get_all_tasks())}")
        return new_handler
    except Exception as e:
        print(f"\n✗ Error al cargar: {e}")
        return handler


def main():
    handler = Task_handler()
    
    print("\n¡Bienvenido al Sistema de Gestión de Tareas!")
    
    while True:
        print_menu()
        choice = input("\nSeleccione una opción: ").strip()
        
        if choice == '1':
            add_task(handler)
        elif choice == '2':
            view_all_tasks(handler)
        elif choice == '3':
            search_task_by_id(handler)
        elif choice == '4':
            update_task(handler)
        elif choice == '5':
            complete_task(handler)
        elif choice == '6':
            delete_task(handler)
        elif choice == '7':
            search_by_category(handler)
        elif choice == '8':
            generate_report(handler)
        elif choice == '9':
            save_tasks(handler)
        elif choice == '10':
            handler = load_tasks(handler)
        elif choice == '0':
            print("\n¡Hasta luego! 👋")
            break
        else:
            print("\n✗ Opción inválida. Intente de nuevo.")
        
        input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    main()