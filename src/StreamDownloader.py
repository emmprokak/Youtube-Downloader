from pytube import YouTube
from tkinter import messagebox
from FilenameParser import FilenameParser
import os

class StreamDownloader:
    def __init__(self):
        return

    @staticmethod
    def downloadYouTubeVideo(window, audioOnly, videourl, path):
        yt = YouTube(videourl)
        finalFileName = ""

        try:
            if audioOnly:
                soundStream = yt.streams.filter(only_audio=True).first()
                if not os.path.exists(path):
                    os.makedirs(path)
                outputFile = soundStream.download(path)
                base, ext = os.path.splitext(outputFile)
                finalFileName = base + '.mp3'
                os.rename(outputFile, finalFileName)
            else:
                videoStream = yt.streams.get_highest_resolution()
                if not os.path.exists(path):
                    os.makedirs(path)
                outputFile = videoStream.download(path)
                base, ext = os.path.splitext(outputFile)
                finalFileName = f"{base}.{ext}"
        except:
            messagebox.showerror("showerror", window.infoErrorMessage)
            window.setLoading(False)
            window.modifyUIStateDisabled(False)
            return

        window.setLoading(False)
        window.modifyUIStateDisabled(False)
        window.directoryLabel.config(text=window.getDirectoryLabel(f"Saved \"{FilenameParser.parseFileName(finalFileName)}\" to"))