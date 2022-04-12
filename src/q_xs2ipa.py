import csv
import sys
import glob
import os
import pandas as pd


# convert formant or TextGrid phones from XSAMPA to IPA
# ex:
# python src/q_xs2ipa.py data/wild/formant_raw data/wild/formant_ipa formant_csv
# python src/q_xs2ipa.py /Users/eahn/work/typ/data/voxclamantis/tg/{lang} data/wild/tg_ipa/{lang}/ tg

table_csv = '/Users/eahn/work/tools/epitran-master/epitran/data/ipa-xsampa.csv'
in_folder = sys.argv[1]  # no final /
out_folder = sys.argv[2]  # no final /
file_type = sys.argv[3]  # 'tg' or 'formant_csv'

xs_ipa_dict = {}
with open(table_csv, 'r') as f:
	# reader = csv.reader(f, encoding='utf-8')
	reader = csv.reader(f)
	next(reader)
	for ipa, xs, _ in reader:
		# xs_ipa_dict[xs.encode('utf-8')] = ipa
		xs_ipa_dict[xs] = ipa


def get_longest_prefix(in_str):
	if len(in_str) < 2:
		return in_str, None

	for i in range(1, len(in_str)):
		longest_prefix = in_str[:-i]
		remainder = in_str[-i:]
		if longest_prefix in xs_ipa_dict:
			return longest_prefix, remainder

	return in_str, None


if file_type == 'tg':
	for in_file in glob.glob(f'{in_folder}/*.TextGrid'):
		out_file = f'{out_folder}/{os.path.basename(in_file)}'
		with open(in_file, 'r') as r:
			with open(out_file, 'w') as w:
				for line in r.readlines():
					if 'text = ' in line:
						if 'SIL' in line:
							w.write(line)
							continue

						xsampa = line.split('text = ')[1]
						xsampa = xsampa.strip()
						xsampa = xsampa[1:-1]  # remove outside quotes only

						if xsampa in xs_ipa_dict:
							line = line.replace(xsampa, xs_ipa_dict[xsampa])

						else:
							# multiple symbols in xsampa (e.g. contains diacritics)
							leftover = xsampa
							while leftover:
								longest_prefix, remainder = get_longest_prefix(leftover)
								if remainder is None:
									break
								line = line.replace(longest_prefix, xs_ipa_dict[longest_prefix])
								if remainder in xs_ipa_dict:
									line = line.replace(remainder, xs_ipa_dict[remainder])
									leftover = ''  # all done!
								else:
									leftover = remainder

					w.write(line)

elif file_type == 'formant_csv':
	for in_file in glob.glob(f'{in_folder}/*.csv'):
		out_file = f'{out_folder}/{os.path.basename(in_file)}'
		data = pd.read_csv(in_file)
		print(in_file)
		phones = set(data['vowel'])
		print('vowels', phones)
		# phones.discard('4')
		# phones.discard('5')
		phones = phones.union(set(data['prec']))
		phones = phones.union(set(data['foll']))
		print(in_file, phones)
		# import pdb; pdb.set_trace()

		xs_ipa_csv_dict = {}
		for phone in phones:
			if type(phone) is not str:
				continue

			elif phone == 'SIL':
				continue

			elif phone in xs_ipa_dict:
				xs_ipa_csv_dict[phone] = xs_ipa_dict[phone]

			else:
				# multiple symbols in phone (e.g. contains diacritics)
				ipa = ''
				leftover = phone
				# import pdb; pdb.set_trace()
				while leftover:
					longest_prefix, remainder = get_longest_prefix(leftover)
					# import pdb; pdb.set_trace()
					if remainder is None:
						break
					ipa += xs_ipa_dict[longest_prefix]
					if remainder in xs_ipa_dict:
						ipa += xs_ipa_dict[remainder]
						leftover = ''  # all done!
					else:
						leftover = remainder

				xs_ipa_csv_dict[phone] = ipa

		# remove extraneous '4'/'5' from vowel set
		df_filtered = data[data['vowel'] != '4']
		df_filtered = df_filtered[df_filtered['vowel'] != '5']

		# replace xsampa with ipa
		for xsampa, full_ipa in xs_ipa_csv_dict.items():

			df_filtered['vowel']= df_filtered['vowel'].replace(xsampa, full_ipa)
			df_filtered['prec']= df_filtered['prec'].replace(xsampa, full_ipa)
			df_filtered['foll']= df_filtered['foll'].replace(xsampa, full_ipa)

		df_filtered.to_csv(out_file)



