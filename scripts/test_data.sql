
DELETE FROM review;
DELETE FROM doc;
DELETE FROM doc_user;

-- doc_user

INSERT INTO doc_user(username, first_name, last_name, password, is_admin) 
    VALUES ('amiga', 'Raoul', 'Duke', 'amiga', true);

INSERT INTO doc_user(username, first_name, last_name, password, is_admin) 
    VALUES ('atari', 'John', 'Rambo', 'atari', false);

INSERT INTO doc_user(username, first_name, last_name, password, is_admin) 
    VALUES ('amstrad', 'White', 'Rabbit', 'amstrad', true);

INSERT INTO doc_user(username, first_name, last_name, password, is_admin) 
    VALUES ('sega', 'Rising', 'Sun', 'sega', false);

-- doc

INSERT INTO doc(title, file_name, content, created_by) 
    VALUES ('Title1', 'Filename1', 'Content1', 1);

INSERT INTO doc(title, file_name, content, created_by) 
    VALUES ('Title2', 'Filename2', 'Content2', 1);

INSERT INTO doc(title, file_name, content, created_by) 
    VALUES ('Title3', 'Filename3', 'Content3', 3);

INSERT INTO doc(title, file_name, content, created_by) 
    VALUES ('Title3', 'Filename3', 'Content3', 3);
