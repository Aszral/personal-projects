def dna_to_rna(dna):
    rna = ""
    for letter in dna.upper():
        if letter == "G":
            rna += "C"
        elif letter == "C":
            rna += "G"
        elif letter == "T":
            rna += "A"
        elif letter == "A":
            rna += "U"
        elif letter == "U":
            rna += "A"

    return rna
