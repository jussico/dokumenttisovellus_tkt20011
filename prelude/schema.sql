
DROP TABLE IF EXISTS review;
DROP TABLE IF EXISTS doc;
DROP TABLE IF EXISTS doc_user;

CREATE TABLE doc_user (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    first_name TEXT,
    last_name TEXT,
    password TEXT,
    is_admin BOOLEAN,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
ALTER SEQUENCE doc_user_id_seq RESTART WITH 1;

CREATE TABLE doc (
    id SERIAL PRIMARY KEY,
    title TEXT,
    file_name TEXT,
    content TEXT,
    created_by INTEGER REFERENCES doc_user,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
ALTER SEQUENCE doc_id_seq RESTART WITH 1;

CREATE TABLE review (
    id SERIAL PRIMARY KEY,
    doc_id INTEGER REFERENCES doc,
    title TEXT,
    content TEXT,
    star_count INTEGER,
    created_by INTEGER REFERENCES doc_user,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
ALTER SEQUENCE review_id_seq RESTART WITH 1;
