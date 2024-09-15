DROP TABLE IF EXISTS Series;

CREATE TABLE IF NOT EXISTS Series(
	series_id BIGSERIAL PRIMARY KEY,
	title TEXT NOT NULL CHECK (title != ''),
	season INT,
	number_of_episode INT NOT NULL,
	duration_of_one_episode INT NOT NULL,
	status BOOL NOT NULL
);

INSERT INTO Series(title, number_of_episode, season, duration_of_one_episode, status)
VALUES ('Пацаны', 8, 1, 60, TRUE);