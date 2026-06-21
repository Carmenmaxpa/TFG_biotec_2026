import pandas as pd

def extraer_genes_repetidos(input_csv, output_csv):
    # 1. Cargar el archivo CSV
    # Si tu archivo está separado por comas, déjalo así.
    # Si está separado por tabuladores, cambia sep=',' por sep='\t'
    df = pd.read_csv(input_csv, sep=',')

    # Suponiendo que la primera columna contiene los nombres de los genes.
    # Si tus columnas tienen nombres distintos (ej. 'gene_id'), cámbialo aquí:
    columna_genes = df.columns[0]

    print(f"Analizando duplicados basados en la columna: '{columna_genes}'")
    print(f"Total de registros iniciales: {len(df)}")

    # 2. Filtrar los que están repetidos
    # keep=False es el truco clave aquí: asegura que si un gen aparece 2 veces,
    # se guarden AMBAS filas en el resultado para que puedas comparar sus coordenadas.
    df_repetidos = df[df.duplicated(subset=[columna_genes], keep=False)].copy()

    # 3. Ordenar por el nombre del gen para que los repetidos salgan juntos
    df_repetidos = df_repetidos.sort_values(by=[columna_genes])

    # 4. Guardar el nuevo CSV
    df_repetidos.to_csv(output_csv, index=False, sep=',')

    print(f"¡Proceso completado!")
    print(f"Se han encontrado {df_repetidos[columna_genes].nunique()} genes repetidos.")
    print(f"Total de filas duplicadas guardadas: {len(df_repetidos)}")
    print(f"Archivo guardado en: {output_csv}")

# =====================================================================
# EJECUCIÓN DEL SCRIPT
# Cambia los nombres por tus archivos reales
# =====================================================================
extraer_genes_repetidos('M_stenopetala_kenya_PT_limpio.csv', 'genes_MST_PLTDrepetidos.csv')
