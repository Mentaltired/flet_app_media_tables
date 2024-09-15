DROP TABLE IF EXISTS AnimeSeriesAnimes;
DROP TABLE IF EXISTS AnimeSeries;
DROP TABLE IF EXISTS Animes;

CREATE TABLE IF NOT EXISTS Animes(
	anime_id BIGSERIAL PRIMARY KEY,
	title TEXT UNIQUE NOT NULL CHECK (title != ''),
	number_of_episode INT NOT NULL,
	status BOOL NOT NULL
);

CREATE TABLE AnimeSeries(
	anime_series_id BIGSERIAL PRIMARY KEY,
	anime_series_name TEXT UNIQUE NOT NULL CHECK (anime_series_name != '')
);

CREATE TABLE AnimeSeriesAnimes(
	anime_id BIGINT,
	anime_series_id BIGINT,
	FOREIGN KEY (anime_id) REFERENCES Animes(anime_id) ON DELETE CASCADE,
    FOREIGN KEY (anime_series_id) REFERENCES AnimeSeries(anime_series_id) ON DELETE CASCADE,
    PRIMARY KEY (anime_id, anime_series_id)
);

INSERT INTO Animes(title, number_of_episode, status)
VALUES ('Госпожа Кагуя: в любви как на войне', 12, TRUE);

INSERT INTO AnimeSeries(anime_series_name)
VALUES ('Госпожа Кагуя'), ('Без серии');

INSERT INTO AnimeSeriesAnimes(anime_id, anime_series_id)
SELECT
	a.anime_id,
	s.anime_series_id
FROM Animes a JOIN AnimeSeries s ON a.title = 'Госпожа Кагуя: в любви как на войне' AND s.anime_series_name = 'Госпожа Кагуя';