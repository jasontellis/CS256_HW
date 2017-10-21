class LookUpTableRow:
    """
    A row of the LookUpTable
    """

    def __init__(self, imageFileName="", imageVector=[], imageClass=""):
        self.imageFileName = imageFileName
        self.imageVector = imageVector  # A normalized histogram containing counts of each of the possible 255 values each of R, G, and B
        self.imageClass = imageClass

    def __str__(self):
        return "{ \n\timageVector: " + repr(self.imageVector) + "\n\timageClass: " + self.imageClass + "\n}"
