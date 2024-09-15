

CREATE TABLE IF NOT EXISTS Films(
	film_id BIGSERIAL PRIMARY KEY,
	title TEXT UNIQUE NOT NULL CHECK (title != ''),
	duration INT NOT NULL,
	status BOOL NOT NULL
);

CREATE TABLE IF NOT EXISTS FilmSeries(
	film_series_id BIGSERIAL PRIMARY KEY,
	film_series_name TEXT UNIQUE NOT NULL CHECK (film_series_name != '')
);

CREATE TABLE IF NOT EXISTS FilmSeriesFilms(
	film_id BIGINT,
	film_series_id BIGINT,
	FOREIGN KEY (film_id) REFERENCES Films(film_id) ON DELETE CASCADE,
    FOREIGN KEY (film_series_id) REFERENCES FilmSeries(film_series_id) ON DELETE CASCADE,
    PRIMARY KEY (film_id, film_series_id)
);

INSERT INTO Films(title, duration, status)
VALUES ('Оно', 135, TRUE);

INSERT INTO FilmSeries(film_series_name)
VALUES ('Оно'), ('Без серии');

INSERT INTO FilmSeriesFilms(film_id, film_series_id)
SELECT f.film_id, s.film_series_id
FROM Films f JOIN FilmSeries s ON f.title = 'Оно' AND s.film_series_name = 'Оно';