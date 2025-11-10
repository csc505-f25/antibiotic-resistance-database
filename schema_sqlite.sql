-- Antibiotic Resistance Database (SQLite-compatible)

-- Drop tables if they exist (in reverse dependency order)
DROP TABLE IF EXISTS resistance_profiles;
DROP TABLE IF EXISTS resistance_genes;
DROP TABLE IF EXISTS antibiotics;
DROP TABLE IF EXISTS organisms;
DROP TABLE IF EXISTS drug_classes;
DROP TABLE IF EXISTS resistance_mechanisms;
DROP TABLE IF EXISTS gene_families;
DROP TABLE IF EXISTS data_sources;

-- Organisms
CREATE TABLE IF NOT EXISTS organisms (
    organism_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    taxonomy_id INTEGER,
    strain TEXT,
    gram_stain TEXT,
    notes TEXT
);

-- Drug Classes
CREATE TABLE IF NOT EXISTS drug_classes (
    drug_class_id TEXT PRIMARY KEY,
    name VARCHAR(255),
    description TEXT
);

-- Antibiotics
CREATE TABLE IF NOT EXISTS antibiotics (
    antibiotic_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    drug_class_id TEXT,
    atc_code TEXT,
    notes TEXT,
    FOREIGN KEY (drug_class_id) REFERENCES drug_classes (drug_class_id)
);

-- Gene Families
CREATE TABLE IF NOT EXISTS gene_families (
    family_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

-- Resistance Mechanisms
CREATE TABLE IF NOT EXISTS resistance_mechanisms (
    resistance_mechanism_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
);

-- Resistance Genes
CREATE TABLE IF NOT EXISTS resistance_genes (
    resistance_gene_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    family_id INTEGER,
    mechanism_id INTEGER,
    sequence_accession TEXT,
    notes TEXT,
    FOREIGN KEY (family_id) REFERENCES gene_families (family_id),
    FOREIGN KEY (mechanism_id) REFERENCES resistance_mechanisms (mechanism_id)
);

-- Data Sources
CREATE TABLE IF NOT EXISTS data_sources (
    source_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT,
    url TEXT,
    citation TEXT
);

-- Resistance Profiles
CREATE TABLE IF NOT EXISTS resistance_profiles (
    profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
    organism_id INTEGER,
    antibiotic_id INTEGER,
    resistance_gene_id INTEGER,
    mechanism_id INTEGER,
    mic_value REAL,
    mic_unit TEXT,
    resistance_level TEXT,
    source_id INTEGER,
    year INTEGER,
    region TEXT,
    FOREIGN KEY (organism_id) REFERENCES organisms (organism_id),
    FOREIGN KEY (antibiotic_id) REFERENCES antibiotics (antibiotic_id),
    FOREIGN KEY (resistance_gene_id) REFERENCES resistance_genes (resistance_gene_id),
    FOREIGN KEY (mechanism_id) REFERENCES resistance_mechanisms (mechanism_id),
    FOREIGN KEY (source_id) REFERENCES data_sources (source_id)
);

-- Indexes
CREATE INDEX idx_org ON resistance_profiles (organism_id);
CREATE INDEX idx_antibiotic ON resistance_profiles (antibiotic_id);
CREATE INDEX idx_region ON resistance_profiles (region);
CREATE INDEX idx_year ON resistance_profiles (year);
