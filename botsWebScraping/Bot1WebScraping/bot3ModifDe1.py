import csv
import requests
from bs4 import BeautifulSoup

def extraer_direccion(link, id_exhibidor):
    try:
        # Verificar si la URL está presente
        if not link:
            print(f"URL vacía para ID_exhibidor {id_exhibidor}")
            return

        # Realizar la solicitud HTTP
        print(f'Enlace para ID_exhibidor {row["ID_exhibidor"]}: {row["enlace"]}')

        response = requests.get(link)
        response.raise_for_status()

        # Analizar el contenido HTML de la página
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar elementos con la clase "address"
        direcciones = soup.find_all(class_='address')

        # Extraer y guardar las direcciones en un archivo CSV
        if direcciones:
            with open('direcciones.csv', 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['ID_exhibidor', 'Enlace', 'Dirección']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                for direccion in direcciones:
                    writer.writerow({'ID_exhibidor': id_exhibidor, 'Enlace': link, 'Dirección': direccion.text.strip()})
    except Exception as e:
        print(f"Error en {link}: {str(e)}")

# Leer enlaces desde un archivo CSV
with open('enlaces.csv', 'r', newline='', encoding='latin-1') as enlaces_file:
    reader = csv.DictReader(enlaces_file, delimiter=';')
    enlaces = [(row.get('ID_exhibidor', ''), row.get('enlace', '')) for row in reader]

# Crear o truncar el archivo CSV antes de comenzar
with open('direcciones.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['ID_exhibidor', 'Enlace', 'Dirección']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

# Iterar sobre cada enlace y extraer direcciones
for id_exhibidor, enlace in enlaces:
    extraer_direccion(enlace, id_exhibidor)
