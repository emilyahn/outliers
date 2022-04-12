# outliers
Outlier Analysis of Phone-aligned Audio

## Preprocessing Data
### CommonVoice v8
* download data, follow `data/cv8/{lang}/processCommonVoice_{lang}_v8.txt` steps
	* (includes using praat scripts, Epitran for G2P, MFA for forced alignment)
* extract formants with `src/getFormantsCommonVoice_highlow.praat` (under high and low settings)
* assign each speaker to either high or low formant setting (will use only low for analysis) with `python src/assign_formant_range.py > data/cv8/formants/settings_highlow.tsv`
	* filter this file to just get low setting speakers: `head -1 data/cv8/formants/settings_highlow.tsv > data/cv8/formants/settings_low.tsv; cat data/cv8/formants/settings_highlow.tsv | awk '$3 == "low" {print}' >> data/cv8/formants/settings_low.tsv`

### Wilderness
* download formants from VoxClamantis (now stored in `data/wild/formant_raw/`); F1/F2 midpoints only
* download TextGrids from VoxClamantis
* convert formant phones from XSAMPA to IPA with `python src/q_xs2ipa.py data/wild/formant_raw data/wild/formant_ipa formant_csv`
* convert TextGrid phones from XSAMPA to IPA with `python src/q_xs2ipa.py /Users/eahn/work/typ/data/voxclamantis/tg/{lang} data/wild/tg_ipa/{lang}/ tg`


## Discovering Errors
* From formant files, create distributions per vowel with `src/mahal_{wild,cv}.py`
	* uses SciKit Learn package [MinCovDet](https://scikit-learn.org/stable/modules/generated/sklearn.covariance.MinCovDet.html)
	* output to another csv file with column 'MD' (Mahalanobis distance)
* To get outliers at 0.1% edge of distribution, use mahal_thresh = 13.82  (alpha = 0.001, 2 degrees of freedom)
* Subset errors (thresh = 13.82, num_samples = 100) with `python src/q_random_formants.py data/wild/mahal/{lang}_vowels_all.csv data/wild/annotate/{lang}_vowels_100.csv`
* Move only num_samples audio and textgrids into folders for annotation:
```sh
lang="SWESFV"; for utt_id in `cat data/wild/annotate/${lang}_errors_100.csv | tail -n +2 | cut -d"," -f1 | sort -u`; do source_file="/Users/eahn/work/typ/data/audio/wav_seg/${lang}/${utt_id}.wav"; cp $source_file data/wild/audio/${lang}_errors_100; done
lang="SWESFV"; for utt_id in `cat data/wild/annotate/${lang}_errors_100.csv | tail -n +2 | cut -d"," -f1 | sort -u`; do source_file="data/wild/tg_ipa/${lang}/${utt_id}.TextGrid"; cp $source_file data/wild/annotate/tg/${lang}_errors_100; done
```
