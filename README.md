# Outliers
An Outlier Analysis of Vowel Formants from a Corpus Phonetics Pipeline

Emily P. Ahn (University of Washington)

## Tools/Versions
* Python 3.9.0
* Montreal Forced Aligner 2.0.0 (via conda)
* R 4.2.2

## Notes for this Repository
* Disclaimer: scripts that are 'quick-and-dirty' start with `q_` and are not meant to reflect high quality code

## Preprocessing Data
### CommonVoice v8
* download data, follow `data/cv8/{lang}/processCommonVoice_{lang}_v8.txt` steps
	* (includes using praat scripts, Epitran for G2P, MFA for forced alignment)
* extract formants with `src/getFormantsCommonVoice_highlow.praat` (under high and low settings)
* assign each speaker to either high or low formant setting (will use only low for analysis) with `python src/assign_formant_range.py > data/cv8/formants/settings_highlow.tsv`
	* filter this file to just get low setting speakers: `head -1 data/cv8/formants/settings_highlow.tsv > data/cv8/formants/settings_low.tsv; cat data/cv8/formants/settings_highlow.tsv | awk '$3 == "low" {print}' >> data/cv8/formants/settings_low.tsv`
* quick script to just get formant data of F1/F2 midpoints and low setting speakers only: `src/q_simplify_cv_formants.py`
* additional script to get AVG F1/F2 per vowel per speaker: `src/get_avg_form_cvlow.py`

### Wilderness
* download formants from VoxClamantis (now stored in `data/wild/formant_raw/`); F1/F2 midpoints only
* download TextGrids from VoxClamantis
* convert formant phones from XSAMPA to IPA with `python src/q_xs2ipa.py data/wild/formant_raw data/wild/formant_ipa formant_csv`
* convert TextGrid phones from XSAMPA to IPA with `python src/q_xs2ipa.py /Users/eahn/work/typ/data/voxclamantis/tg/{lang} data/wild/tg_ipa/{lang}/ tg`


## Discovering Errors
* From formant files, create distributions per vowel with `src/mahal_{wild,cv}.py`
	* uses SciKit Learn package [MinCovDet](https://scikit-learn.org/stable/modules/generated/sklearn.covariance.MinCovDet.html)
	* output to another csv file with column 'MD' (Mahalanobis distance)
	* `src/mahal_cv.py` can take a subset argument to only get n utterances (used in this case for Common Voice Swedish)
* To get outliers at 0.1% edge of distribution, use mahal_thresh = 13.82  (alpha = 0.001, 2 degrees of freedom)
* Subset errors (thresh = 13.82, num_samples = 100) with `python src/q_random_errors.py data/wild/mahal/{lang}_vowels_all.csv data/wild/annotate/{lang}_vowels_100.csv`
	* Subset at other points along the MD distribution (e.g. 'near-perfect' samples of Mahal dist < 1.0)
	`python src/q_random_good.py data/cv8/mahal/kazakh_vowels_all.csv data/cv8/annotate/kazakh_good_40.csv 1 40`
* Move only num_samples audio and textgrids into folders for annotation:
```sh
# wild errors
lang="SWESFV"; for utt_id in `cat data/wild/annotate/${lang}_errors_100.csv | tail -n +2 | cut -d"," -f1 | sort -u`; do source_file="/Users/eahn/work/typ/data/audio/wav_seg/${lang}/${utt_id}.wav"; cp $source_file data/wild/audio/${lang}_errors_100; done
lang="SWESFV"; for utt_id in `cat data/wild/annotate/${lang}_errors_100.csv | tail -n +2 | cut -d"," -f1 | sort -u`; do source_file="data/wild/tg_ipa/${lang}/${utt_id}.TextGrid"; cp $source_file data/wild/annotate/tg/${lang}_errors_100; done
# wild good
lang="SWESFV"; wav_dir="data/wild/audio/${lang}_good_40_wav"; mkdir $wav_dir; for utt_id in `cat data/wild/annotate/${lang}_good_40.csv | tail -n +2 | cut -d"," -f1 | sort -u`; do source_file="/Users/eahn/work/typ/data/audio/wav_seg/${lang}/${utt_id}.wav";  cp $source_file $wav_dir; done
lang="SWESFV"; tg_dir="data/wild/annotate/tg/${lang}_good_40_tg"; mkdir $tg_dir; for utt_id in `cat data/wild/annotate/${lang}_good_40.csv | tail -n +2 | cut -d"," -f1 | sort -u`; do source_file="data/wild/tg_ipa/${lang}/${utt_id}.TextGrid";  cp $source_file $tg_dir; done
# cv errors
lang="kazakh"; wav_dir="data/cv8/annotate/${lang}_errors_100_wav"; mkdir $wav_dir;for utt_id in `cat data/cv8/annotate/${lang}_errors_100.csv | tail -n +2 | cut -d"," -f1 | sort -u`; do source_file="data/cv8/${lang}/prep_validated/${utt_id}.wav";  cp $source_file $wav_dir; done
lang="hausa"; tg_dir="data/cv8/annotate/${lang}_errors_100_tg"; mkdir $tg_dir;for utt_id in `cat data/cv8/annotate/${lang}_errors_100.csv | tail -n +2 | cut -d"," -f1 | sort -u`; do source_file="data/cv8/${lang}/aligned_validated/${utt_id}.TextGrid";  cp $source_file $tg_dir; done
# cv good files
lang="kazakh"; wav_dir="data/cv8/annotate/${lang}_good_40_wav"; mkdir $wav_dir;for utt_id in `cat data/cv8/annotate/${lang}_good_40.csv | tail -n +2 | cut -d"," -f1 | sort -u`; do source_file="data/cv8/${lang}/prep_validated/${utt_id}.wav";  cp $source_file $wav_dir; done
lang="hausa"; tg_dir="data/cv8/annotate/${lang}_good_40_tg"; mkdir $tg_dir;for utt_id in `cat data/cv8/annotate/${lang}_good_40.csv | tail -n +2 | cut -d"," -f1 | sort -u`; do source_file="data/cv8/${lang}/aligned_validated/${utt_id}.TextGrid";  cp $source_file $tg_dir; done
```

## Annotations
* Guidelines: `PDF FILE`
* Master spreadsheet including re-annotations with new Formant category: `data/master_reannot_221114.csv`

