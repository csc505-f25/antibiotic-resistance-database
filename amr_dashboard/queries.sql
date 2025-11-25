-- 1. List all organisms
SELECT * FROM organisms;

-- 2. List all antibiotics
SELECT a.antibiotic_id, a.name AS antibiotic, d.name AS drug_class, a.atc_code
FROM antibiotics a
LEFT JOIN drug_classes d ON a.drug_class_id = d.drug_class_id;

-- 3. List all resistance mechanisms
SELECT * FROM resistance_mechanisms;

-- 4. List all resistance genes with family and mechanism
SELECT rg.name AS gene, gf.name AS gene_family, rm.name AS mechanism
FROM resistance_genes rg
LEFT JOIN gene_families gf ON rg.family_id = gf.family_id
LEFT JOIN resistance_mechanisms rm ON rg.mechanism_id = rm.mechanism_id;

-- 5. List all resistance profiles with organism, antibiotic, and resistance level
SELECT o.name AS organism, a.name AS antibiotic, r.resistance_level, r.mic_value, r.mic_unit
FROM resistance_profiles r
LEFT JOIN organisms o ON r.organism_id = o.organism_id
LEFT JOIN antibiotics a ON r.antibiotic_id = a.antibiotic_id;

-- 6. Find all resistant organisms for a specific antibiotic
SELECT o.name AS organism, r.resistance_level
FROM resistance_profiles r
JOIN organisms o ON r.organism_id = o.organism_id
JOIN antibiotics a ON r.antibiotic_id = a.antibiotic_id
WHERE a.name = 'Amoxicillin'
  AND r.resistance_level = 'Resistant';

-- 7. List genes responsible for resistance in each organism
SELECT o.name AS organism, a.name AS antibiotic, rg.name AS gene
FROM resistance_profiles r
LEFT JOIN organisms o ON r.organism_id = o.organism_id
LEFT JOIN antibiotics a ON r.antibiotic_id = a.antibiotic_id
LEFT JOIN resistance_genes rg ON r.gene_id = rg.gene_id;

-- 8. Resistance by drug class
SELECT o.name AS organism, d.name AS drug_class, COUNT(r.profile_id) AS resistance_count
FROM resistance_profiles r
JOIN organisms o ON r.organism_id = o.organism_id
JOIN antibiotics a ON r.antibiotic_id = a.antibiotic_id
JOIN drug_classes d ON a.drug_class_id = d.drug_class_id
WHERE r.resistance_level = 'Resistant'
GROUP BY o.name, d.name
ORDER BY resistance_count DESC;

-- 9. Resistance by year and region
SELECT r.year, r.region, COUNT(*) AS resistant_cases
FROM resistance_profiles r
WHERE r.resistance_level = 'Resistant'
GROUP BY r.year, r.region
ORDER BY r.year, r.region;

-- 10. Summary: number of resistant organisms per antibiotic
SELECT a.name AS antibiotic, COUNT(DISTINCT r.organism_id) AS resistant_organisms
FROM resistance_profiles r
JOIN antibiotics a ON r.antibiotic_id = a.antibiotic_id
WHERE r.resistance_level = 'Resistant'
GROUP BY a.name
ORDER BY resistant_organisms DESC;