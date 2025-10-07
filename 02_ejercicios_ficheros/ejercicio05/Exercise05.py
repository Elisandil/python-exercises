import json
import csv

with open('./notas.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

print("Medias de los alumnos:")
print("-" * 30)

results = []

for alumni, qualifications in data.items():
    average = sum(qualifications) / len(qualifications)
    print(f"{alumni}: {average:.2f}")
    results.append([alumni, average])

with open('medias.csv', 'w', newline='', encoding='utf-8') as archivo_csv:
    writer = csv.writer(archivo_csv)
    writer.writerow(['nombre', 'nota_media'])
    writer.writerows(results)