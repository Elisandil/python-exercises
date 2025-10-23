import json
from typing import List, Dict, Optional

class Alumno:
    def __init__(self, id: int, nombre: str, apellidos: str, email: str, modulos: List[int] = None):
        self.id = id
        self.nombre = nombre
        self.apellidos = apellidos
        self.email = email
        self.modulos = modulos if modulos else []
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellidos': self.apellidos,
            'email': self.email,
            'modulos': self.modulos
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Alumno':
        return Alumno(
            id=data['id'],
            nombre=data['nombre'],
            apellidos=data['apellidos'],
            email=data['email'],
            modulos=data.get('modulos', [])
        )


class Modulo:
    def __init__(self, id: int, nombre: str, codigo: str, creditos: int, curso: int):
        self.id = id
        self.nombre = nombre
        self.codigo = codigo
        self.creditos = creditos
        self.curso = curso
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'nombre': self.nombre,
            'codigo': self.codigo,
            'creditos': self.creditos,
            'curso': self.curso
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Modulo':
        return Modulo(
            id=data['id'],
            nombre=data['nombre'],
            codigo=data['codigo'],
            creditos=data['creditos'],
            curso=data['curso']
        )


class Matricula_handler:
    def __init__(self):
        self.alumnos: List[Alumno] = []
        self.modulos: List[Modulo] = []
    
    # Gestión de Alumnos
    def add_alumno(self, alumno: Alumno) -> bool:
        if self.get_alumno_by_id(alumno.id):
            return False
        self.alumnos.append(alumno)
        return True
    
    def get_alumno_by_id(self, alumno_id: int) -> Optional[Dict]:
        for alumno in self.alumnos:
            if alumno.id == alumno_id:
                return alumno.to_dict()
        return None
    
    def get_all_alumnos(self) -> List[Dict]:
        return [alumno.to_dict() for alumno in self.alumnos]
    
    def update_alumno(self, alumno_id: int, nombre: str = None, apellidos: str = None, email: str = None) -> bool:
        for alumno in self.alumnos:
            if alumno.id == alumno_id:
                if nombre:
                    alumno.nombre = nombre
                if apellidos:
                    alumno.apellidos = apellidos
                if email:
                    alumno.email = email
                return True
        return False
    
    def delete_alumno(self, alumno_id: int) -> bool:
        for i, alumno in enumerate(self.alumnos):
            if alumno.id == alumno_id:
                self.alumnos.pop(i)
                return True
        return False
    
    # Gestión de Módulos
    def add_modulo(self, modulo: Modulo) -> bool:
        if self.get_modulo_by_id(modulo.id):
            return False
        self.modulos.append(modulo)
        return True
    
    def get_modulo_by_id(self, modulo_id: int) -> Optional[Dict]:
        for modulo in self.modulos:
            if modulo.id == modulo_id:
                return modulo.to_dict()
        return None
    
    def get_all_modulos(self) -> List[Dict]:
        return [modulo.to_dict() for modulo in self.modulos]
    
    def update_modulo(self, modulo_id: int, nombre: str = None, codigo: str = None, creditos: int = None, curso: int = None) -> bool:
        for modulo in self.modulos:
            if modulo.id == modulo_id:
                if nombre:
                    modulo.nombre = nombre
                if codigo:
                    modulo.codigo = codigo
                if creditos is not None:
                    modulo.creditos = creditos
                if curso is not None:
                    modulo.curso = curso
                return True
        return False
    
    def delete_modulo(self, modulo_id: int) -> bool:
        for alumno in self.alumnos:
            if modulo_id in alumno.modulos:
                alumno.modulos.remove(modulo_id)
        
        for i, modulo in enumerate(self.modulos):
            if modulo.id == modulo_id:
                self.modulos.pop(i)
                return True
        return False
    
    # Gestión de Matrículas
    def matricular_alumno(self, alumno_id: int, modulo_id: int) -> bool:
        alumno = None
        for a in self.alumnos:
            if a.id == alumno_id:
                alumno = a
                break
        
        if not alumno:
            return False
        
        if not self.get_modulo_by_id(modulo_id):
            return False
        
        if modulo_id in alumno.modulos:
            return False
        
        alumno.modulos.append(modulo_id)
        return True
    
    def desmatricular_alumno(self, alumno_id: int, modulo_id: int) -> bool:
        for alumno in self.alumnos:
            if alumno.id == alumno_id:
                if modulo_id in alumno.modulos:
                    alumno.modulos.remove(modulo_id)
                    return True
                return False
        return False
    
    def get_modulos_alumno(self, alumno_id: int) -> List[Dict]:
        for alumno in self.alumnos:
            if alumno.id == alumno_id:
                modulos_matriculados = []
                for modulo_id in alumno.modulos:
                    modulo = self.get_modulo_by_id(modulo_id)
                    if modulo:
                        modulos_matriculados.append(modulo)
                return modulos_matriculados
        return []


def save_data_to_file(handler: Matricula_handler, filename: str = 'matriculas.json') -> bool:
    try:
        data = {
            'alumnos': handler.get_all_alumnos(),
            'modulos': handler.get_all_modulos()
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error al guardar datos: {e}")
        return False


def load_data_from_file(filename: str = 'matriculas.json') -> Matricula_handler:
    handler = Matricula_handler()
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for modulo_data in data.get('modulos', []):
            modulo = Modulo.from_dict(modulo_data)
            handler.add_modulo(modulo)
        
        for alumno_data in data.get('alumnos', []):
            alumno = Alumno.from_dict(alumno_data)
            handler.add_alumno(alumno)
        
        return handler
    except FileNotFoundError:
        return handler
    except Exception as e:
        print(f"Error al cargar datos: {e}")
        return handler