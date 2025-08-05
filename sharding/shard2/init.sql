CREATE TABLE IF NOT EXISTS users
(
    id      SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name    TEXT    NOT NULL
);

INSERT INTO users (user_id, name)
VALUES (3, 'lee'),
       (5, 'choi');
