from math import sqrt


class DistanceMatrix:
    """

    """

    def __init__(self, coords):
        """

        """
        self.matrix = DistanceMatrix.cartesian_matrix(coords)


    def cartesian_matrix(coords):
        """

        :param coords:
        :return:
        """
        matrix = {}
        for i, (x1, y1) in enumerate(coords):
            for j, (x2, y2) in enumerate(coords):
                dx, dy = x1 - x2, y1 - y2
                dist = sqrt(dx * dx + dy * dy)
                matrix[i, j] = dist
        return matrix