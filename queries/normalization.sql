CREATE TABLE IF NOT EXISTS semesters (
    id SERIAL PRIMARY KEY,
    year INTEGER,
    semester INTEGER
);

INSERT INTO semesters (year, semester)
SELECT DISTINCT year, semester
FROM test;

CREATE TABLE IF NOT EXISTS departments (
    module_code TEXT,
    semester_id INTEGER,
    department TEXT NOT NULL,
    PRIMARY KEY (module_code, semester_id, department),
    FOREIGN KEY (semester_id) REFERENCES semesters (id)
);

INSERT INTO departments (module_code, semester_id, department)
    SELECT DISTINCT module_code, semesters.id, department
    FROM (
        SELECT DISTINCT module_code, semester, year, department
        FROM test) AS subquery
    INNER JOIN semesters USING(semester, year)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS module_information (
    module_code TEXT,
    semester INTEGER,
    year INTEGER,
    module_title TEXT,

    PRIMARY KEY(module_code, semester, year)
    FOREIGN KEY (year, semester) REFERENCES semesters (year, semester)
)

INSERT INTO module_information
SELECT DISTINCT module_code, semester, year, module_title 
FROM test;

CREATE TABLE IF NOT EXISTS module_codes (
    module_code TEXT,
    semester INTEGER,
    year INTEGER,
    round INTEGER,
    module_class TEXT,

    ug INTEGER,
    gd INTEGER,
    dk INTEGER,
    ng INTEGER,
    cpe INTEGER,

    PRIMARY KEY
)
