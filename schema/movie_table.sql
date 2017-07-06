create table if not EXISTS movie_table (
  id integer PRIMARY KEY ,
  name text NOT NULL COLLATE NOCASE,
  year integer NOT NULL ,
  score real NOT NULL
);

create table IF NOT EXISTS rating_table (
  id integer REFERENCES movie_table(id),
  imdb integer,
  meta integer,
  rotten integer,
  audience integer
);

create table if NOT EXISTS genre_table (
  id integer REFERENCES movie_table(id),
  genre1 text COLLATE NOCASE,
  genre2 text COLLATE NOCASE,
  genre3 text COLLATE NOCASE
);

