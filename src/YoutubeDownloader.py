import os
import sys
import re
import time
from pathlib import Path
from pytube import YouTube
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import ThemedStyle
from threading import Thread, Lock

from LinkValidator import LinkValidator
from StreamDownloader import StreamDownloader

class YoutubeDownloaderApp:
    WINDOW_RESOLUTION = "650x350"
    WINDOW_TITLE = "Download Youtube Videos"
    root = None
    fontHeader = ("Times", "24")
    fontSimple = ("Times", "16")
    linkEntry = ""
    error = False
    errorLabel = None
    loading = False
    progressBar = None
    directoryLabel = None
    saveFileDirectory = f"{str(Path.home())}/Downloads"

    lock = Lock()
    downloadCompleted = False

    buttonStartDownloadMp4 = None
    buttonStartDownloadMp3 = None
    directoryButton = None

    COLOUR_RED = "#EE3D04"
    ORIGINAL_COLOUR = None

    infoErrorMessage = "Something went wrong! Make sure you are connected to the internet and that the Youtube link is valid."

    def __init__(self):
        self.initializeGUI()
        self.root.mainloop()

    def startVideoDownload(self, audioOnly):
        ytUrl = self.getYoutubeLink()
        if not LinkValidator.validateLink(self, ytUrl):
            self.setError("Url for Youtube Video is invalid")
            return

        ytUrl = LinkValidator.formatLink(ytUrl)
        self.modifyUIStateDisabled(True)
        self.setLoading(True)

        subjectOfDownload = "Video"
        if audioOnly:
            subjectOfDownload = "Audio"
        self.setMessage(f"Downloading {subjectOfDownload} ... (Please wait)")

        with self.lock:
            self.finished = False
        t = Thread(target=StreamDownloader.downloadYouTubeVideo, args=(self, audioOnly, ytUrl, self.saveFileDirectory))
        t.daemon = True
        self.root.after(2000, self.checkDownloadStatus)
        t.start()

    def checkDownloadStatus(self):
        with self.lock:
            if not self.finished:
                self.root.after(2000, self.checkDownloadStatus)
            else:
                return

    def setError(self, msg):
        self.ORIGINAL_COLOUR = self.linkEntry.cget("highlightbackground")
        self.linkEntry.config(highlightbackground=self.COLOUR_RED)
        self.setMessage(msg)
        self.errorLabel.config(fg=self.COLOUR_RED)
        self.error = True

    def clearError(self):
        self.linkEntry.config(highlightbackground=self.ORIGINAL_COLOUR)
        self.setMessage("")

    def setMessage(self, msg):
        self.errorLabel.config(fg="white")
        self.errorLabel.config(text=msg)

    def setLoading(self, b):
        if b:
            self.pb.place(x=185, y=145)
            self.pb.start()
        else:
            self.pb.stop()
            self.pb['value'] = 0
            self.pb.place_forget()
            self.setMessage("Sitting Idle...")

    def modifyUIStateDisabled(self, disabled):
        if disabled:
            self.buttonStartDownloadMp4['state'] = 'disabled'
            self.buttonStartDownloadMp3['state'] = 'disabled'
            self.directoryButton['state'] = 'disabled'
            self.linkEntry['state'] = DISABLED
        else:
            self.buttonStartDownloadMp4['state'] = 'normal'
            self.buttonStartDownloadMp3['state'] = 'normal'
            self.directoryButton['state'] = 'normal'
            self.linkEntry['state'] = NORMAL

    def getDirectoryLabel(self, actionName):
        return actionName + " " + self.saveFileDirectory + "/"

    def changeSaveDirectory(self):
        self.saveFileDirectory = filedialog.askdirectory()
        if self.saveFileDirectory:
            self.directoryLabel.config(text=self.getDirectoryLabel("Saving to"))


    def getYoutubeLink(self):
        return self.linkEntry.get("1.0", "end-0c")

    def centerWindowOnScreen(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        frameWidth = window.winfo_rootx() - window.winfo_x()
        windowHeight = width + 2 * frameWidth
        height = window.winfo_height()
        titlebar_height = window.winfo_rooty() - window.winfo_y()
        win_height = height + titlebar_height + frameWidth
        x = window.winfo_screenwidth() // 2 - windowHeight // 2
        y = window.winfo_screenheight() // 2 - win_height // 2
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        window.deiconify()

    def initializeGUI(self):
        root = tk.Tk()
        self.root = root
        root.withdraw()
        style = ThemedStyle(root)
        style.set_theme("plastik")
        root.tk_setPalette(background='#3c3f41', foreground='white',
                      activeBackground='#3c3f41', activeForeground="black")

        root.geometry(self.WINDOW_RESOLUTION)
        root.title(self.WINDOW_TITLE)
        # root.configure(bg = "#3c3f41")
        self.centerWindowOnScreen(root)
        root.resizable(width=False, height=False)
        mainTitle = tk.Label(text="Welcome to MNS's Youtube Downloader", font=self.fontHeader)
        mainTitle.pack(padx=10, pady=15)

        top = tk.Frame(root)
        bottom = tk.Frame(root)

        labelSelectFile = tk.Label(text="Paste Youtube Link: ", font=self.fontSimple)
        self.linkEntry = tk.Text(root, height=2, width=50, highlightbackground="white")
        self.buttonStartDownloadMp4 = tk.Button(root, text="Start Download to mp4",
                                             command=lambda: self.startVideoDownload(False), font=self.fontSimple, fg="black")
        self.buttonStartDownloadMp3 = tk.Button(root, text="Start Download to mp3",
                                             command=lambda: self.startVideoDownload(True), font=self.fontSimple, fg="black")
        self.errorLabel = tk.Label(root, text="", fg=self.COLOUR_RED, font=self.fontSimple)
        self.pb = ttk.Progressbar(root, orient='horizontal', mode='indeterminate', length=280)
        self.directoryLabel = tk.Label(root, text=self.getDirectoryLabel("Saving to"), font=self.fontSimple)
        self.directoryButton = tk.Button(root, text="Change Save Location", command=self.changeSaveDirectory, font=self.fontSimple, fg="black")

        labelSelectFile.pack(padx=15, pady=5, side=tk.TOP)
        self.linkEntry.pack(padx=15, pady=5, side=tk.TOP)
        self.errorLabel.pack(padx=15, pady=30, side=tk.TOP)
        top.pack(side=tk.TOP)
        bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.buttonStartDownloadMp4.pack(in_=top, side=tk.LEFT)
        self.buttonStartDownloadMp3.pack(in_=top, side=tk.LEFT)
        self.directoryLabel.pack(side=tk.BOTTOM, pady=0, padx=10)
        self.directoryButton.pack(side=tk.BOTTOM, pady=20, padx=10)
        self.pb.place(x=185, y=145)

        self.setMessage("Sitting Idle...")





