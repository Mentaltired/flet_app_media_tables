DROP TABLE IF EXISTS AnimeBookSeriesAnimeBooks;
DROP TABLE IF EXISTS AnimeBooks;
DROP TABLE IF EXISTS AnimeBookSeries;

CREATE TABLE IF NOT EXISTS AnimeBooks(
	anime_book_id BIGSERIAL PRIMARY KEY,
    title TEXT UNIQUE NOT NULL CHECK (title != ''),
    symbols_amount INT NOT NULL,
    status BOOL NOT NULL
);

CREATE TABLE IF NOT EXISTS AnimeBookSeries(
	anime_book_series_id BIGSERIAL PRIMARY KEY,
    anime_book_series_name TEXT UNIQUE NOT NULL CHECK (anime_book_series_name != '')
);

CREATE TABLE IF NOT EXISTS AnimeBookSeriesAnimeBooks(
	anime_book_id BIGINT,
    anime_book_series_id BIGINT,
    FOREIGN KEY (anime_book_id) REFERENCES AnimeBooks(anime_book_id) ON DELETE CASCADE,
    FOREIGN KEY (anime_book_series_id) REFERENCES AnimeBookSeries(anime_book_series_id) ON DELETE CASCADE,
    PRIMARY KEY (anime_book_id, anime_book_series_id)
);

INSERT INTO AnimeBooks(title, symbols_amount, status)
VALUES ('Богиня отбросов и золотой монеты', 344, TRUE);

INSERT INTO AnimeBookSeries(anime_book_series_name)
VALUES ('Без серии');

INSERT INTO AnimeBookSeriesAnimeBooks(anime_book_id, anime_book_series_id)
SELECT b.anime_book_id, s.anime_book_series_id
FROM AnimeBooks b JOIN AnimeBookSeries s ON b.title = 'Богиня отбросов и золотой монеты' AND s.anime_book_series_name = 'Без серии';
	