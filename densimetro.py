import pandas as pd
import numpy as np

def calcular_densidad_ventanas(input_file, output_file):
    # 1. Cargar los datos
    # Cambia header=0 si tu archivo ya tiene la cabecera (ID, start, end, color)
    # Si no tiene cabecera, usa header=None
    columnas = ['ID', 'start', 'end', 'color']
    df = pd.read_csv(input_file, sep='\t', names=columnas, header=0)

    # 2. Filtrar: Ignorar 'MITO' y asegurarnos de trabajar solo con 'PLTD'
    df = df[~df['ID'].str.contains('MITO', na=False)].copy()
    df_filtered = df[df['ID'].isin(['MST_PLTD', 'MOL_PLTD'])].copy()

    # 3. Definir longitudes exactas y tamaño de ventana
    chr_lengths = {
        'MST_PLTD': 160506,
        'MOL_PLTD': 160600
    }
    window_size = 500

    # 4. Crear el "Esqueleto" de todas las ventanas posibles
    all_windows = []
    for seq_id, length in chr_lengths.items():
        # Inicios: 1, 501, 1001, etc.
        starts = np.arange(1, length + 1, window_size)
        # Finales: 500, 1000, 1500, etc.
        ends = starts + window_size - 1

        # CRÍTICO: Ajustar el último "end" para que sea exactamente el final del cromosoma
        ends[-1] = length

        for s, e in zip(starts, ends):
            all_windows.append({
                'ID': seq_id,
                'start_ventana': s,
                'end_ventana': e
            })

    df_esqueleto = pd.DataFrame(all_windows)

    # 5. Asignar cada fila de tus datos reales a su ventana correspondiente
    # Usamos matemática entera para ubicar el 'start' en su caja de 500pb
    df_filtered['start_ventana'] = ((df_filtered['start'] - 1) // window_size) * window_size + 1
    df_filtered['end_ventana'] = df_filtered['start_ventana'] + window_size - 1

    # Ajustar también el end_ventana de los datos si caen en la última ventana (truncada)
    def ajustar_end_datos(row):
        max_len = chr_lengths.get(row['ID'], 0)
        return min(row['end_ventana'], max_len)

    df_filtered['end_ventana'] = df_filtered.apply(ajustar_end_datos, axis=1)

    # 6. Agrupar los datos para calcular la densidad
    # Si hay varios colores en una sola ventana de 500pb, por defecto cogerá el primero ('first')
    df_agrupado = df_filtered.groupby(['ID', 'start_ventana', 'end_ventana']).agg(
        Valor_ventana=('start', 'count'),
        color=('color', 'first')
    ).reset_index()

    # 7. Unir el esqueleto completo con los datos calculados (Left Join)
    df_final = pd.merge(df_esqueleto, df_agrupado, on=['ID', 'start_ventana', 'end_ventana'], how='left')

    # 8. Limpiar los datos (Ceros para ventanas sin genes y color por defecto)
    df_final['Valor_ventana'] = df_final['Valor_ventana'].fillna(0).astype(int)

    # TBtools puede fallar si la columna color está vacía (NaN). Le asignamos un gris a las zonas de densidad 0.
    # Puedes cambiar '#E0E0E0' al color hexadecimal o nombre (ej. 'white') que prefieras.
    df_final['color'] = df_final['color'].fillna('#E0E0E0')

    # 9. Guardar el archivo listo para TBtools
    df_final.to_csv(output_file, sep='\t', index=False)
    print(f"¡Listo! Archivo procesado y guardado en: {output_file}")

    return df_final
calcular_densidad_ventanas('Moringa_Tandem_tbtools.txt', 'resultado_PLTD.txt')

# Para ejecutarlo solo tienes que llamar a la función con tus rutas:
# calcular_densidad_ventanas('mis_datos_genomicos.txt', 'datos_para_tbtools.txt')
