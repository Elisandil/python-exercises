# Análisis de Datos de Personas
import csv

people = []

with open('personas.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        person = {
            'nombre': row['nombre'],
            'edad': int(row['edad']),
            'altura': float(row['altura']),
            'peso': float(row['peso']),
            'localidad': row['localidad']
        }
        people.append(person)

print("=" * 60)
print(f"Total de personas en el dataset: {len(people)}")

# 1. Media de edad
print("=" * 60)
print("1. ANÁLISIS DE EDAD")
print("=" * 60)
total_age = sum(p['edad'] for p in people)
average_age = total_age / len(people)
print(f"Media de edad: {average_age:.2f} años")
print("\n")

# 2. Persona más joven y más vieja
print("=" * 60)
print("2. PERSONA MÁS JOVEN Y MÁS VIEJA")
print("=" * 60)
youngest_person = min(people, key=lambda p: p['edad'])
oldest_person = max(people, key=lambda p: p['edad'])

print("Persona más joven:")
print(f"  Nombre: {youngest_person['nombre']}")
print(f"  Edad: {youngest_person['edad']} años")
print(f"  Altura: {youngest_person['altura']} m")
print(f"  Peso: {youngest_person['peso']} kg")
print(f"  Localidad: {youngest_person['localidad']}")

print("\nPersona más vieja:")
print(f"  Nombre: {oldest_person['nombre']}")
print(f"  Edad: {oldest_person['edad']} años")
print(f"  Altura: {oldest_person['altura']} m")
print(f"  Peso: {oldest_person['peso']} kg")
print(f"  Localidad: {oldest_person['localidad']}")
print("\n")

# 3. Media de altura
print("=" * 60)
print("3. ANÁLISIS DE ALTURA")
print("=" * 60)
total_height = sum(p['altura'] for p in people)
average_height = total_height / len(people)
print(f"Media de altura: {average_height:.2f} metros")
print("\n")

# 4. Persona más alta y más baja
print("=" * 60)
print("4. PERSONA MÁS ALTA Y MÁS BAJA")
print("=" * 60)
tallest_person = max(people, key=lambda p: p['altura'])
smallest_person = min(people, key=lambda p: p['altura'])

print("Persona más alta:")
print(f"  Nombre: {tallest_person['nombre']}")
print(f"  Edad: {tallest_person['edad']} años")
print(f"  Altura: {tallest_person['altura']} m")
print(f"  Peso: {tallest_person['peso']} kg")
print(f"  Localidad: {tallest_person['localidad']}")

print("\nPersona más baja:")
print(f"  Nombre: {smallest_person['nombre']}")
print(f"  Edad: {smallest_person['edad']} años")
print(f"  Altura: {smallest_person['altura']} m")
print(f"  Peso: {smallest_person['peso']} kg")
print(f"  Localidad: {smallest_person['localidad']}")
print("\n")

# 5. Persona con más peso y menos peso
print("=" * 60)
print("5. PERSONA CON MÁS PESO Y MENOS PESO")
print("=" * 60)
heavier_person = max(people, key=lambda p: p['peso'])
lighter_person = min(people, key=lambda p: p['peso'])

print("Persona con más peso:")
print(f"  Nombre: {heavier_person['nombre']}")
print(f"  Edad: {heavier_person['edad']} años")
print(f"  Altura: {heavier_person['altura']} m")
print(f"  Peso: {heavier_person['peso']} kg")
print(f"  Localidad: {heavier_person['localidad']}")

print("\nPersona con menos peso:")
print(f"  Nombre: {lighter_person['nombre']}")
print(f"  Edad: {lighter_person['edad']} años")
print(f"  Altura: {lighter_person['altura']} m")
print(f"  Peso: {lighter_person['peso']} kg")
print(f"  Localidad: {lighter_person['localidad']}")
print("\n")

# 6. Localidad con más personas
print("=" * 60)
print("6. LOCALIDAD CON MÁS PERSONAS")
print("=" * 60)

total_cities = {}
for person in people:
    city = person['localidad']
    if city in total_cities:
        total_cities[city] += 1
    else:
        total_cities[city] = 1

localidad_max = max(total_cities, key=total_cities.get)
cantidad_max = total_cities[localidad_max]

print(f"Localidad con más personas: {localidad_max}")
print(f"Número de personas: {cantidad_max}")

sorted_cities = sorted(total_cities.items(), key=lambda x: x[1], reverse=True)

print("\nTop 5 localidades con más personas:")
print("-" * 40)
for i, (city, quantity) in enumerate(sorted_cities[:5], 1):
    print(f"{i}. {city}: {quantity} personas")
print("\n")