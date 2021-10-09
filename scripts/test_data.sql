
DELETE FROM doc_note_history;
DELETE FROM doc_note;
DELETE FROM doc_owner;
DELETE FROM doc_keyword;
DELETE FROM keyword;
DELETE FROM doc;
DELETE FROM user_account;

-- user_account

INSERT INTO user_account(username, first_name, last_name, password, is_admin, is_superuser, modified_by, created_by) 
    VALUES ('amiga', 'Raoul', 'Duke', 'amiga', true, true, 1, 1);

INSERT INTO user_account(username, first_name, last_name, password, is_admin, is_superuser, modified_by, created_by) 
    VALUES ('atari', 'John', 'Rambo', 'atari', true, false, 1, 1);

INSERT INTO user_account(username, first_name, last_name, password, is_admin, is_superuser, modified_by, created_by) 
    VALUES ('amstrad', 'White', 'Rabbit', 'amstrad', false, false, 1, 1);

INSERT INTO user_account(username, first_name, last_name, password, is_admin, is_superuser, modified_by, created_by) 
    VALUES ('sega', 'Rising', 'Sun', 'sega', false, false, 1, 1);

-- doc

INSERT INTO doc(title, file_name, description, created_by, modified_by) 
    VALUES ('Title1', 'Filename1', 'description1', 1, 1);

INSERT INTO doc(title, file_name, description, created_by, modified_by) 
    VALUES ('Title2', 'Filename2', 'description2', 1, 1);

INSERT INTO doc(title, file_name, description, created_by, modified_by) 
    VALUES ('Title3', 'Filename3', 'description3', 3, 3);

INSERT INTO doc(title, file_name, description, created_by, modified_by) 
    VALUES ('Title3', 'Filename3', 'description3', 3, 3);

-- keyword
INSERT INTO keyword(word, created_by) 
    VALUES ('cheese', 1);

INSERT INTO keyword(word, created_by) 
    VALUES ('cake', 1);

INSERT INTO keyword(word, created_by) 
    VALUES ('retro', 1);

INSERT INTO keyword(word, created_by) 
    VALUES ('wow', 1);

-- doc_keyword
INSERT INTO doc_keyword(keyword_id, doc_id, created_by) 
    VALUES (1,1,1);

INSERT INTO doc_keyword(keyword_id, doc_id, created_by) 
    VALUES (1,2,1);

INSERT INTO doc_keyword(keyword_id, doc_id, created_by) 
    VALUES (1,3,1);

INSERT INTO doc_keyword(keyword_id, doc_id, created_by) 
    VALUES (2,1,1);

INSERT INTO doc_keyword(keyword_id, doc_id, created_by) 
    VALUES (3,1,1);

INSERT INTO doc_keyword(keyword_id, doc_id, created_by) 
    VALUES (3,2,1);

INSERT INTO doc_keyword(keyword_id, doc_id, created_by) 
    VALUES (3,3,1);

INSERT INTO doc_keyword(keyword_id, doc_id, created_by) 
    VALUES (3,4,1);

INSERT INTO doc_keyword(keyword_id, doc_id, created_by) 
    VALUES (2,4,1);

INSERT INTO doc_keyword(keyword_id, doc_id, created_by) 
    VALUES (1,4,1);



-- doc_owner
INSERT INTO doc_owner(doc_id, owner_id) 
    VALUES (1,1);

INSERT INTO doc_owner(doc_id, owner_id) 
    VALUES (2,1);

INSERT INTO doc_owner(doc_id, owner_id) 
    VALUES (3,2);

INSERT INTO doc_owner(doc_id, owner_id) 
    VALUES (4,3);


-- doc_note
INSERT INTO doc_note(doc_id, title, content, modified_by, created_by) 
    VALUES (1, 'what about this?', 'if there is rain there is wet', 1, 1);

INSERT INTO doc_note(doc_id, title, content, modified_by, created_by) 
    VALUES (1, 'remember this', 'there is always more!', 2, 1);

INSERT INTO doc_note(doc_id, title, content, modified_by, created_by) 
    VALUES (2, 'todo', 'buy milk', 2, 3);

INSERT INTO doc_note(doc_id, title, content, modified_by, created_by) 
    VALUES (2, 'dont do', 'haha', 4, 1);

INSERT INTO doc_note(doc_id, title, content, modified_by, created_by) 
    VALUES (3, 'in the summer', 'go wild!', 1, 1);

INSERT INTO doc_note(doc_id, title, content, modified_by, created_by) 
    VALUES (4, 'seriously now', 'if you can', 1, 1);


-- doc_note_history
UPDATE doc_note
SET 
title = 'what about this NOW?',
content = 'if there is rain there is wet ALWAYS?',
modified_by = 2
WHERE id = 1;

UPDATE doc_note
SET 
title = 'what about this NOW AGAIN?',
content = 'if there is rain there is wet ALWAYS??',
modified_by = 2
WHERE id = 1;

UPDATE doc_note
SET 
title = 'what about this NOW oujea AGAIN?',
content = 'if there is rain there is wet almost ALWAYS??',
modified_by = 3
WHERE id = 1;

UPDATE doc_note
SET 
title = 'remember this.',
content = 'there is always more!!',
modified_by = 3
WHERE id = 2;

UPDATE doc_note
SET 
title = 'remember this..',
content = 'there is always more!!!',
modified_by = 2
WHERE id = 2;

UPDATE doc_note
SET 
title = 'remember this...',
content = 'there is always more!!!?',
modified_by = 1
WHERE id = 2;

UPDATE doc_note
SET 
title = 'TODO',
content = 'buy milk and beer',
modified_by = 1
WHERE id = 3;

UPDATE doc_note
SET 
title = 'TODO',
content = 'no more beer!',
modified_by = 3
WHERE id = 3;

UPDATE doc_note
SET 
title = 'do not do',
content = 'ha ha',
modified_by = 1
WHERE id = 4;

/* INSERT INTO doc_note(doc_id, title, content, modified_by, created_by) 
    VALUES (3, 'in the summer', 'go wild!', 1, 1);

INSERT INTO doc_note(doc_id, title, content, modified_by, created_by) 
    VALUES (4, 'seriously now', 'if you can', 1, 1); */
