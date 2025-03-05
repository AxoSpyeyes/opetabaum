def format_fras(ttb):
    fras = ttb["fras"]
    ko = [konen["ko"] for konen in ttb["zunaga"]]
    svar = fras.format(*ko)
    return svar
