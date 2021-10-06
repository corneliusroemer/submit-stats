set -x
set -v
scp -C worker01.scicore.unibas.ch:~/ncov-simple/archive/pre-processed/metadata.tsv .
conda activate nextstrain
tsv-filter -H --str-eq country:Switzerland metadata.tsv | tsv-select -H -f strain,date,date_submitted,submitting_lab > meta_switzerland.tsv
python3 analysis.py
