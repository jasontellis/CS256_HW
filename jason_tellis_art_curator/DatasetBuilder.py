import urllib
import urllib2
from urlparse import urljoin

from bs4 import BeautifulSoup


class DatasetBuilder:
    """
    Used to automatically download Picasso Images
    """
    sourceURL = "https://www.wikiart.org/en/pablo-picasso/all-works"
    baseURL = "https://www.wikiart.org/en/pablo-picasso/"

    @staticmethod
    def downloadImage(imagesURL=sourceURL, path="./picasso/"):

        page = urllib2.urlopen(DatasetBuilder.sourceURL)
        bsParser = BeautifulSoup(page, 'html.parser')
        image = ""
        images = []
        imageTags = bsParser.find_all(name="ul", attrs={"class": "title"})
        for imageTag in imageTags:

            image = imageTag.li.a

            if image is not None:
                imgURL = urljoin(DatasetBuilder.baseURL, image["href"])
                print imgURL
                imgName = image.string
                if imgName is not None:
                    imgName = imgName.encode("ascii") + ".jpg"
                    print imgName + " downloaded"
                    urllib.urlretrieve(imgURL, path + imgName)


DatasetBuilder.downloadImage()
