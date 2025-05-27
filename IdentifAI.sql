-- 1️⃣ Studenten-Tabelle (falls noch nicht existiert)
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    face_encoding BYTEA  -- Gesichtsdaten (wird später gefüllt)
);

-- 2️⃣ Prüfen, ob Spalte 'face_encoding' existiert, falls nicht → hinzufügen
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'students' AND column_name = 'face_encoding') 
    THEN 
        ALTER TABLE students ADD COLUMN face_encoding BYTEA;
    END IF;
END $$;

-- 3️⃣ Access Logs Tabelle erstellen, falls nicht existiert
CREATE TABLE IF NOT EXISTS access_logs (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(id) ON DELETE CASCADE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) CHECK (status IN ('anwesend', 'verspätet', 'fehlend'))
);

-- 4️⃣ Prüfen, ob 'status'-Spalte existiert, falls nicht → hinzufügen
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'access_logs' AND column_name = 'status') 
    THEN 
        ALTER TABLE access_logs ADD COLUMN status VARCHAR(20) 
        CHECK (status IN ('anwesend', 'verspätet', 'fehlend'));
    END IF;
END $$;

-- 5️⃣ Studenten-Daten einfügen, falls sie noch nicht existieren


ALTER TABLE students ADD CONSTRAINT unique_student_name UNIQUE (name);
INSERT INTO students (name) VALUES 
    ('Emine Acur'),
    ('Omran Almohamed'),
    ('Alexander Buczolitz'),
    ('Seif Dawoud'),
    ('Adis Duranovic'),
    ('Oleg Galatanu'),
    ('Ali Güldogan'),
    ('Edina Harcevic'),
    ('Jakob Kautschitz'),
    ('Vuk Kostic'),
    ('Marcel Malbasic'),
    ('Filip Obradovic'),
    ('Nikola Pantic'),
    ('Daniel Platanov'),
    ('Mohsen Rezaihi'),
    ('Hubert Rychter'),
    ('Johannes Schönauer'),
    ('Angelo Schreiner'),
    ('Balazs Sik'),
    ('Leopold Wagner')
ON CONFLICT (name) DO NOTHING;

SELECT column_name 
FROM information_schema.columns 
WHERE table_name = 'students' AND column_name = 'face_encoding';



-- 6️⃣ Aktuelle Anwesenheitsliste für Lehrer anzeigen
SELECT s.name, a.timestamp, a.status
FROM students s
LEFT JOIN access_logs a ON s.id = a.student_id
ORDER BY a.timestamp DESC;

SELECT name, LENGTH(face_encoding) AS encoding_bytes
FROM students
WHERE face_encoding IS NOT NULL;

