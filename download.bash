set -x
set -v
scp worker01.scicore.unibas.ch:~/ncov-simple/archive/pre-processed/metadata.tsv.zst .
zstd -d metadata.tsv.zst >metadata.tsv
tsv-filter -H --str-eq country:Switzerland metadata.tsv | tsv-select -H -f strain,date,date_submitted,submitting_lab > meta_switzerland.tsv
