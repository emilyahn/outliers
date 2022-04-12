import sys
import csv
import pandas as pd
import numpy as np
from sklearn.covariance import MinCovDet


# Get distribution and outliers via Mahalanobis distance for vowels F1 + F2
# for Wilderness data (from formant csv files)
# don't need to filter to keep only speakers from low_spkr_list

# to run:
# python mahal_wild.py {formant_file} {out_csv}
# ex:
# python src/mahal_wild.py data/wild/formant_ipa/KAZKAZ_formants_mid.csv data/wild/mahal/KAZKAZ_vowels_all.csv


def main():
	formant_file = sys.argv[1]
	out_csv = sys.argv[2]

	fields = ['file', 'vowel', 'prec', 'foll', 'start', 'end', 'f1_mid', 'f2_mid']
	df = pd.read_csv(formant_file, usecols=fields)
	df = df[(pd.isna(df['f1_mid']) == False)]

	vowel_set = set(df['vowel'])

	# set up out_file (csv) to write
	with open(out_csv, 'w', newline='') as csv_writer:
		fieldnames = ['file', 'vowel', 'prec', 'foll', 'start', 'end', 'F1', 'F2', 'MD']
		writer = csv.DictWriter(csv_writer, fieldnames=fieldnames)

		writer.writeheader()

		for vowel in vowel_set:
			vowel_df = df[df['vowel'] == vowel]

			# only take vowels that occur >= 100 times
			if len(vowel_df) < 100:
				continue

			f12 = np.stack((vowel_df['f1_mid'], vowel_df['f2_mid']), axis=1)
			print(vowel, len(f12))
			f12_cov = MinCovDet(random_state=0).fit(f12)

			for index in vowel_df.index:
				f1 = vowel_df['f1_mid'][index]
				f2 = vowel_df['f2_mid'][index]
				mahal_dist = f12_cov.mahalanobis([[f1, f2]])
				# import pdb; pdb.set_trace()

				writer.writerow({'file': vowel_df['file'][index], 'vowel': vowel_df['vowel'][index], 'prec': vowel_df['prec'][index], 'foll': vowel_df['foll'][index], 'start': f'{vowel_df["start"][index]:.2f}', 'end': f'{vowel_df["end"][index]:.2f}', 'F1': f'{f1:.2f}', 'F2': f'{f2:.2f}','MD': f'{mahal_dist[0]:.3f}'})  # only 2 or 3 digits


if __name__ == '__main__':
	main()
