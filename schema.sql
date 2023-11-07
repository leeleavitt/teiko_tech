-- We create a schema named 'research_data'
CREATE SCHEMA research_data;

-- Creating table for Projects
CREATE TABLE research_data.projects (
    project_id SERIAL PRIMARY KEY,
    project_name VARCHAR(50) UNIQUE NOT NULL
);

-- Creating table for Subjects
CREATE TABLE research_data.subjects (
    subject_id SERIAL PRIMARY KEY,
    subject_name VARCHAR(50) UNIQUE NOT NULL,
    project_id INT REFERENCES research_data.projects(project_id) ON DELETE CASCADE,
    age INT,
    sex CHAR(1),
    condition VARCHAR(50),
    UNIQUE(subject_id, project_id)
);

-- Creating table for Treatments
CREATE TABLE research_data.treatments (
    treatment_id SERIAL PRIMARY KEY,
    treatment_name VARCHAR(50) UNIQUE NOT NULL
);

-- Creating table for Samples
CREATE TABLE research_data.samples (
    sample_id SERIAL PRIMARY KEY,
    subject_id INT REFERENCES research_data.subjects(subject_id) ON DELETE CASCADE,
    treatment_id INT REFERENCES research_data.treatments(treatment_id) ON DELETE SET NULL,
    response CHAR(1),
    sample_name VARCHAR(50),
    sample_type VARCHAR(50),
    time_from_treatment_start INT
);

-- Creating table for CellCounts
CREATE TABLE research_data.cell_counts (
    cell_count_id SERIAL PRIMARY KEY,
    sample_id INT REFERENCES research_data.samples(sample_id) ON DELETE CASCADE,
    b_cell INT,
    cd8_t_cell INT,
    cd4_t_cell INT,
    nk_cell INT,
    monocyte INT
);

