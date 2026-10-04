#!/usr/bin/env bash
# Corre la cadena completa desde data/raw, en orden de dependencia.
#
# Borra data/temp y data/processed antes de empezar: es la prueba de que no quedan
# dependencias ocultas entre notebooks ni artefactos que sobrevivan de corridas
# anteriores. data/raw no se toca.
#
# Uso:  ./tools/correr_cadena.sh [--conservar]
#       --conservar  no borra data/temp ni data/processed

set -uo pipefail
cd "$(dirname "$0")/.."

PYTHON=.venv/bin/python
JUPYTER=.venv/bin/jupyter
REGISTRO="logs/cadena_$(date +%Y%m%d_%H%M%S).log"
mkdir -p logs

if [[ "${1:-}" != "--conservar" ]]; then
    echo "Limpiando data/temp y data/processed..."
    find data/temp data/processed -mindepth 1 -not -name '.gitkeep' -delete 2>/dev/null
fi

fallidos=0
inicio_total=$SECONDS

# Solo los notebooks de las carpetas numeradas: los que cuelgan directamente de
# notebooks/ son plantillas, no pasos de la cadena.
for cuaderno in $(find notebooks/*/ -name '*.ipynb' -not -path '*/.ipynb_checkpoints/*' | sort); do
    inicio=$SECONDS
    printf '%-58s ' "$cuaderno"
    if $JUPYTER nbconvert --to notebook --execute --inplace \
            --ExecutePreprocessor.timeout=-1 "$cuaderno" >> "$REGISTRO" 2>&1; then
        printf 'OK   %5ds\n' "$((SECONDS - inicio))"
    else
        printf 'FALLA %4ds\n' "$((SECONDS - inicio))"
        echo "  -> el detalle esta en $REGISTRO"
        fallidos=$((fallidos + 1))
        break
    fi
done

echo
echo "Tiempo total: $(( (SECONDS - inicio_total) / 60 )) min"
if [[ $fallidos -eq 0 ]]; then
    echo "La cadena corrio completa. Ahora: $PYTHON tools/verificar_migracion.py"
else
    echo "La cadena se detuvo en el primer fallo."
fi
exit $fallidos
