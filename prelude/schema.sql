
-- CURRENT
DROP TABLE IF EXISTS doc_note_history;
DROP TABLE IF EXISTS doc_note;
DROP TABLE IF EXISTS doc_owner;
DROP TABLE IF EXISTS doc_keyword;
DROP TABLE IF EXISTS keyword;
DROP TABLE IF EXISTS doc;
DROP TABLE IF EXISTS user_account;

CREATE TABLE user_account (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    first_name TEXT,
    last_name TEXT,
    password TEXT,
    is_admin BOOLEAN,
    is_superuser BOOLEAN,
    enabled BOOLEAN DEFAULT TRUE,
    modified_by INTEGER REFERENCES user_account,
    created_by INTEGER REFERENCES user_account,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP    
);
ALTER SEQUENCE user_account_id_seq RESTART WITH 1;

CREATE TABLE doc (
    id SERIAL PRIMARY KEY,
    title TEXT,
    file_name TEXT,
    description TEXT,
    modified_by INTEGER REFERENCES user_account,
    created_by INTEGER REFERENCES user_account,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
ALTER SEQUENCE doc_id_seq RESTART WITH 1;

CREATE TABLE keyword (
    id SERIAL PRIMARY KEY,
    word TEXT,
    created_by INTEGER REFERENCES user_account,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
ALTER SEQUENCE keyword_id_seq RESTART WITH 1;

CREATE TABLE doc_keyword (
    id SERIAL PRIMARY KEY,
    keyword_id INTEGER REFERENCES keyword,
    doc_id INTEGER REFERENCES doc,    
    created_by INTEGER REFERENCES user_account,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
ALTER SEQUENCE doc_keyword_id_seq RESTART WITH 1;

CREATE TABLE doc_owner (
    id SERIAL PRIMARY KEY,
    doc_id INTEGER REFERENCES doc,
    owner_id INTEGER REFERENCES user_account,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(doc_id, owner_id)
);
ALTER SEQUENCE doc_owner_id_seq RESTART WITH 1;

CREATE TABLE doc_note (
    id SERIAL PRIMARY KEY,
    doc_id INTEGER REFERENCES doc,
    title TEXT,
    content TEXT,
    modified_by INTEGER REFERENCES user_account,
    modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES user_account,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
ALTER SEQUENCE doc_note_id_seq RESTART WITH 1;

CREATE TABLE doc_note_history (
    id SERIAL PRIMARY KEY,
    doc_note_id INTEGER,
    doc_id INTEGER,
    title TEXT,
    content TEXT,
    modified_by INTEGER,
    modified_date TIMESTAMP
);
ALTER SEQUENCE doc_note_history_id_seq RESTART WITH 1;

-- FUNCTION to update note history
CREATE OR REPLACE FUNCTION doc_note_history_updater() RETURNS TRIGGER AS $new$
BEGIN
INSERT INTO doc_note_history(doc_note_id, doc_id, title, content, modified_by, modified_date)
VALUES (new.id, new.doc_id, new.title, new.content, new.modified_by, new.modified_date);
RETURN NEW;
END;
$new$ LANGUAGE plpgsql;

-- TRIGGER to update note history
CREATE TRIGGER update_doc_note_history AFTER UPDATE ON doc_note
FOR EACH ROW EXECUTE PROCEDURE doc_note_history_updater();

CREATE TRIGGER update_doc_note_history_after_insert AFTER INSERT ON doc_note
FOR EACH ROW EXECUTE PROCEDURE doc_note_history_updater();
