-- Удаление существующих таблиц, если они есть
DROP TABLE IF EXISTS BookAuthors;
DROP TABLE IF EXISTS BookGenres;
DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Authors;
DROP TABLE IF EXISTS BookSeries;
DROP TABLE IF EXISTS Genres;
DROP TABLE IF EXISTS BookSeriesBooks; -- Новая промежуточная таблица

-- Создание таблиц
CREATE TABLE IF NOT EXISTS Authors (
    author_id BIGSERIAL PRIMARY KEY,
    author_name TEXT UNIQUE NOT NULL CHECK (author_name != '')
);

CREATE TABLE IF NOT EXISTS Genres (
    genre_id BIGSERIAL PRIMARY KEY,
    genre_name TEXT UNIQUE NOT NULL CHECK (genre_name != '')
);

CREATE TABLE IF NOT EXISTS BookSeries (
    book_series_id BIGSERIAL PRIMARY KEY,
    book_series_name TEXT UNIQUE NOT NULL CHECK (book_series_name != '')
);

CREATE TABLE IF NOT EXISTS Books (
    book_id BIGSERIAL PRIMARY KEY,
    title TEXT UNIQUE NOT NULL CHECK (title != ''),
    reading_start_day DATE,
    reading_end_day DATE,
    symbols_amount INT NOT NULL,
    status BOOL NOT NULL
);

-- Промежуточная таблица для связи "многие ко многим" между Books и BookSeries
CREATE TABLE IF NOT EXISTS BookSeriesBooks (
    book_id BIGINT,
    book_series_id BIGINT,
    FOREIGN KEY (book_id) REFERENCES Books(book_id) ON DELETE CASCADE,
    FOREIGN KEY (book_series_id) REFERENCES BookSeries(book_series_id) ON DELETE CASCADE,
    PRIMARY KEY (book_id, book_series_id)
);

CREATE TABLE IF NOT EXISTS BookAuthors (
    book_id BIGINT,
    author_id BIGINT,
    FOREIGN KEY (book_id) REFERENCES Books(book_id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES Authors(author_id) ON DELETE CASCADE,
    PRIMARY KEY (book_id, author_id)
);

CREATE TABLE IF NOT EXISTS BookGenres (
    book_id BIGINT,
    genre_id BIGINT,
    FOREIGN KEY (book_id) REFERENCES Books(book_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES Genres(genre_id) ON DELETE CASCADE,
    PRIMARY KEY (book_id, genre_id)
);

-- Вставка данных
INSERT INTO Authors(author_name) VALUES 
    ('Сергей Лукьяненко'), 
    ('Ник Перумов');

INSERT INTO BookSeries(book_series_name) VALUES 
    ('Без серии'), 
    ('Не время для драконов');

INSERT INTO Genres(genre_name) VALUES 
    ('Роман'), 
    ('Научная фантастика'), 
    ('Фэнтези');

-- Вставка данных в таблицу Books
INSERT INTO Books(title, reading_start_day, reading_end_day, symbols_amount, status)
VALUES 
    ('Мальчик и тьма', NULL, NULL, 382, TRUE),
    ('Не время для драконов', NULL, NULL, 710, TRUE),
    ('Не место для людей', NULL, NULL, 688, TRUE);

-- Вставка данных в таблицу BookSeriesBooks
INSERT INTO BookSeriesBooks(book_id, book_series_id)
VALUES
    ((SELECT book_id FROM Books WHERE title = 'Мальчик и тьма'), (SELECT book_series_id FROM BookSeries WHERE book_series_name = 'Без серии')),
    ((SELECT book_id FROM Books WHERE title = 'Не время для драконов'), (SELECT book_series_id FROM BookSeries WHERE book_series_name = 'Не время для драконов')),
    ((SELECT book_id FROM Books WHERE title = 'Не место для людей'), (SELECT book_series_id FROM BookSeries WHERE book_series_name = 'Не время для драконов'));

-- Вставка данных в таблицу BookAuthors
INSERT INTO BookAuthors(book_id, author_id)
SELECT
    b.book_id,
    a.author_id
FROM Books b
JOIN Authors a ON a.author_name IN ('Сергей Лукьяненко') AND b.title = 'Мальчик и тьма';

INSERT INTO BookAuthors(book_id, author_id)
SELECT
    b.book_id,
    a.author_id
FROM Books b
JOIN Authors a ON a.author_name IN ('Сергей Лукьяненко', 'Ник Перумов') AND b.title IN ('Не время для драконов', 'Не место для людей');

-- Вставка данных в таблицу BookGenres
INSERT INTO BookGenres(book_id, genre_id)
SELECT
    b.book_id,
    g.genre_id
FROM Books b
JOIN Genres g ON g.genre_name IN ('Роман', 'Научная фантастика', 'Фэнтези');
