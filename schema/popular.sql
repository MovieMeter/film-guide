drop table if exists popular_now;

create table if not exists popular_now (
  id integer REFERENCES movie_table(id),
  name text not null,
  year text not null
);
