import pandas as pd
import numpy as np

def calcular_densidad_desde_csv_fijo(input_csv, output_txt):
    # 1. Cargar el archivo CSV
    df = pd.read_csv(input_csv, sep=',')
    df.columns = df.columns.str.strip()

    print(f"Columnas detectadas en el archivo: {list(df.columns)}")
    print(f"Filas totales originales: {len(df)}")

    # 2. IDENTIFICACIÓN INTELIGENTE DE COLUMNAS
    # Buscamos cuál es la columna del ID (la que contiene PLTD o MITO)
    col_id = df.columns[0] # Por defecto la primera

    # Buscamos las columnas numéricas para Start y End
    # Intentamos convertirlas dinámicamente para saber cuáles son las coordenadas
    columnas_numericas = []
    for col in df.columns:
        # Si se puede convertir a número, es una coordenada
        if pd.to_numeric(df[col], errors='coerce').notna().sum() > len(df) * 0.5:
            columnas_numericas.append(col)

    if len(columnas_numericas) >= 2:
        col_start = columnas_numericas[0]
        col_end = columnas_numericas[1]
    else:
        # Si el truco automático falla, usamos las posiciones típicas del final (penúltima y última)
        print("Aviso: No se detectaron cabeceras numéricas claras, usando las dos últimas columnas.")
        col_start = df.columns[-2]
        col_end = df.columns[-1]

    print(f"-> Usando mapeo estricto => ID: '{col_id}' | START: '{col_start}' | END: '{col_end}'")

    # 3. Filtrar de forma estricta: Ignorar 'MITO' y quedarnos solo con 'PLTD'
    df[col_id] = df[col_id].astype(str)
    df = df[~df[col_id].str.contains('MITO', na=False)].copy()
    df_filtered = df[df[col_id].isin(['MST_PLTD', 'MOL_PLTD'])].copy()

    print(f"Filas tras filtrar PLTD (excluyendo MITO): {len(df_filtered)}")

    # 4. Definir longitudes exactas y tamaño de ventana (500 pb)
    chr_lengths = {
        'MST_PLTD': 160506,
        'MOL_PLTD': 160600
    }
    window_size = 500

    # 5. Crear el "Esqueleto" de ventanas perfectas para TBtools
    all_windows = []
    for seq_id, length in chr_lengths.items():
        starts = np.arange(1, length + 1, window_size)
        ends = starts + window_size - 1
        ends[-1] = length  # Ajuste estricto del final del cromosoma

        for s, e in zip(starts, ends):
            all_windows.append({
                'ID': seq_id,
                'start_ventana': s,
                'end_ventana': e
            })

    df_esqueleto = pd.DataFrame(all_windows)

    # 6. Forzar las coordenadas a enteros limpios pasando de largo cualquier texto corrupto
    df_filtered[col_start] = pd.to_numeric(df_filtered[col_start], errors='coerce').astype(int)

    # 7. Asignar cada gen a su ventana correspondiente basado en su 'Start'
    df_filtered['start_ventana'] = ((df_filtered[col_start] - 1) // window_size) * window_size + 1
    df_filtered['end_ventana'] = df_filtered['start_ventana'] + window_size - 1

    # Ajustar el final de la ventana si desborda el cromosoma
    def ajustar_end_datos(row):
        max_len = chr_lengths.get(row[col_id], 0)
        return min(row['end_ventana'], max_len)

    df_filtered['end_ventana'] = df_filtered.apply(ajustar_end_datos, axis=1)

    # 8. Agrupar para contar la densidad
    df_agrupado = df_filtered.groupby([col_id, 'start_ventana', 'end_ventana']).size().reset_index(name='Valor_ventana')
    df_agrupado = df_agrupado.rename(columns={col_id: 'ID'})

    # 9. Combinar el esqueleto completo con los conteos (Left Join)
    df_final = pd.merge(df_esqueleto, df_agrupado, on=['ID', 'start_ventana', 'end_ventana'], how='left')

    # 10. Rellenar vacíos (0 para densidad y rojo por defecto)
    df_final['Valor_ventana'] = df_final['Valor_ventana'].fillna(0).astype(int)
    df_final['color'] = 'red'

    # 11. Guardar resultado final para TBtools
    df_final.to_csv(output_txt, sep='\t', index=False)

    print(f"---")
    print(f"¡Solucionado! Archivo de densidad generado con éxito.")
    print(f"Salida guardada en: {output_txt}")
    return df_final

# =====================================================================
# EJECUCIÓN
# =====================================================================
calcular_densidad_desde_csv_fijo('M_stenopetala_kenya_PT_limpio.csv', 'densidad_genes_MST_PLTD.txt')
