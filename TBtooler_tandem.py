def convertir_trf_a_tbtools(archivo_entrada, archivo_salida, nombre_cromosoma="MST_PLTD", valor="orange"):
    """
    Convierte la salida de Tandem Repeats Finder (TRF) al formato de pista de TBtools.
    """
    try:
        with open(archivo_entrada, 'r') as f_in, open(archivo_salida, 'w') as f_out:
            # Puedes descomentar la siguiente línea si TBtools te exige el encabezado literal
            # f_out.write("Chr\tStartPos\tEndPos\tValus\n")

            for linea in f_in:
                linea = linea.strip()

                # Ignorar líneas vacías o de encabezado (las de datos siempre empiezan con un número)
                if not linea or not linea[0].isdigit():
                    continue

                # Separar la línea por espacios
                partes = linea.split()

                # Verificar que sea una línea de datos de TRF (tienen unas 15 columnas en total)
                if len(partes) >= 15:
                    start_pos = partes[0]
                    end_pos = partes[1]

                    # Escribir la línea separada por tabulaciones (\t)
                    f_out.write(f"{nombre_cromosoma}\t{start_pos}\t{end_pos}\t{valor}\n")

        print(f"✅ Archivo guardado con éxito en: {archivo_salida}")

    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{archivo_entrada}'.")

# --- INSTRUCCIONES DE USO ---
# 1. Pon el nombre de tu archivo .txt original aquí
archivo_trf = "Tandem_Repeats_MST_PLTD.txt"

# 2. Pon el nombre del archivo que quieres generar para TBtools
archivo_tbtools = "MST_PLTD_Tandem_tbtools.txt"

# 3. Cambia "MOL_MITO" por el nombre de tu cromosoma/secuencia que usas en TBtools
nombre_chr = "MST_PLTD"

# Ejecutamos la función
convertir_trf_a_tbtools(archivo_trf, archivo_tbtools, nombre_cromosoma=nombre_chr, valor="orange")
