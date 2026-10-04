#!/usr/bin/env bash
#
# Copia los insumos crudos desde OneDrive a data/raw/.
#
#   ./tools/copiar_raw.sh
#
# Es idempotente: omite lo que ya esta copiado con el mismo tamano, de modo que se
# puede relanzar tras una interrupcion.
#
# OneDrive guarda estos archivos como marcadores en la nube. Antes de correr esto
# conviene marcar la carpeta de origen como "Mantener siempre en este dispositivo"
# en Finder y esperar a que termine de bajar: de lo contrario cada copia dispara una
# materializacion individual, que es lenta y puede bloquear el proveedor de archivos.
set -u

ORIG="/Users/juandiegoheredianino/Library/CloudStorage/OneDrive-Fedesarrollo/David Gelvez & Rafael Puyana/Nearshoring"
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
D="$RAIZ/data/raw"

CAR="$ORIG/Caracterización"
IMP="$ORIG/Impacto"
AE="$ORIG/Archivos Extra"
AMC="$ORIG/AmCham"
EXC="$ORIG/Excel Impacto PIB"

copiar() {  # copiar <archivo origen> <carpeta destino>
    local destino="$2/$(basename "$1")"
    mkdir -p "$2"
    if [ ! -e "$1" ]; then
        echo "  AUSENTE  $1"
        return
    fi
    if [ -f "$destino" ] && [ "$(stat -f%z "$destino")" = "$(stat -f%z "$1")" ]; then
        echo "  ya esta  $(basename "$1")"
        return
    fi
    if cp -p "$1" "$destino"; then
        echo "  ok       $(basename "$1")"
    else
        echo "  FALLA    $(basename "$1")"
    fi
}

copiar_carpeta() {  # copiar_carpeta <carpeta origen> <carpeta destino>
    mkdir -p "$2"
    if rsync -a --ignore-existing --exclude '.DS_Store' --exclude '__pycache__' "$1/" "$2/"; then
        echo "  ok       $(basename "$1")/  ($(find "$2" -type f | wc -l | tr -d ' ') archivos)"
    else
        echo "  FALLA    $(basename "$1")/"
    fi
}

echo "== comercio =="
for f in wits.parquet df_comercio_mundial.parquet df_BEC.parquet df_info_calidad.parquet; do
    copiar "$CAR/raw data/$f" "$D/comercio"
done
copiar_carpeta "$CAR/raw data/Correlativas HS" "$D/comercio/correlativas"
for f in "FIXEDLeamer HS 2012 to SITC Rev.4 Correlation and conversion tables 2.xls" \
         "Leamer HS 2012 to SITC Rev.4 Correlation and conversion tables (1).xls" \
         "HS Missing Leamer - Fixed.xlsx"; do
    copiar "$CAR/raw data/$f" "$D/comercio/correlativas"
done
copiar "$IMP/data/raw/exportaciones/productos/HS 2012 to HS 1996 Correlation and conversion tables.xls" "$D/comercio/correlativas"

echo "== clasificacion industrial =="
copiar "$CAR/raw data/EstructuraDetalladaCIIU_4AC.xls" "$D/ciiu"
copiar "$CAR/raw data/anex-DIRPEN-TOTPARTv76-ago2024.xlsx" "$D/ciiu"
copiar "$CAR/data/ciiu3.parquet" "$D/ciiu"
copiar "$IMP/Priorización/data/raw/CIIU_Clasificacion_Actualizada.xlsx" "$D/ciiu"
for f in "CIIU-básico.xlsx" "CIIU-complementado.xlsx" "CIIU-complemento.xlsx" "CIIU VA - Básico.xlsx"; do
    copiar "$IMP/data/raw/pib/$f" "$D/ciiu"
done

echo "== aranceles y medidas no arancelarias =="
copiar "$CAR/raw data/tariffs.parquet" "$D/aranceles"
copiar "$CAR/raw data/Aranceles Trump.xlsx" "$D/aranceles"
copiar_carpeta "$CAR/raw data/NTMS" "$D/aranceles/ntms"

echo "== potencial exportador =="
copiar "$CAR/raw data/Potencial Exportador/ISO ITC Treemap.xlsx" "$D/potencial_exportador"
copiar_carpeta "$CAR/raw data/Potencial Exportador/country data" "$D/potencial_exportador/country_data"

echo "== formulario 600 =="
copiar_carpeta "$CAR/raw data/2023 F600" "$D/formulario600/2023"
copiar "$CAR/raw data/df_600.parquet" "$D/formulario600"

echo "== logistica =="
copiar "$CAR/raw data/rndc.parquet" "$D/logistica"
copiar "$AE/df_costos_externos.parquet" "$D/logistica"
copiar "$AE/Registro_Nacional_de_Despachos_de_Carga_por_Carretera_20250530.csv" "$D/logistica"

echo "== resiliencia e insumos de terceros =="
copiar "$CAR/raw data/Estrategias de resiliencia.xlsx" "$D/resiliencia"
copiar_carpeta "$CAR/input data" "$D/insumos"

echo "== amcham =="
for f in "AmChamColombia-EEUU-Oportunidades-EstudioVCR 2025 copia.xlsx" \
         "AmChamColombia-EEUU-Oportunidades-EstudioVCR 2025 copia.pdf" \
         "AmChamOverLap.xlsx" "AmChamOverLap2.xlsx"; do
    copiar "$AMC/$f" "$D/amcham"
done

echo "== exportaciones: series de WITS (7,4 GB, 27 archivos) =="
copiar_carpeta "$IMP/data/raw/exportaciones/comercio" "$D/exportaciones/comercio"
for sub in controles "cortes de datos" gdp otros_paises; do
    copiar_carpeta "$IMP/data/raw/exportaciones/$sub" "$D/exportaciones/$sub"
done
copiar "$IMP/data/raw/exportaciones/productos/2 - Output Final 040725 V02 - EXT.xlsx" "$D/exportaciones/productos"

echo "== cuentas nacionales y matriz insumo-producto =="
for f in "anex-MIP-2019.xlsx" "anex-CuentasNalANuales-OfertaUtilizacionPreciosCorrientes-2023p.xlsx"; do
    copiar "$IMP/data/raw/pib/$f" "$D/pib"
done
copiar_carpeta "$IMP/data/raw/pib/VA" "$D/pib/VA"

echo "== resultados numericos en excel =="
copiar_carpeta "$EXC" "$D/impacto_excel"

echo "== descargas WITS de comentarios =="
copiar_carpeta "$IMP/data/raw/comentarios" "$D/comentarios"
copiar_carpeta "$IMP/data/processed/comentarios/3004985_1C4043D0-F" "$D/comentarios/3004985_1C4043D0-F"

echo "== insumos sin productor (ver AUDITORIA_MIGRACION.md, hallazgo 2.5) =="
copiar "$IMP/Priorización/data/raw/indices_normalizados_20anios.xlsx" "$D/modelo"
copiar "$IMP/df_trade_share.parquet" "$D/modelo"
copiar "$IMP/df_hat_basic.parquet" "$D/modelo"

echo "== tipografia =="
copiar "$CAR/raw data/Fuente/Aptos.ttf" "$RAIZ/tools/fonts"

echo
echo "== FIN =="
du -sh "$D"
