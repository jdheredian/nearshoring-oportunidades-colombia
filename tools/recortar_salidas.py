"""
Recorta las salidas de texto desmedidas que quedan embebidas en los notebooks.

Algunos pasos de la cadena imprimen una linea por cada combinacion que procesan. En
`03_models/02_episodios` eso son 23.313 bloques y 23 MB dentro del .ipynb, que vuelven el
archivo inmanejable sin aportar nada: es un registro de avance, no un resultado.

Este script conserva las primeras y ultimas lineas de cada salida y reemplaza el resto por
una marca explicita. No toca el codigo de las celdas ni ninguna salida que no sea texto:
las tablas, las figuras y los resumenes impresos quedan intactos.

    python tools/recortar_salidas.py [--limite BYTES] [--lineas N]
"""
import argparse
import json
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[1]


def recortar_texto(texto, lineas):
    partes = texto.splitlines(keepends=True)
    if len(partes) <= lineas * 2:
        return texto
    omitidas = len(partes) - lineas * 2
    marca = f"\n[... {omitidas:,} lineas omitidas por tools/recortar_salidas.py ...]\n\n"
    return "".join(partes[:lineas]) + marca + "".join(partes[-lineas:])


def main(limite, lineas):
    total_antes = total_despues = 0
    for ruta in sorted(RAIZ.joinpath("notebooks").rglob("*.ipynb")):
        nb = json.loads(ruta.read_text(encoding="utf-8"))
        tocado = False
        for celda in nb["cells"]:
            salidas = celda.get("outputs")
            if not salidas:
                continue
            # las salidas de texto de una misma celda llegan troceadas: se juntan para medirlas
            texto = "".join(
                "".join(s.get("text", []))
                for s in salidas
                if s.get("output_type") == "stream"
            )
            if len(texto) <= limite:
                continue
            otras = [s for s in salidas if s.get("output_type") != "stream"]
            celda["outputs"] = [
                {"output_type": "stream", "name": "stdout",
                 "text": recortar_texto(texto, lineas).splitlines(keepends=True)}
            ] + otras
            tocado = True
        if tocado:
            antes = ruta.stat().st_size
            ruta.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
            despues = ruta.stat().st_size
            total_antes += antes
            total_despues += despues
            print(f"  {ruta.relative_to(RAIZ)}: {antes/1048576:.1f} MB -> {despues/1048576:.1f} MB")
    if total_antes:
        print(f"\ntotal: {total_antes/1048576:.1f} MB -> {total_despues/1048576:.1f} MB")
    else:
        print("  ningun notebook supera el limite")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--limite", type=int, default=200_000, help="bytes de texto a partir de los cuales se recorta")
    p.add_argument("--lineas", type=int, default=20, help="lineas que se conservan al inicio y al final")
    args = p.parse_args()
    main(args.limite, args.lineas)
