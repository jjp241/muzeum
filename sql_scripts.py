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
    imię VARCHAR(40) NOT NULL,
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

LIST_TABLES = """
    SELECT tablename
    FROM pg_catalog.pg_tables
    WHERE schemaname = 'scott' AND
    tableowner = 'scott';
"""