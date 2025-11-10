#!/usr/bin/env python3
import sys
import re

if len(sys.argv) != 3:
    print("Usage: python aro_lookup.py <fasta_file> <ARO number>")
    sys.exit(1)

fasta = sys.argv[1]
aro_query = sys.argv[2]

# Regex tuned for your FASTA headers
pattern = re.compile(
    r"^>gb\|([^|]+)\|.*?ARO:(\d+)\|([^\[]+)\[([^\]]+)\]",
    re.IGNORECASE
)

with open(fasta) as f:
    for line in f:
        if not line.startswith(">"):
            continue
        
        m = pattern.search(line)
        if m:
            accession, aro, gene, organism = m.groups()

            if aro == aro_query:
                print(f"gb|{accession}|+{gene.strip()} [{organism.strip()}]")
                sys.exit(0)

print("Not found.")
