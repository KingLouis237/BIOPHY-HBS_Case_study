# BLAST Workflow

~~~
blastp -query data/processed/blast/secret_beta_query.fasta -db swissprot -taxids 9606 -outfmt 5 -max_target_seqs 5 -evalue 1e-20 -out data/processed/blast/secret_beta_blast.xml
~~~

- Requires NCBI BLAST+ to be installed locally or available in the PATH.
- Restricts the search to Homo sapiens (taxid 9606).
- Expect top hits corresponding to hemoglobin beta variants (e.g., Hb Monza, HbS).
- Copy the resulting XML/Tabular output into data/processed/blast/ for version control.
