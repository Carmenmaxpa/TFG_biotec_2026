import re
from openpyxl import Workbook

gff_file = "archivo.gff3"      
output_file = "genes_output.xls"

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

gene_set = set(g.strip().replace(",", "") for g in gene_list_raw.splitlines() if g.strip())

results = []

with open(gff_file, "r") as f:
    for line in f:
        if line.startswith("#"):
            continue

        cols = line.strip().split("\t")
        if len(cols) < 9:
            continue

        feature_type = cols[2]

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


wb = Workbook()
ws = wb.active
ws.title = "Gene Coordinates"


ws.append(["Gene", "Contig", "Start", "End", "Strand"])


for row in results:
    ws.append(row)

wb.save(output_file)

print(f"Archivo generado correctamente: {output_file}")

