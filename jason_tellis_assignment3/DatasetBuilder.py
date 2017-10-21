import urllib
import urllib2
from urlparse import urljoin

from bs4 import BeautifulSoup


class DatasetBuilder:
    """
    Used to automatically download flags
    """
    sourceURL = "http://www.sciencekids.co.nz/pictures/flags.html"
    baseURL = "http://www.sciencekids.co.nz/pictures/flags.html"

    @staticmethod
    def downloadImage(imagesURL=sourceURL, path=".flags/"):

        page = urllib2.urlopen(DatasetBuilder.sourceURL)
        bsParser = BeautifulSoup(page, 'html.parser')
        image = ""
        images = []
        imageTags = bsParser.find_all(name="td", attrs={"class": "style54"})
        for imageTag in imageTags:

            anchor = imageTag.div.p.a
            if imageTag.div.a is not None:
                image = imageTag.div.a.img
            if anchor is not None:
                imgURL = urljoin(DatasetBuilder.baseURL, image["src"])
                print imgURL
                imgName = anchor.string
                if imgName is None:
                    imgName = imageTag.div.p.a.img["alt"]
                if imgName is not None:
                    imgName = imgName.encode("ascii") + ".jpg"
                    print imgName + " downloaded"
                    urllib.urlretrieve(imgURL, "./flags/" + imgName)


DatasetBuilder.downloadImage()
