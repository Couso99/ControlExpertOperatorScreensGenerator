
filter = "TP06"
fname = "EXPORT_TP06.txt"

outfname = f"FILTERED_TAGS/{filter}_{fname}"

with open(fname, 'r') as f:
    rows = f.readlines()

new_rows = []
for row in rows:
    if filter in row:
        new_rows.append(row)

with open(outfname, 'w+') as f:
    [f.write(row) for row in new_rows]
