 CSV file to Database

## Gene family (Populate manually)
* family_id --> gene_family.csv (family_id)
* name --> gene_family.csv (name)
* description --> gene_family.csv (description)

## Resistance genes
* gene_id --> aro.tsv (Assession)
* name --> aro.tsv (ARO Name)
* family_id --> added column to aro.tsv
* description --> aro.tsv (description)
* mechanism_id --> 
* sequence_accession --> aro.tsv (Assession)
* notes --> 

## Resistance mechanism
mechanism_id --> aro_categories.tsv (ARO Accession where ARO Category == Resistance Mechanism)
name --> aro_categories_index.tsv (Resistance Mechanism text)
description --> aro_categories_index.tsv (Description)

## Resistancee profiles
* profile_id --> resistance_profiles.tsv (#BioSample)
* organism_id --> connect to Organism.id (Match Scientific name to Organisms.name)
* antibiotic_id --> connect to Antibiotic.id (Match Antibiotic from resistance_profiles.tsv to Antibiotic.name and get Antibiotic.antibiotic_id)
* gene_id --> connect to Resistance_gene.id??? how?
* mechanism_id --> connect to Resistance_mechanism.id
* mic_value --> resistance_profiles.tsv (MIC (mg/L))
* mic_unit --> set it to mg/L
* resistance_level --> resistance profile (Resistance phenotype)
* source_id --> connect to DataSources.id
* year --> resistance_profiles.tsv (First 4 digits of create date)
* region --> resistance_profiles.tsv (location)