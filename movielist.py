from urllib.request import urlopen
import requests
INF = 10000000

class MovieList():
    def __init__(self):
        print("Creating a MovieList Instance")

    def addnewmovie(self, movie, addition, movielist):
        f = open(movielist, "a")
        f.write(movie + " " + str(addition) + "\n")
        f.close()
        self.updatelist(movielist)

    def updatelines(self, lines, movielist):
        f = open(movielist, "w")
        for line in lines:
            f.write(line + "\n")
        f.close()
        self.updatelist(movielist)

    def updatelist(self, movielist):
        f = open(movielist, "r")
        lines = f.readlines()
        before = INF
        OK = 0
        for i in range(len(lines)):
            lines[i] = lines[i].split()
            if before < int(lines[i][1]): 
                lines[i] = lines[i][0] + " " + lines[i][1]
                lines[i-1], lines[i] = lines[i], lines[i-1]
                OK = 1
            else:
                before = int(lines[i][1])
                lines[i] = lines[i][0] + " " + lines[i][1]
        f.close()
        if OK:
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

    def add(self, movie, movielist, addition):
        movie = movie.split()
        for i in range(len(movie)):
            movie[i] = movie[i].lower().capitalize()
        movie2 = " ".join(movie)
        movie = "+".join(movie)
        webp = requests.get("https://www.imdb.com/find?q=" + movie).text

        startlist = "<table class=\"findList\">"
        lenlist = webp.find(startlist, 80000, len(webp)-1) + len(startlist)
        if lenlist == len(startlist) - 1:
            print("SOMETHING IS WRONG")
            return
        secondone = "<a href=\"/title/"
        lensecond = len(secondone)

        for i in range(lenlist,len(webp)):
            if webp[i:(i+lensecond)] == secondone:
                lensecond += i
                break
        endsymbol = '/'
        endnumber = lensecond
        for i in range(lensecond,len(webp)):
            if webp[i] == endsymbol:
                endnumber = i + 1
                break
        title = webp[lensecond:endnumber]
        webp = requests.get("https://www.imdb.com/title/" + title).text

        
        lastone = "<meta property='og:title' content=\""
        lenlastone = len(lastone)

        for i in range(len(webp)):
            if webp[i:(i+lenlastone)] == lastone:
                lenlastone += i
                break

        endsymbol = '('
        endsecond = lenlastone
        for i in range(lenlastone,len(webp)):
            if webp[i] == endsymbol:
                endsecond = i-1
                break
        
        quotes = "&quot;"

        x = webp.find(quotes, lenlastone, endsecond)
        if (x != -1):
            lenlastone = webp.find(quotes, x + len(quotes), endsecond) + len(quotes) + 1

        movie = webp[lenlastone:endsecond]
        if movie.lower() != movie2.lower():
            print("Not the same: " + movie2 + " vs " + movie)
        # else:
        #     print("The same: " + movie)

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
