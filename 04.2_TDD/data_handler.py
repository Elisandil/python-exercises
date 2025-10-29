import json
from typing import Optional, List, Dict, Any


class Task:
    """Clase para representar una tarea individual"""
    
    def __init__(self, task_id: int, name: str, description: str, 
                 priority: int = 1, status: bool = False, 
                 category: Dict[str, Any] = None):
        self.id = task_id
        self.name = name
        self.description = description
        self.priority = priority
        self.status = status
        self.category = category if category else {"primaria": "", "secundaria": []}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la tarea a un diccionario"""
        return {
            "id": self.id,
            "nombre": self.name,
            "descripcion": self.description,
            "prioridad": self.priority,
            "completada": self.status,
            "categoria": self.category
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Crea una tarea desde un diccionario"""
        return cls(
            task_id=data["id"],
            name=data["nombre"],
            description=data["descripcion"],
            priority=data["prioridad"],
            status=data["completada"],
            category=data["categoria"]
        )


class Task_handler:
    """Clase para manejar múltiples tareas"""
    
    def __init__(self):
        self.tasks: List[Task] = []
    
    def add_task(self, task: Task) -> None:
        """Añade una tarea al gestor"""
        self.tasks.append(task)
    
    def delete_task(self, task: Task) -> None:
        """Elimina una tarea del gestor"""
        if task in self.tasks:
            self.tasks.remove(task)
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Obtiene todas las tareas como lista de diccionarios"""
        return [task.to_dict() for task in self.tasks]
    
    def get_task_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Busca una tarea por su ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task.to_dict()
        return None
    
    def update_task(self, task_id: int, name: str = None, 
                   description: str = None, priority: int = None,
                   status: bool = None, category: Dict[str, Any] = None) -> bool:
        """Actualiza los campos de una tarea"""
        for task in self.tasks:
            if task.id == task_id:
                if name is not None:
                    task.name = name
                if description is not None:
                    task.description = description
                if priority is not None:
                    task.priority = priority
                if status is not None:
                    task.status = status
                if category is not None:
                    task.category = category
                return True
        return False
    
    def complete_task(self, task_id: int) -> bool:
        """Marca una tarea como completada"""
        return self.update_task(task_id, status=True)
    
    def search_tasks_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Busca tareas por categoría primaria"""
        result = []
        for task in self.tasks:
            if task.category.get("primaria") == category:
                result.append(task.to_dict())
        return result


def save_tasks_to_file(handler: Task_handler, filename: str) -> None:
    """Guarda las tareas en un archivo JSON"""
    tasks_data = handler.get_all_tasks()
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(tasks_data, f, ensure_ascii=False, indent=2)


def load_tasks_from_file(filename: str) -> Task_handler:
    """Carga las tareas desde un archivo JSON"""
    handler = Task_handler()
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            tasks_data = json.load(f)
            for task_dict in tasks_data:
                task = Task.from_dict(task_dict)
                handler.add_task(task)
    except FileNotFoundError:
        pass
    return handler