DROP_DB = """
DROP TABLE IF EXISTS Artysta CASCADE;
DROP TABLE IF EXISTS Eksponat CASCADE;
DROP TABLE IF EXISTS Instytucja CASCADE;
DROP TABLE IF EXISTS Wypozyczenie;
DROP TABLE IF EXISTS Wystawienie;
DROP TABLE IF EXISTS Magazynowanie;
DROP TABLE IF EXISTS Galeria;
"""


DB_INIT = """
DROP TABLE IF EXISTS Artysta CASCADE;
DROP TABLE IF EXISTS Eksponat CASCADE;
DROP TABLE IF EXISTS Instytucja CASCADE;
DROP TABLE IF EXISTS Wypozyczenie;
DROP TABLE IF EXISTS Wystawienie;
DROP TABLE IF EXISTS Magazynowanie;
DROP TABLE IF EXISTS Galeria;

CREATE TABLE Artysta (
    id NUMERIC(4) PRIMARY KEY,
    imie VARCHAR(40) NOT NULL,
    nazwisko VARCHAR(40) NOT NULL,
    rok_urodzenia DATE NOT NULL,
    rok_smierci DATE
);

CREATE TABLE Eksponat (
    id NUMERIC(4) PRIMARY KEY,
    tytul VARCHAR(40) NOT NULL,
    typ VARCHAR(40) NOT NULL,
    wysokosc NUMERIC(4) NOT NULL,
    szerokosc NUMERIC(4) NOT NULL,
    waga NUMERIC(4) NOT NULL,
    artysta_id NUMERIC(4) REFERENCES Artysta
);

CREATE TABLE Galeria (
    id NUMERIC(4) PRIMARY KEY, 
    nazwa VARCHAR(40) NOT NULL,
    liczba_sal NUMERIC(4) NOT NULL
);

CREATE TABLE Instytucja (
    id NUMERIC(4) PRIMARY KEY,
    nazwa VARCHAR(40) NOT NULL,
    miasto VARCHAR(40) NOT NULL
);

CREATE TABLE Magazynowanie (
    id NUMERIC(4) PRIMARY KEY,
    id_eksponatu NUMERIC(4) NOT NULL REFERENCES Eksponat,
    poczatek DATE,
    koniec DATE
);

CREATE TABLE Wystawienie (
    id NUMERIC(4) PRIMARY KEY,
    id_eksponatu NUMERIC(4) NOT NULL REFERENCES Eksponat,
    sala NUMERIC(4) NOT NULL, 
    id_galerii NUMERIC(4) NOT NULL REFERENCES Galeria,
    poczatek DATE,
    koniec DATE
);

CREATE TABLE Wypozyczenie (
    id NUMERIC(4) PRIMARY KEY,
    id_eksponatu NUMERIC(4) NOT NULL REFERENCES Eksponat,
    id_instytucji NUMERIC(4) NOT NULL REFERENCES Instytucja,
    poczatek DATE,
    koniec DATE
);

/*
    Potrzebne TRIGGERY:
    - trigger zapewniający, że żaden eksponat nie przebywa poza muzeum dłużej niż 30 dni rocznie
    - muzeum powinno zawsze mieć w swoich galeriach lub w magazynie co najmniej jeden eksponat każdego artysty.
*/


-- Trigger zapewniający, że trzymamy tylko artystów, którzy są autorami jakichś eksponatów
CREATE OR REPLACE FUNCTION f1 () RETURNS TRIGGER AS $$
DECLARE
    ile integer;
    autor integer;
BEGIN
    IF old.autor_id IS NOT NULL THEN
        SELECT old.autor_id INTO autor;
        SELECT COUNT(*) INTO ile
        FROM Eksponat
        WHERE autor_id = old.autor_id;
        IF (ile == 0) THEN
            raise notice 'Usunięcia ostatniego dzieła artysty, %', autor;
            raise notice 'Usuwam go z bazy danych';
            DELETE FROM Artysta WHERE id = autor;
        END IF;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER t1
AFTER UPDATE OR DELETE ON Eksponat FOR EACH ROW
EXECUTE PROCEDURE f1();
"""

DB_SAMPLE = """
    -- Galerie
    INSERT INTO Galeria VALUES (1, 'Galeria Klasyków', 4);
    INSERT INTO Galeria VALUES (2, 'Galeria Sztuki Nowoczesnej', 3);

    -- Artyści
    INSERT INTO Artysta VALUES (1, 'Francesco', 'Ramazotti', '1959-03-09', '2009-10-18');
    INSERT INTO Artysta VALUES (2, 'Vincent', 'Moore', '1982-11-12', NULL);

    -- Eksponaty
    INSERT INTO Eksponat VALUES (1, 'W poszukiwaniu buga', 'Obraz', 150, 100, 3, 1);
    INSERT INTO Eksponat VALUES (2, 'Null o poranku', 'Obraz', 59, 90, 1, 1);
    INSERT INTO Eksponat VALUES (3, 'Złoty Procesor', 'Rzeźba', 120, 90, 12, 2);

    -- Instytucje
    INSERT INTO Instytucja VALUES (1, 'Prywatne Muzeum w Toruniu', 'Toruń');

    -- Magazynowanie
    INSERT INTO Magazynowanie VALUES (1, 1, '2021-12-02', NULL);
    INSERT INTO Magazynowanie VALUES (2, 2, '2021-12-02', NULL);
    INSERT INTO Magazynowanie VALUES (3, 3, '2021-12-02', NULL);
"""

LIST_TABLES = """
    SELECT tablename
    FROM pg_catalog.pg_tables
    WHERE schemaname = 'scott' AND
    tableowner = 'scott';
"""

GET_EKSPONAT = """
    SELECT * FROM eksponat;
"""

GET_EKSPONAT_WITH_ARTYSTA = """
    SELECT eksponat.*, artysta.imie, artysta.nazwisko FROM eksponat INNER JOIN artysta ON eksponat.artysta_id =artysta.id;
"""

GET_ARTYSTA = """
    SELECT * FROM artysta;
"""

GET_GALERIA = """
    SELECT * FROM galeria;
"""

GET_INSTYTUCJA = """
    SELECT * FROM instytucja;
"""

GET_MAGAZYNOWANIE = """
    SELECT * FROM magazynowanie;
"""

GET_WYPOZYCZENIE = """
    SELECT * FROM wypozyczenie;
"""

GET_WYSTAWIENIE = """
    SELECT * FROM wystawienie;
"""

ADD_TO_EKSPONAT = """
    INSERT INTO eksponat
    (id, tytul, typ, wysokosc, szerokosc, waga, artysta_id) 
    VALUES (%s, %s, %s, %s, %s, %s, %s);
"""

ADD_TO_ARTYSTA = """
    INSERT INTO artysta
    (id, imie, nazwisko, rok_urodzenia, rok_smierci) 
    VALUES (%s, %s, %s, %s, %s);
"""

ADD_TO_GALERIA = """
    INSERT INTO galeria
    (id, nazwa, liczba_sal)
    VALUES (%s, %s, %s);
"""