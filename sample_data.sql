-- Generated from ChatGPT

-- Drug Classes
INSERT INTO drug_classes (name, description)
VALUES 
('Beta-lactams', 'Penicillins, Cephalosporins, etc.'),
('Aminoglycosides', 'Gentamicin, Tobramycin, etc.');

-- Antibiotics
INSERT INTO antibiotics (name, drug_class_id, atc_code, notes)
VALUES
('Amoxicillin', 1, 'J01CA04', 'Common penicillin'),
('Gentamicin', 2, 'J01GB03', 'Aminoglycoside');

-- Organisms
INSERT INTO organisms (name, taxonomy_id, strain, gram_strain, notes)
VALUES
('Escherichia coli', 562, 'K12', 'Gram-negative', 'Model lab strain'),
('Staphylococcus aureus', 1280, 'MRSA', 'Gram-positive', 'Methicillin-resistant');

-- Gene Families
INSERT INTO gene_families (name)
VALUES ('Beta-lactamase'), ('Aminoglycoside-modifying enzyme');

-- Resistance Mechanisms
INSERT INTO resistance_mechanisms (name, description)
VALUES ('Enzymatic degradation', 'Bacteria produce enzymes that destroy the antibiotic'),
       ('Target modification', 'Bacteria modify the antibiotic target');

-- Resistance Genes
INSERT INTO resistance_genes (name, family_id, mechanism_id, sequence_accession, notes)
VALUES
('blaTEM', 1, 1, 'NC_000913.3', 'Common beta-lactamase gene'),
('aac(6'')-Ib', 2, 1, 'NC_007779.1', 'Aminoglycoside acetyltransferase');

-- Data Sources
INSERT INTO data_sources (name, type, url, citation)
VALUES ('CARD', 'Database', 'https://card.mcmaster.ca', 'Jia et al., Nucleic Acids Res, 2017');

-- Resistance Profiles
INSERT INTO resistance_profiles (organism_id, antibiotic_id, gene_id, mechanism_id, mic_value, mic_unit, resistance_level, source_id, year, region)
VALUES
(1, 1, 1, 1, 16.0, 'µg/mL', 'Resistant', 1, 2023, 'USA'),
(2, 2, 2, 1, 4.0, 'µg/mL', 'Resistant', 1, 2023, 'USA');
