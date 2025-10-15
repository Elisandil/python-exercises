from functools import reduce
import csv

print("\n")
print("EJERCICIO 1: Cuadrado y cubo de números")
print("\n")
numeros = list(range(1, 10))
resultado = list(map(lambda x: (x**2, x**3), numeros))
print(f"Lista original: {numeros}")
print(f"Resultado (cuadrado, cubo): {resultado}")

print("\n")
print("EJERCICIO 2: Filtrar valores numéricos válidos")
print("\n")
lista_mixta = [10, "error", 25, None, 30, "?", 40]
numeros_validos = list(filter(lambda x: isinstance(x, (int, float)) and x is not None, lista_mixta))
print(f"Lista original: {lista_mixta}")
print(f"Valores numéricos válidos: {numeros_validos}")

print("\n")
print("EJERCICIO 3: Promedio con reduce")
print("\n")
numeros = list(range(1, 50, 10))
suma = reduce(lambda acc, x: acc + x, numeros)
cantidad = reduce(lambda acc, x: acc + 1, numeros, 0)
promedio = suma / cantidad
print(f"Lista: {numeros}")
print(f"Suma: {suma}")
print(f"Cantidad: {cantidad}")
print(f"Promedio: {promedio}")

print("\n")
print("EJERCICIO 4: Ordenar cadenas")
print("\n")
palabras = ["Python", "javascript", "Java", "C", "Ruby", "Go"]
print(f"Lista original: {palabras}")

# Por longitud
por_longitud = sorted(palabras, key=lambda x: len(x))
print(f"Ordenadas por longitud: {por_longitud}")

# Alfabéticamente ignorando mayúsculas
alfabeticamente = sorted(palabras, key=lambda x: x.lower())
print(f"Ordenadas alfabéticamente: {alfabeticamente}")

print("\n")
print("EJERCICIO 5: Análisis de ventas.csv")
print("\n")

# Leer el archivo ventas.csv usando solo lambdas y map
with open('ventas.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    ventas = list(map(lambda row: {
        'producto': row['producto'],
        'categoria': row['categoria'],
        'precio': float(row['precio']),
        'cantidad': int(row['cantidad'])
    }, reader))

# 1. Total vendido por producto
totales = list(map(lambda v: {
    'producto': v['producto'],
    'total': v['precio'] * v['cantidad']
}, ventas))

print("1. Total vendido por producto:")
list(map(lambda item: print(f"{item['producto']}: {item['total']:.2f} €"), totales))

# 2. Filtrar ventas > 100€
ventas_mayores = list(filter(lambda v: v['precio'] * v['cantidad'] > 100, ventas))
print("\n2. Productos con ventas mayores a 100 €:")
list(map(lambda v: print(f"{v['producto']}: {v['precio'] * v['cantidad']:.2f} €"), ventas_mayores))

# 3. Suma total con reduce
suma_total = reduce(lambda acc, v: acc + (v['precio'] * v['cantidad']), ventas, 0)
print(f"\n3. Suma total de ventas: {suma_total:.2f} €")

print("\n")
print("EJERCICIO 6: Análisis de personas.csv")
print("\n")

# Leer personas.csv usando solo lambdas
with open('personas.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    personas = list(map(lambda row: {
        'nombre': row['nombre'],
        'edad': int(row['edad']),
        'ciudad': row['ciudad']
    }, reader))

# 1. Mayores de edad
mayores_edad = list(filter(lambda p: p['edad'] >= 18, personas))
print("1. Personas mayores de edad (≥18):")
list(map(lambda p: print(f"   {p['nombre']}, {p['edad']} años"), mayores_edad))

# 2. Personas de Madrid
de_madrid = list(filter(lambda p: p['ciudad'] == 'Madrid', personas))
print("\n2. Personas que viven en Madrid:")
list(map(lambda p: print(f"   {p['nombre']}, {p['edad']} años"), de_madrid))

# 3. Combinación: mayores de edad Y de Madrid
mayores_madrid = list(filter(lambda p: p['edad'] >= 18 and p['ciudad'] == 'Madrid', personas))
print("\n3. Personas mayores de edad que viven en Madrid:")
list(map(lambda p: print(f"   {p['nombre']}, {p['edad']} años"), mayores_madrid))

print("\n")
print("EJERCICIO 7: Análisis de temperaturas.csv")
print("\n")

# Leer temperaturas.csv usando solo lambdas
with open('temperaturas.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    temperaturas = list(map(lambda row: {
        'ciudad': row['ciudad'],
        'celsius': int(row['temperatura'])
    }, reader))

# 1. Convertir a Fahrenheit
en_fahrenheit = list(map(lambda t: {
    'ciudad': t['ciudad'],
    'celsius': t['celsius'],
    'fahrenheit': t['celsius'] * 9/5 + 32
}, temperaturas))

print("1. Temperaturas en Fahrenheit:")
list(map(lambda t: print(f"   {t['ciudad']}: {t['celsius']}°C = {t['fahrenheit']:.1f}°F"), en_fahrenheit))

# 2. Ciudades con temperatura > 25°C
calurosas = list(filter(lambda t: t['celsius'] > 25, temperaturas))
print("\n2. Ciudades con temperatura superior a 25°C:")
list(map(lambda t: print(f"   {t['ciudad']}: {t['celsius']}°C"), calurosas))

# 3. Temperatura media con reduce
suma_temp = reduce(lambda acc, t: acc + t['celsius'], temperaturas, 0)
cantidad_temp = reduce(lambda acc, t: acc + 1, temperaturas, 0)
temp_media = suma_temp / cantidad_temp
print(f"\n3. Temperatura media: {temp_media:.2f}°C")