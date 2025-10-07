import csv
from collections import defaultdict

def procesar_ventas(archivo_entrada='ventas.csv', output_file='resumen.csv'):
    """
    Lee un archivo CSV de ventas, calcula totales por producto y genera un resumen.
    
    Args:
        archivo_entrada: Nombre del archivo CSV de entrada
        archivo_salida: Nombre del archivo CSV de salida
    """
    sales_per_product = defaultdict(float)
    
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                product = row['producto']
                quatity = float(row['cantidad'])
                price_per_unit = float(row['precio_unitario'])
                total = quatity * price_per_unit
                sales_per_product[product] += total
        
        print("=" * 50)
        print("RESUMEN DE VENTAS POR PRODUCTO")
        print("=" * 50)
        print(f"{'Producto':<20} {'Total Ventas':>20}")
        print("-" * 50)
        total = 0

        for product, total in sorted(sales_per_product.items()):
            print(f"{product:<20} ${total:>14.2f}")
            total += total
        
        print("-" * 50)
        print(f"{'TOTAL GENERAL':<20} ${total:>14.2f}")
        print("=" * 50)
        
        with open(output_file, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['producto', 'total_ventas'])

            for product, total in sorted(sales_per_product.items()):
                writer.writerow([product, f'{total:.2f}'])
        
        print(f"\n✓ Resumen guardado exitosamente en '{output_file}'")
        
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo_entrada}'")
    except Exception as e:
        print(f"Error inesperado: {e}")

def main():
    procesar_ventas()

main()