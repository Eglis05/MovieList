import requests
import sys
import os

from imdb import IMDb
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

class MovieList():
    def __init__(self):
        print("Creating a MovieList Instance")
        # create an instance of the IMDb class
        self.ia = IMDb()
        if os.environ.get("NETFLIX_USER") and os.environ.get("NETFLIX_PASS"):
            sys.path.append("../netflix-selenium")
            from netflix_selenium import NetflixLogin

            self.netflix = NetflixLogin()
            self.URL = "https://www.netflix.com/browse/my-list"

    def addnewmovie(self, movie, addition, movielist):
        f = open(movielist, "a")
        f.write(movie + " " + str(addition) + "\n")
        f.close()
        self.updatelist(movielist)

    def updatelines(self, lines, movielist):
        f = open(movielist, "w")
        for line in lines:
            f.write(line)
            if line[-1] != "\n":
                f.write("\n")
        f.close()

    def updatelist(self, movielist):
        f = open(movielist, "r")
        lines = f.readlines()
        lines.sort(reverse = True, key=lambda x: int(x.split()[1]))
        f.close()
        self.updatelines(lines, movielist)

    def addmovie(self, movie, movielist, addition):
        f = open(movielist, "r")
        lines = f.readlines()
        OK = 1
        for i in range(len(lines)):
            lines[i] = lines[i].split()
            if lines[i][0] != movie:
                lines[i] = " ".join(lines[i])
                continue
            lines[i] = lines[i][0] + " " + str(int(lines[i][1])+addition)
            OK = 0
        f.close()
        if OK:
            self.addnewmovie(movie, addition, movielist)
        else:
            self.updatelines(lines, movielist)
            self.updatelist(movielist)

    def add(self, movie, movielist, addition):
        movies = self.ia.search_movie(movie)

        # case when something was found
        if movies:
            ok = 1
            for movie_try in movies:
                movie_title  = movie_try['title']
                if movie_title.lower() == movie.lower():
                    movie = movie_title
                    ok = 0
                    break
            if ok:
                print("Not the same: " + movies[0]['title'] + " vs " + movie)
                movie = movies[0]['title']

        movie = movie.split()
        movie = "_".join(movie)
        self.addmovie(movie, movielist, addition)

    def readnotes(self, notes, movielist):
        f = open(notes, "r")
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].split()
            movie = lines[i][0:len(lines[i])-1]
            movie = " ".join(movie)
            try:
                self.add(movie, movielist, int(lines[i][len(lines[i])-1]))
            except ValueError:
                self.add(" ".join(lines[i]), movielist, 1)
        f.close()

    def scale(self, movielist):
        f = open(movielist, "r")
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].split()
            self.addmovie(lines[i][0], movielist, len(lines)-i-int(lines[i][1]))
        f.close()
            
    def notline(self, lines, j, movielist):
        f = open(movielist, "w")
        for i in range(len(lines)):
            if i != j:
                f.write(lines[i] + "\n")
        f.close()

    def removemovie(self, movie, movielist):
        f = open(movielist, "r")
        lines = f.readlines()
        j = -1
        for i in range(len(lines)):
            lines[i] = lines[i].split()
            if lines[i][0] != movie:
                if j != -1:
                    lines[i][1] = str(int(lines[i][1])+1)
                lines[i] = " ".join(lines[i])
                continue
            lines[i] = " ".join(lines[i])
            j = i
        if j != -1:
            self.notline(lines, j, movielist)
        f.close()

    def remove(self, movie, movielist):
        movie = movie.split()
        for i in range(len(movie)):
            movie[i] = movie[i].lower().capitalize()
        movie = "_".join(movie)
        self.removemovie(movie, movielist)

    def topmovies(self, x, movielist, ok = 1):
        f = open(movielist, "r")
        lines = f.readlines()
        movies = []
        for i in range(min(len(lines),x)):
            lines[i] = lines[i].split()
            lines[i][0] = lines[i][0].split('_')
            lines[i][0] = " ".join(lines[i][0])
            if ok:
                lines[i] = " ".join(lines[i])
                movies.append(lines[i])
            else:
                movies.append(lines[i][0])
        f.close()
        return movies

    def searchmovie(self, movie, movielist):
        f = open(movielist, "r")
        lines = f.readlines()
        movies = []
        for i in range(len(lines)):
            lines[i] = lines[i].split()
            OK = 0
            for j in range(len(lines[i][0])-len(movie)+1):
                if lines[i][0][j:len(movie)+j].lower() == movie:
                    OK = 1
            lines[i] = " ".join(lines[i])
            if OK:
                movies.append(lines[i])
        f.close()
        return movies

    def search(self, movie, movielist):
        movie = movie.split()
        for i in range(len(movie)):
            movie[i] = movie[i].lower()
        movie = "_".join(movie)
        return self.searchmovie(movie, movielist)
    
    def search_note_netflix(self, movielist, country):
        browser = webdriver.Chrome(ChromeDriverManager().install())
        browser.get(self.URL)
        self.netflix.login(browser)
        self.netflix.profileselect(browser)

        f = open(movielist, "r")
        lines = f.readlines()
        for line in lines:
            line = line.split()[0]
            movie = " ".join(line.split("_"))
            if self.netflix.check_available(browser, movie):
                print(movie)
            else:
                print(f"NOT IN NETFLIX: {movie}")