SELECT condition, COUNT(DISTINCT subject_id) AS number_of_subjects
FROM research_data.subjects
GROUP BY condition;

-- wwrite a query that returns all melanoma PBMC samples at baseline (time_from_treatment_start is 0) from patients who have treatment tr1.


SELECT subject_name, sample_name, age, sex, response, project_name
FROM research_data.samples as s
JOIN research_data.subjects as sub ON s.subject_id = sub.subject_id
JOIN research_data.projects as p ON sub.project_id = p.project_id
JOIN research_data.treatments as t ON s.treatment_id = t.treatment_id
WHERE t.treatment_name = 'tr1' 
AND sub.condition = 'melanoma'
AND s.sample_type = 'PBMC' 
AND s.time_from_treatment_start = 0;


SELECT p.project_name, COUNT(s.sample_name) AS sample_count
FROM research_data.samples as s
JOIN research_data.subjects as sub ON s.subject_id = sub.subject_id
JOIN research_data.projects as p ON sub.project_id = p.project_id
JOIN research_data.treatments as t ON s.treatment_id = t.treatment_id
WHERE t.treatment_name = 'tr1' 
AND sub.condition = 'melanoma'
AND s.sample_type = 'PBMC' 
AND s.time_from_treatment_start = 0
GROUP BY p.project_name;


SELECT sex,COUNT(sub.sex) AS sample_count
FROM research_data.samples as s
JOIN research_data.subjects as sub ON s.subject_id = sub.subject_id
JOIN research_data.projects as p ON sub.project_id = p.project_id
JOIN research_data.treatments as t ON s.treatment_id = t.treatment_id
WHERE t.treatment_name = 'tr1' 
AND sub.condition = 'melanoma'
AND s.sample_type = 'PBMC' 
AND s.time_from_treatment_start = 0
GROUP BY sub.sex;