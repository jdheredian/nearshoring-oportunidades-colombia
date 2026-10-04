"""
download.py

Editor: Juan Diego Heredia - juandiegoheredianino@gmail.com
Agosto 2026
"""

import pathlib
import urllib.parse
import urllib.request
import urllib.error

destino = pathlib.Path(__file__).resolve().parent

print("pega la url de cada archivo de fuente, enter vacio para terminar")
print("conviene bajar todos los pesos, matplotlib no fabrica la negrita")

while True:
    url = input("url: ").strip()
    if not url:
        break

    # la url que muestra github al abrir el archivo es una pagina html, no el .ttf
    url = url.replace("github.com/", "raw.githubusercontent.com/").replace("/blob/", "/")
    nombre = urllib.parse.unquote(url.split("/")[-1])

    try:
        datos = urllib.request.urlopen(url, timeout=30).read()
    except urllib.error.HTTPError as error:
        print(f"no encontrada, error {error.code}, revisar la url")
        continue
    except urllib.error.URLError:
        print("sin conexion")
        break

    # sin esto un html guardado como .ttf rompe el import de config en todos los notebooks
    if not datos.startswith((b"\x00\x01\x00\x00", b"OTTO", b"true", b"ttcf")):
        print("eso no es un archivo de fuente, revisar la url")
        continue

    (destino / nombre).write_bytes(datos)
    print(f"descargada {nombre}")
