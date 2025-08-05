CREATE TABLE IF NOT EXISTS users
(
    id      SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name    TEXT    NOT NULL
);

INSERT INTO users (user_id, name)
VALUES (2, 'kim'),
       (4, 'park');
