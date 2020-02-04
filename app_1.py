import tkinter as tk
import movielist


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.addmoviebutton = tk.Button(self, text = "Add Movie", command = self.addingmovie)
        self.addmoviebutton.pack(side="top")

        self.removemoviebutton = tk.Button(self, text = "Remove Movie", command = self.removemovie)
        self.removemoviebutton.pack(side="top")

        self.searchmoviebutton = tk.Button(self, text = "Search Movie", command = self.searchmovie)
        self.searchmoviebutton.pack(side="top")

        self.topmoviesbutton = tk.Button(self, text = "Top Movies", command = self.topmovies)
        self.topmoviesbutton.pack(side="top")

        self.scalebutton = tk.Button(self, text = "Scale", command = self.scale)
        self.scalebutton.pack(side = "top")

        self.readnotesbutton = tk.Button(self, text = "Read File", command = self.readnotes)
        self.readnotesbutton.pack(side = "top")

        self.writenotesbutton = tk.Button(self, text = "Write File", command = self.writenotes)
        self.writenotesbutton.pack(side = "top")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

    def scale(self):
        movielist.scale()
        root.destroy()

    def readnotesfunc(notes, master):
        movielist.readnotes(notes)
        master.destroy()

    def readnotes(self):
        root.destroy()
        master = tk.Tk()
        tk.Label(master, text="File Name").grid(row=0)
        e1 = tk.Entry(master)
        e1.insert(10, "notes.txt")
        e1.grid(row=0, column=1)
        tk.Button(master, text='Quit', command=master.quit).grid(
            row=3, column=0, sticky=tk.W, pady=4)
        tk.Button(master, text='Submit', command= lambda: Application.readnotesfunc(e1.get(), master)).grid          (row=3, column=1, sticky=tk.W, pady=4)

    def writenotesfunc(notes, master):
        movielist.writenotes(notes)
        master.destroy()

    def writenotes(self):
        root.destroy()
        master = tk.Tk()
        tk.Label(master, text="File Name").grid(row=0)
        e1 = tk.Entry(master)
        e1.insert(10, "notes.txt")
        e1.grid(row=0, column=1)
        tk.Button(master, text='Quit', command=master.quit).grid(
            row=3, column=0, sticky=tk.W, pady=4)
        tk.Button(master, text='Submit', command= lambda: Application.writenotesfunc(e1.get(), master)).grid          (row=3, column=1, sticky=tk.W, pady=4)
        
    def addmoviefunc(movie ,addition, master):
        movielist.add(movie, int(addition))
        master.destroy()

    def addingmovie(self):
        root.destroy()
        master = tk.Tk()
        tk.Label(master, text="Movie Name").grid(row=0)
        tk.Label(master, text="Points number").grid(row=1)

        e1 = tk.Entry(master)
        e2 = tk.Entry(master)
        e2.insert(10, "1")

        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)

        tk.Button(master, text='Quit', command=master.quit).grid(
            row=3, column=0, sticky=tk.W, pady=4)
        tk.Button(master, text='Submit', command= lambda: Application.addmoviefunc(e1.get(), e2.get(), master)).grid(row=3, column=1, sticky=tk.W, pady=4)

    def removemoviefunc(movie, master):
        movielist.remove(movie)
        master.destroy()

    def removemovie(self):
        root.destroy()
        master = tk.Tk()
        tk.Label(master, text="Movie Name").grid(row=0)

        e1 = tk.Entry(master)

        e1.grid(row=0, column=1)

        tk.Button(master, text='Quit', command=master.quit).grid(
            row=3, column=0, sticky=tk.W, pady=4)
        tk.Button(master, text='Submit', command= lambda: Application.removemoviefunc(e1.get(), master)).grid(row=3, column=1, sticky=tk.W, pady=4)

    def topmoviesfunc(x, master):
        movies = movielist.topmovies(int(x))
        master.destroy()

        master = tk.Tk()
        for i in range(len(movies)):
            tk.Label(master, text=str((i+1)) + ". " + movies[i]).grid(row=i)
        tk.Button(master, text='Quit', command=master.quit).grid(
            row=len(movies), column=0, sticky=tk.W, pady=4)

    def topmovies(self):
        root.destroy()
        master = tk.Tk()
        tk.Label(master, text="Number of Movies").grid(row=0)

        e1 = tk.Entry(master)

        e1.grid(row=0, column=1)

        tk.Button(master, text='Quit', command=master.quit).grid(
            row=3, column=0, sticky=tk.W, pady=4)
        tk.Button(master, text='Submit', command= lambda: Application.topmoviesfunc(e1.get(), master)).grid(row=3, column=1, sticky=tk.W, pady=4)

    def searchmoviefunc(movie, master):
        movies = movielist.search(movie)
        master.destroy()
        master = tk.Tk()
        if movies == None:
            tk.Label(master, text="No Movie Found").grid(row=0)
        else:
            if len(movies) == 1:
                tk.Label(master, text="Movie Name:").grid(row=0)
            else:
                tk.Label(master, text="Movie Names:").grid(row=0)
            for i in range(len(movies)):
                tk.Label(master, text= str(i+1) + ". " + movies[i]).grid(row=i+1)
            tk.Button(master, text='Quit', command=master.quit).grid(
                row=len(movies)+2, column=0, sticky=tk.W, pady=4)

    def searchmovie(self):
        root.destroy()
        master = tk.Tk()
        tk.Label(master, text="Movie Name").grid(row=0)

        e1 = tk.Entry(master)

        e1.grid(row=0, column=1)

        tk.Button(master, text='Quit', command=master.quit).grid(
            row=3, column=0, sticky=tk.W, pady=4)
        tk.Button(master, text='Submit', command= lambda: Application.searchmoviefunc(e1.get(), master)).grid(row=3, column=1, sticky=tk.W, pady=4)

root = tk.Tk()
app = Application(master=root)
app.mainloop()