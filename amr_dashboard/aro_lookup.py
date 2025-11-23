import sys
import re

def clean_header(header: str,index):
    """
    Clean both DNA and protein FASTA headers.
    """

    # 2 patterns: DNA-style and protein-style
    fields = header[1:].split('|')
    
    if index < 0:
        return header

    # Check if we have enough fields (5 delimiters means 6 fields)
    if len(fields) < index+1:
        return f"Error: {header}"
    fields_to_keep = fields[:index] + fields[index+1:]
    
    # 3. Join the selected fields back together with the '|' delimiter.
    result_string = '|'.join(fields_to_keep)
    
    return result_string

def load_fasta_lookup(filename, queries, index):
    results = {}
    with open(filename) as fh:
        for line in fh:
            if line.startswith(">"):
                header = line.strip()
                aro_match = re.search(r"ARO:(\d+)", header)
                if aro_match:
                    aro = aro_match.group(1)
                    if aro in queries:
                        results[aro] = clean_header(header,index) or f"UNPARSED: {header}"
    return results

def add_one(s):
    parts = s.split("|")
    # parts[3] is "0-723"
    if len(parts) > 2:
        start, end = parts[3].split("-")
        start = str(int(start) + 1)
        parts[3] = f"{start}-{end}"

    out = "|".join(parts)
    return out

def main():
    if len(sys.argv) != 4:
        print("Usage: python aro_lookup_bulk.py <dna_fasta> <protein_fasta> <aro_list>")
        sys.exit(1)

    dna_fasta = sys.argv[1]
    protein_fasta = sys.argv[2]
    aro_file = sys.argv[3]

    aro_list = [line.strip() for line in open(aro_file) if line.strip()]
    queries = set(aro_list)

    dna_results = load_fasta_lookup(dna_fasta, queries,4)
    prot_results = load_fasta_lookup(protein_fasta, queries,2)

    for aro in aro_list:
        dna_val = add_one(dna_results.get(aro, "N/A"))
        prot_val = re.sub(r'^((?:[^|]*\|){2})', r'\1+|', prot_results.get(aro, "N/A"))
        print(f"{dna_val}\t{prot_val}")

if __name__ == "__main__":
    main()
