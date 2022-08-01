import ehtim as eh


files = [
            'avery_m87_1_eofn',
            'avery_sgra_eofn',
            'jason_mad_eofn',
            'roman_eofn',
            'avery_m87_2_eofn',
            'howes_m87',
            'jason_mri_eofn',
            'rowan_m87'
            ]

for f in files:
    im = eh.image.load_txt(f'models/{f}.txt')
    im.display(show=False, export_pdf=f"models/{f}.pdf")
