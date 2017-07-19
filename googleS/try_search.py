from gsearch import search



movie = input('Enter name of movie : ')

imdb_link = search(movie + ' imdb')
print(imdb_link)

rotten_link = search(movie + ' rottentomatoes')
print(rotten_link)

