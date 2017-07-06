

class Film:

    def __init__(self):
        self.name = None
        self.score = None
        self.imdb_link = None
        self.rotten_link = None
        self.year = None
        self.genre = []
        self.ratings = []

    def set_name(self, name):
        self.name = name

    def set_year(self, year):
        self.name = year

    def set_score(self, score):
        self.score = score

    def set_genre(self, genre):
        if genre not in self.genre:
            self.genre.append(genre)

    def set_imdb_ref(self, imdb):
        self.imdb_link = imdb

    def set_rotten_ref(self, rotten):
        self.rotten_link = rotten

    def set_details(self, name, year, score, genres):
        self.name = name
        self.year = year
        self.score = score
        for item in genres:
            if item not in self.genre:
                self.genre.append(item)

