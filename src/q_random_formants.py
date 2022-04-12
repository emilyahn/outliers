import sys
import pandas as pd


# take full formant file (with column marked with Mahalanobis distance 'MD')
# take errors greater than OUTLIER_THRESH(old) and take random NUM_SAMPLES (e.g. 100) subset
# write to CSV
# ex.
# python src/q_random_formants.py data/wild/mahal/KAZKAZ_vowels_all.csv data/wild/annotate/KAZKAZ_errors_100.csv

full_csv = sys.argv[1]
out_csv = sys.argv[2]
OUTLIER_THRESH = 13.82
NUM_SAMPLES = 100


df = pd.read_csv(full_csv)
df_errors = df[df['MD'] > OUTLIER_THRESH]
errors_subset = df_errors.sample(n=NUM_SAMPLES)

print('TOTAL ERRORS')
print(df_errors['vowel'].value_counts())

print('SUBSET ERRORS')
print(errors_subset['vowel'].value_counts())

# sort
sorted100 = errors_subset.sort_values(by=['file'])
sorted100.to_csv(out_csv, index=False)
