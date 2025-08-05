CREATE TABLE IF NOT EXISTS users
(
    id       SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    email    TEXT NOT NULL
);

CREATE INDEX idx_users_email ON users (email);

-- 샘플 데이터 삽입
INSERT INTO users (username, email)
SELECT 'user_' || i,
       'user_' || i || '@example.com'
FROM generate_series(1, 1000) AS s(i);
