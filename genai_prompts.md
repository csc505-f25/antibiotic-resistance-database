# genai_prompts.md

### Prompt 1
Help me design a SQL schema for an antimicrobial resistance database including organisms, antibiotics, and resistance genes.


**Response Summary:**  
ChatGPT generated a normalized SQL schema with tables for organisms, antibiotics, drug classes, resistance genes, mechanisms, gene families, and resistance profiles. It included primary/foreign keys, field types, and optimized relationships for efficient querying.

---

### Prompt 2
Write Python code to extract AMR gene and MIC data from NCBI Pathogen Detection.

**Response Summary:**  
ChatGPT described how to use NCBI’s Pathogen Detection FTP and API endpoints to retrieve metadata, AMR genes, and MIC results. It provided example Python scripts using `requests` and `pandas` to automate data download and parsing. I got the information in "data/bacteria_taxonomy.csv" and "data/bacteria_list.txt" from this script.
---

### Prompt 3
Give me a week-by-week development plan for my AMR database and dashboard project.

**Response Summary:**  
ChatGPT created a detailed roadmap outlining weekly goals: database setup, data ingestion, indexing, writing SQL summary queries, and building a dashboard prototype with Python visualization libraries.

### Prompt 4
{Pasted antibiotic data from ATC/DDD Index} Format this to add to my antibiotic csv.
Chat GPT gave me code formatted as a section of a csv file with "antibiotic_id,name,drug_class_id,atc_code,notes" as a header. I ran this multiple times as I went through the index. It allowed me to quickly populate my "antibiotic.csv" and "drug_class.csv" files.