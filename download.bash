set -x
set -v
scp worker01.scicore.unibas.ch:~/ncov-simple/archive/pre-processed/metadata.tsv .
tsv-filter -H --str-eq country:Switzerland metadata.tsv | tsv-select -H -f strain,date,date_submitted,submitting_lab > meta_switzerland.tsv
