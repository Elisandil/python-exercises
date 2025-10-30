import re

def validar_email(email: str) -> bool:
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None


def validar_entero(valor: str) -> bool:

    try:
        int(valor)
        return True
    except ValueError:
        return False


def validar_entero_positivo(valor: str) -> bool:

    if validar_entero(valor):
        return int(valor) > 0
    return False


def solicitar_entero(mensaje: str, min_val: int = None, max_val: int = None) -> int:

    while True:
        entrada = input(mensaje)
        if validar_entero(entrada):
            valor = int(entrada)
            if min_val is not None and valor < min_val:
                print(f"El valor debe ser mayor o igual a {min_val}")
                continue
            if max_val is not None and valor > max_val:
                print(f"El valor debe ser menor o igual a {max_val}")
                continue
            return valor
        else:
            print("Por favor, introduce un número válido.")


def solicitar_texto(mensaje: str, min_length: int = 1) -> str:

    while True:
        entrada = input(mensaje).strip()
        if len(entrada) >= min_length:
            return entrada
        else:
            print(f"El texto debe tener al menos {min_length} caracteres.")


def solicitar_email(mensaje: str) -> str:

    while True:
        entrada = input(mensaje).strip()
        if validar_email(entrada):
            return entrada
        else:
            print("Por favor, introduce un email válido (ej: usuario@dominio.com).")


def confirmar_accion(mensaje: str) -> bool:

    while True:
        respuesta = input(f"{mensaje} (S/N): ").strip().upper()
        if respuesta in ['S', 'SI', 'SÍ']:
            return True
        elif respuesta in ['N', 'NO']:
            return False
        else:
            print("Por favor, responde S (sí) o N (no).")


def limpiar_pantalla():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    input("\nPresiona Enter para continuar...")


def mostrar_tabla(headers: list, rows: list, titulo: str = None):

    if titulo:
        print(f"\n{'=' * 80}")
        print(f"{titulo:^80}")
        print('=' * 80)
    
    if not rows:
        print("No hay datos para mostrar.")
        return
    
    anchos = [len(str(header)) for header in headers]
    for row in rows:
        for i, cell in enumerate(row):
            anchos[i] = max(anchos[i], len(str(cell)))
    
    header_row = " | ".join(str(headers[i]).ljust(anchos[i]) for i in range(len(headers)))
    print(f"\n{header_row}")
    print("-" * len(header_row))
    
    for row in rows:
        print(" | ".join(str(row[i]).ljust(anchos[i]) for i in range(len(row))))
    
    print()


def generar_id_unico(lista_existente: list) -> int:

    if not lista_existente:
        return 1
    ids = [item['id'] for item in lista_existente]
    return max(ids) + 1