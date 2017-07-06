create table IF NOT EXISTS rating_table (
  id integer REFERENCES movie_table(id)

)