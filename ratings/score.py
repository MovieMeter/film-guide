# Makes Calls to the IMDb and Rottentomatoes movie pages, and calculates the aggregate score for a movie.
# Modify values for each rating system here, to change the aggregate scoring.
# Function call, need to import this module and call the get_score() method by passing the URLs.

from ratings.imdb_rating import imdb_meta
from ratings.rotten_rating import rotten


def get_score(imdb_url, rotten_url):
    (imdb, meta) = imdb_meta(imdb_url)
    (rotten_meter, audience_score) = rotten(rotten_url)
    imdb_w = 5
    meta_w = 4
    rotten_w = 3
    audience_w = 3
    if meta > 0:
        total = imdb_w + meta_w + rotten_w + audience_w
    else:
        total = imdb_w + rotten_w + audience_w
    temp1 = imdb_w * imdb
    temp2 = meta_w * meta
    temp3 = rotten_w * rotten_meter
    temp4 = audience_w * audience_score

    # print(temp1, temp2, temp3, temp4)
    print('Breakdown : ')
    print('IMDb : ' + str(imdb) + ', Metascore : ' + str(meta) + ', RT : ' + str(rotten_meter) + ', Audience Poll : ' + str(audience_score))
    sc = (temp1+temp2+temp3+temp4)/total
    # print('Score : ' + str((temp1 + temp2 + temp3 + temp4)/10))
    return sc


