def procesar_misa_a_tbtools(archivo_entrada, archivo_salida, nombre_cromosoma):
    print(f"Procesando {archivo_entrada}...")

    with open(archivo_entrada, 'r') as f_in, open(archivo_salida, 'w') as f_out:
        lineas = f_in.readlines()
        contador = 0

        for i, linea in enumerate(lineas):
            if i == 0 and "ID" in linea and "start" in linea:
                continue

            columnas = linea.strip().split()

            if not columnas:
                continue

            try:
                start = columnas[-2]
                end = columnas[-1]

                int(start)
                int(end)

                f_out.write(f"{nombre_cromosoma}\t{start}\t{end}\t1\n")
                contador += 1

            except ValueError:
                print(f"⚠️ Aviso: Se saltó la línea {i+1} por formato inválido: {linea.strip()}")

    print(f"¡Listo! Se han guardado {contador} SSRs en '{archivo_salida}'.")

# ==========================================
# AQUÍ ES DONDE VAN TUS DATOS REALES
# ==========================================
archivo_misa = "MST_PLTD_SSR_REAL.txt"
archivo_final = "MST_PLTD_Misa_REAL_Tbtooler.txt"
nombre_en_circos = "MST_PLTD"

procesar_misa_a_tbtools(archivo_misa, archivo_final, nombre_en_circos)
