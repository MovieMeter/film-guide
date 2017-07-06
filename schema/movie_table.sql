create table if not EXISTS movie_table (
  id integer PRIMARY KEY ,
  name text NOT NULL COLLATE NOCASE,
  year integer NOT NULL
);

create table IF NOT EXISTS rating_table (
  id integer REFERENCES movie_table(id),
  imdb integer,
  meta integer,
  rotten integer,
  audience integer,
  score integer
);

create table if NOT EXISTS genre_table (
  id integer REFERENCES movie_table(id),
  genre text COLLATE NOCASE,
  PRIMARY KEY(id, genre)
);

