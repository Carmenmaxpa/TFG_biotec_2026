import re
from openpyxl import Workbook

# =========================
# CONFIGURACIÓN
# =========================

gff_file = "archivo.gff3"      # <-- Cambia por tu archivo
output_file = "genes_output.xls"

# Lista de genes (se eliminan duplicados automáticamente)
gene_list_raw = """
ycf2
TrnM-CAU
rpl23
rpl2
rps19
trnH-GUG
petG
trnW-CCA
trnP-UGG
rrn16S
psbC
trnS-GGA
rpoB
trnD-GUC
trnN-GUU
ndhC
TrnS-GCU
rrn23S
trnA-UGC
TrnE-UUC
"""

# Normalizar lista (eliminar duplicados y espacios)
gene_set = set(g.strip().replace(",", "") for g in gene_list_raw.splitlines() if g.strip())

# =========================
# PROCESAMIENTO GFF
# =========================

results = []

with open(gff_file, "r") as f:
    for line in f:
        if line.startswith("#"):
            continue

        cols = line.strip().split("\t")
        if len(cols) < 9:
            continue

        feature_type = cols[2]

        # Solo mirar mRNA (ahí está el Name real del gen)
        if feature_type == "mRNA":
            attributes = cols[8]

            match = re.search(r"Name=([^;]+)", attributes)
            if match:
                gene_name = match.group(1)

                if gene_name in gene_set:
                    results.append([
                        gene_name,
                        cols[0],   # Contig
                        cols[3],   # Start
                        cols[4],   # End
                        cols[6]    # Strand
                    ])

# =========================
# EXPORTAR A XLS
# =========================

wb = Workbook()
ws = wb.active
ws.title = "Gene Coordinates"

# Cabecera
ws.append(["Gene", "Contig", "Start", "End", "Strand"])

# Datos
for row in results:
    ws.append(row)

wb.save(output_file)

print(f"Archivo generado correctamente: {output_file}")

