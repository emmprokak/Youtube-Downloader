import re

class LinkValidator:
    def __init__(self):
        return

    @staticmethod
    def formatLink(link):
        return link.strip()

    @staticmethod
    def validateLink(window, link):
        if not link:
            return False

        window.clearError()
        return bool(re.search("https://youtu.be", link)) or bool(re.search("https://www.youtube.com", link))