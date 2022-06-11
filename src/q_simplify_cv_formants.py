import sys
import pandas as pd


# Simplify raw Common Voice formant files
# output: only f1_mid, f2_mid (no quartiles, near-midpoints)
#			only for low-formant setting speakers


lang_name = sys.argv[1]
out_file = sys.argv[2]


# load low_spkr IDs
low_spkr_file = f'data/cv8/{lang_name}/{lang_name}_low_spkrs.txt'
with open(low_spkr_file, 'r') as f:
	low_spkr_list = [line.strip() for line in f.readlines()]

# load formant file
formant_file = f'data/cv8/{lang_name}/{lang_name}_formants_low2.csv'
fields = ['file', 'vowel', 'prec', 'foll', 'start', 'end', 'f1_mid', 'f2_mid']
df = pd.read_csv(formant_file, usecols=fields, encoding='utf16')

# remove nan's
df = df[(pd.isna(df['f1_mid']) == False)]
df = df[(pd.isna(df['f2_mid']) == False)]

# filter to keep only speakers from low_spkr_list
df = df[df['file'].str.startswith(tuple(low_spkr_list))]

# sort and export
sorted_n = df.sort_values(by=['file'])
sorted_n.to_csv(out_file, index=False)
