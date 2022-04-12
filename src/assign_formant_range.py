import sys
import csv
import glob
import os
import numpy as np
from collections import defaultdict
from statistics import mean
from sklearn.covariance import MinCovDet


# assign Common Voice speakers to high or low formant range
# to run:
# python assign_formant_range.py
# ex:
# python src/assign_formant_range.py > data/cv8/formants/settings_highlow.tsv

# TRAIN: load 1202 data points across 11 langs (uzbek -> dutch)
def process_gender_tsv(tsv_file):
	# langs = []
	genders = []
	f1 = []
	f2 = []

	with open(tsv_file, newline='') as tsvfile:
		reader = csv.DictReader(tsvfile, delimiter='\t')
		for row in reader:
			# langs.append(row['lang'])
			genders.append(row['gender'])
			f1.append(float(row['F1 avg']))
			f2.append(float(row['F2 avg']))

	m_f1 = []
	m_f2 = []
	f_f1 = []
	f_f2 = []
	for i, val in enumerate(f1):
		if genders[i] == 'male':
			m_f1.append(val)
			m_f2.append(f2[i])
		elif genders[i] == 'female':
			f_f1.append(val)
			f_f2.append(f2[i])
	return m_f1, m_f2, f_f1, f_f2

low_m_f1, low_m_f2, low_f_f1, low_f_f2 = process_gender_tsv('data/old_cv7/train_cv7_gender_low_mp.tsv')
high_m_f1, high_m_f2, high_f_f1, high_f_f2 = process_gender_tsv('data/old_cv7/train_cv7_gender_high_mp.tsv')

# fit male speakers to LOW setting
male_f12 = np.stack((np.array(low_m_f1), np.array(low_m_f2)), axis=1)
low_cov = MinCovDet(random_state=0).fit(male_f12)
# fit female speakers to HIGH setting
female_f12 = np.stack((np.array(high_f_f1), np.array(high_f_f2)), axis=1)
high_cov = MinCovDet(random_state=0).fit(female_f12)

# TEST: iterate across langs
print('lang\tspkr\tsetting\tF1 avg\tF2 avg')
for low_formant_infile in glob.glob('data/cv8/*/*_formants_low2.*'):
# do 1 lang at a time version:
# for low_formant_infile in glob.glob('data/comvoi/formants/full/hungarian_formants_low4.csv'):
	high_formant_infile = low_formant_infile.replace('low2', 'high2')
	lang = os.path.basename(low_formant_infile).split('_')[0]  # makes "sorbian_upper" into "sorbian"

	# collect f1_mid and f2_mid values into dictionaries per speaker
	def get_spkr_formants(formant_infile):
		print(formant_infile, file=sys.stderr)
		spkr_formants = {}
		try:
			with open(formant_infile, encoding='utf-16') as csvfile:
				reader = csv.DictReader(csvfile, delimiter=',')

				for row in reader:

					fileid = row['file']
					spkr_id = fileid.split('_')[0]  # ex. 00004

					# average formant midpoint with its nearest +/- 10ms around the midpoint
					f1 = mean([float(row['f1_mid']), float(row['f1_mp1']), float(row['f1_mp2'])])
					f2 = mean([float(row['f2_mid']), float(row['f2_mp1']), float(row['f2_mp2'])])

					if spkr_id not in spkr_formants:
						spkr_formants[spkr_id] = defaultdict(list)

					spkr_formants[spkr_id]['f1'].append(f1)
					spkr_formants[spkr_id]['f2'].append(f2)

		except:
			# remove encoding
			with open(formant_infile) as csvfile:
				reader = csv.DictReader(csvfile, delimiter=',')

				for row in reader:
					fileid = row['file']
					spkr_id = fileid.split('_')[0]  # ex. 00004

					# average formant midpoint with its nearest +/- 10ms around the midpoint
					f1 = mean([float(row['f1_mid']), float(row['f1_mp1']), float(row['f1_mp2'])])
					f2 = mean([float(row['f2_mid']), float(row['f2_mp1']), float(row['f2_mp2'])])

					if spkr_id not in spkr_formants:
						spkr_formants[spkr_id] = defaultdict(list)

					spkr_formants[spkr_id]['f1'].append(f1)
					spkr_formants[spkr_id]['f2'].append(f2)

		return spkr_formants

	low_spkr_formants = get_spkr_formants(low_formant_infile)
	high_spkr_formants = get_spkr_formants(high_formant_infile)

	for spkr in low_spkr_formants:

		low_test_point = [[mean(low_spkr_formants[spkr]['f1']), mean(low_spkr_formants[spkr]['f2'])]]
		high_test_point = [[mean(high_spkr_formants[spkr]['f1']), mean(high_spkr_formants[spkr]['f2'])]]

		# get distance for low point at low setting and high point at high setting
		test_low_low_dist = low_cov.mahalanobis(low_test_point)
		test_high_high_dist = high_cov.mahalanobis(high_test_point)

		if test_low_low_dist < test_high_high_dist:
			label = 'low'
			print_f1 = mean(low_spkr_formants[spkr]['f1'])
			print_f2 = mean(low_spkr_formants[spkr]['f2'])
		else:
			label = 'high'
			print_f1 = mean(high_spkr_formants[spkr]['f1'])
			print_f2 = mean(high_spkr_formants[spkr]['f2'])

		out_str = f"{lang}\t{spkr}\t{label}\t{print_f1:.2f}\t{print_f2:.2f}"
		print(out_str)
