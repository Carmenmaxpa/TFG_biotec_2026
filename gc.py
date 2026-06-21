import pandas as pd
import numpy as np

def calcular_gc_monofasta(fasta_input, output_file, window_size=100):
    # 1. Leer la única secuencia del archivo FASTA
    id_secuencia = ""
    lineas_secuencia = []

    with open(fasta_input, 'r') as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            if linea.startswith('>'):
                # Guardamos el ID por si TBtools lo necesita en la primera columna
                id_secuencia = linea[1:].split()[0]
            else:
                lineas_secuencia.append(linea)

    # Juntamos todo en una sola cadena de texto en mayúsculas
    secuencia_completa = "".join(lineas_secuencia).upper()
    longitud_total = len(secuencia_completa)

    print(f"Secuencia detectada: {id_secuencia}")
    print(f"Longitud total del genoma: {longitud_total} pb")

    # 2. Generar las ventanas de 100 pb exactamente hasta el final
    starts = np.arange(1, longitud_total + 1, window_size)
    resultados = []

    for start in starts:
        end = start + window_size - 1
        if end > longitud_total:
            end = longitud_total  # Reajuste estricto de la última ventana para TBtools

        # Extraer el fragmento (en Python los índices empiezan en 0)
        fragmento = secuencia_completa[start - 1 : end]
        longitud_fragmento = len(fragmento)

        # 3. Calcular el % de GC
        if longitud_fragmento > 0:
            conteo_g = fragmento.count('G')
            conteo_c = fragmento.count('C')
            porcentaje_gc = ((conteo_g + conteo_c) / longitud_fragmento) * 100
        else:
            porcentaje_gc = 0.0

        # Guardar la fila con el formato requerido
        resultados.append({
            'ID': id_secuencia,
            'start_ventana': start,
            'end_ventana': end,
            'GC_porcentaje': round(porcentaje_gc, 2),
            'color': 'green'  # Color por defecto para que TBtools no de error
        })

    # 4. Convertir a DataFrame y guardar en el archivo de salida (.txt)
    df_final = pd.DataFrame(resultados)
    df_final.to_csv(output_file, sep='\t', index=False)
    print(f"¡Listo! Archivo de densidad GC guardado en: {output_file}")

# =====================================================================
# EJECUCIÓN DEL SCRIPT
# Pon aquí el nombre exacto de tu archivo FASTA actual
# =====================================================================
calcular_gc_monofasta('MORINGASTN.pltd.ctg_kenya (2).fasta', 'resultado_MST_PLTD_GC_100pb.txt')
