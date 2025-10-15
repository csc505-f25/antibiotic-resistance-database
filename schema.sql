-- Antibiotic Resistance Database

-- Drop tables if they exist (in reverse dependency order)
DROP TABLE IF EXISTS resistance_profiles CASCADE;
DROP TABLE IF EXISTS resistance_genes CASCADE;
DROP TABLE IF EXISTS antibiotics CASCADE;
DROP TABLE IF EXISTS organisms CASCADE;
DROP TABLE IF EXISTS drug_classes CASCADE;
DROP TABLE IF EXISTS resistance_mechanisms CASCADE;
DROP TABLE IF EXISTS gene_families CASCADE;
DROP TABLE IF EXISTS data_sources CASCADE;

-- Organism
CREATE TABLE IF NOT EXISTS organisms (
    organism_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    taxonomy_id INT,
    strain VARCHAR(255),
    gram_strain VARCHAR(50),
    notes TEXT
);

-- Drug Classes
CREATE TABLE IF NOT EXISTS drug_classes (
    drug_class_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

-- Antibiotics
CREATE TABLE IF NOT EXISTS antibiotics (
    antibiotic_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    drug_class_id SERIAL REFERENCES drug_classes (drug_class_id),
    atc_code VARCHAR(255),
    notes TEXT
);

-- Gene Families
CREATE TABLE IF NOT EXISTS gene_families (
    family_id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);

-- Resistance Mechanism
CREATE TABLE IF NOT EXISTS resistance_mechanisms (
    mechanism_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

-- Resistance Genes
CREATE TABLE IF NOT EXISTS resistance_genes (
    gene_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    family_id INT REFERENCES gene_families (family_id),
    mechanism_id INT REFERENCES resistance_mechanisms (mechanism_id),
    sequence_accession VARCHAR(255),
    notes TEXT
);

-- Data Source
CREATE TABLE IF NOT EXISTS data_sources (
    source_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100),
    url VARCHAR(50),
    citation TEXT
);

-- Resistance Profiles
CREATE TABLE IF NOT EXISTS resistance_profiles (
    profile_id SERIAL PRIMARY KEY,
    organism_id INT REFERENCES organisms (organism_id),
    antibiotic_id INT REFERENCES antibiotics (antibiotic_id),
    gene_id INT REFERENCES resistance_genes (gene_id),
    mechanism_id INT REFERENCES resistance_mechanisms (mechanism_id),
    mic_value FLOAT,
    mic_unit VARCHAR(50),
    resistance_level VARCHAR(100),
    source_id INT REFERENCES data_sources(source_id),
    year INT,
    region VARCHAR(255)
);