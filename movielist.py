INF = 1000000
movielist = "movielist.txt"

def addnewmovie(movie, addition):
    f = open(movielist, "a")
    f.write(movie + " " + str(addition) + "\n")
    f.close()
    updatelist(movielist)

def updatelines(lines, wantedfile):
    f = open(wantedfile, "w")
    for line in lines:
        f.write(line + "\n")
    f.close()
    if wantedfile == movielist:
        updatelist(wantedfile)

def updatelist(wantedfile):
    f = open(wantedfile, "r")
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
        updatelines(lines, wantedfile)

def addmovie(movie, addition = 1):
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
        addnewmovie(movie, addition)
    else:
        updatelines(lines, movielist)

def add(movie, addition = 1):
    movie = movie.split()
    for i in range(len(movie)):
        movie[i] = movie[i].lower().capitalize()
    movie = "_".join(movie)
    addmovie(movie, addition)

def readnotes(notes):
    f = open(notes, "r")
    lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].split()
        movie = lines[i][0:len(lines[i])-1]
        movie = " ".join(movie)
        try:
            add(movie, int(lines[i][len(lines[i])-1]))
        except ValueError:
            add(" ".join(lines[i]), 1)
    f.close()

def writenotes(notes):
    f = open(movielist, "r")
    lines = f.readlines()
    f.close()
    lines = topmovies(len(lines), 0)
    updatelines(lines, notes)

def erase():
    f = open(movielist, "w")
    f.close()

def scale():
    f = open(movielist, "r")
    lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].split()
        addmovie(lines[i][0], len(lines)-i-int(lines[i][1]))
    f.close()
        
def notline(lines, j):
    f = open(movielist, "w")
    for i in range(len(lines)):
        if i != j:
            f.write(lines[i] + "\n")
    f.close()

def removemovie(movie):
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
        notline(lines, j)
    f.close()

def remove(movie):
    movie = movie.split()
    for i in range(len(movie)):
        movie[i] = movie[i].lower().capitalize()
    movie = "_".join(movie)
    removemovie(movie)

def topmovies(x, ok = 1):
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

def searchmovie(movie):
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

def search(movie):
    movie = movie.split()
    for i in range(len(movie)):
        movie[i] = movie[i].lower()
    movie = "_".join(movie)
    return searchmovie(movie)