
from pymatgen.analysis.diffraction.xrd import XRDCalculator
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.ext.matproj import MPRester
import pandas as pd

with MPRester(api_key='xxxxxxxxxxx') as mpr:  ##### put your own API key
    # first retrieve the relevant structure
    structure = mpr.get_structure_by_material_id('mp-xxxxx')  #### number of mp structure

# important to use the conventional structure to ensure
# that peaks are labelled with the conventional Miller indices
sga = SpacegroupAnalyzer(structure)
conventional_structure = sga.get_conventional_standard_structure()

# this example shows how to obtain an XRD diffraction pattern
# these patterns are calculated on-the-fly from the structure
calculator = XRDCalculator(wavelength='CuKa')
pattern = calculator.get_pattern(conventional_structure)

print(pattern)

x, y = pattern.x, pattern.y

df = pd.DataFrame({"2theta": x, "I": y})

#### arredondar casas decimais
df['2theta'] = df['2theta'].round(1)
df['I'] = df['I'].round(1)


# criando um índice completo de 10 a 80, com intervalo de 0,1
indice_completo = pd.Series(range(100, 801)).div(10)

# definindo o índice do dataframe como os valores completos de 10 a 80
df = df.set_index('2theta').reindex(indice_completo).reset_index()

# renomeando a coluna de índice de volta para 'x'
df = df.rename(columns={'index': '2theta'})

pd.set_option('display.max_rows', None)


# preenchendo valores ausentes na coluna 'y' com 0
df.loc[df['I'].isna(), 'I'] = 0

# imprimindo o dataframe resultante
print(df)

df.to_excel("pattern.xlsx", index=False)
