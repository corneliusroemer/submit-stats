set -x
set -v
scp -C worker01.scicore.unibas.ch:~/ncov-simple/archive/pre-processed/metadata.tsv .
conda activate nextstrain
tsv-filter -H --str-eq country:Switzerland metadata.tsv | tsv-select -H -f strain,date,date_submitted,submitting_lab > meta_switzerland.tsv
python3 analysis.py
tsv-filter -H --regex '2:2021-(39|4)' days_diff_by_submitting_lab_and_week.tsv >days_diff_most_recent_weeks.tsv
