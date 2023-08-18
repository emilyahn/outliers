import pandas as pd


# prep data for logistic regression analysis in R
# includes following categories: vowel height, sibilant environment
# output variable: Deletion (binary)
# output file: CSV w/ headings: Dataset, Type, Lang, File, Start, vowel, v_high, sib_env, deleted
# to run:
#	python src/prep_logregsib_data.py

master_spreadsheet = "data/master_reannot_221114.csv"

# INCLUDE_NEARMEANS = False  # if false, don't process near-mean vowels
# out_file = "data/analysis/logreg_sibilants_outliers.csv"

INCLUDE_NEARMEANS = True  # if false, don't process near-mean vowels
out_file = "data/analysis/logreg_sibilants_all.csv"

sibilants = ["s", "z", "ʃ", "ʒ", "ʂ", "ʐ", "ɕ", "ʑ", "ɕː"]
high_vowels = ["ɪ", "i", "ʏ", "ʊ", "u", "iː", "ʉ", "uː", "ʉː", "yː"]

gold_data = pd.read_csv(master_spreadsheet)

if not INCLUDE_NEARMEANS:
	gold_data = gold_data[gold_data['Type'] == 'outlier']

out_df = gold_data[['Dataset', 'Type', 'Lang', 'file', 'start', 'vowel']].copy()
out_df['v_high'] = pd.Series([], dtype=object)
out_df['sib_env'] = pd.Series([], dtype=object)
out_df['deleted'] = pd.Series([], dtype=object)

for index, row in gold_data.iterrows():
	out_df.loc[index, 'sib_env'] = 1 if row['prec'] in sibilants or row['foll'] in sibilants else -1
	out_df.loc[index, 'v_high'] = 1 if row['vowel'] in high_vowels else -1
	out_df.loc[index, 'deleted'] = 1 if row['Linguistic'] == 'Deletion' else 0

out_df.to_csv(out_file, index=False)