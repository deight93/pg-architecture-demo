CREATE TABLE IF NOT EXISTS test_table
(
    id    SERIAL PRIMARY KEY,
    value TEXT
);

INSERT INTO test_table (value)
VALUES ('master 데이터 1'),
       ('master 데이터 2');
