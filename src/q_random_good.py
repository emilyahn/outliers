import sys
import pandas as pd


# take full formant file (with column marked with Mahalanobis distance 'MD')
# take 'good' vowels whose MD for F1/F2 is LESS than THRESH and take random NUM_SAMPLES (e.g. 25) subset
# write to CSV
# ex.
# python src/q_random_good.py data/wild/mahal/KAZKAZ_vowels_all.csv data/wild/annotate/KAZKAZ_good_25.csv 2 25

full_csv = sys.argv[1]
out_csv = sys.argv[2]
OUTLIER_THRESH = float(sys.argv[3])  # 2.0
NUM_SAMPLES = int(sys.argv[4])  # 25


df = pd.read_csv(full_csv)
df_good = df[df['MD'] < OUTLIER_THRESH]
errors_subset = df_good.sample(n=NUM_SAMPLES)

print('TOTAL GOOD')
print(df_good['vowel'].value_counts())

print('SUBSET GOOD')
print(errors_subset['vowel'].value_counts())

# sort
sorted_n = errors_subset.sort_values(by=['file'])
sorted_n.to_csv(out_csv, index=False)
