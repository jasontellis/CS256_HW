import matplotlib.pyplot as plt
import numpy as np


class AccuracyPlotter:
    """
    The below code has been referenced from http://blog.bharatbhole.com/creating-boxplots-with-matplotlib/
    """

    @staticmethod
    def plot(kList=[], accuracyList=[]):
        #   Takes 2 lists containing k and corresponding prediction accuracy as input and plots graph


        # Create a figure instance
        fig = plt.figure(1, figsize=(9, 6))
        # Create an axes instance
        ax = fig.add_subplot(111)

        # Create the boxplot

        ## add patch_artist=True option to ax.boxplot()
        ## to get fill color
        bp = ax.boxplot(accuracyList, patch_artist=True)

        plt.axis([0, 20, 0, 100.0])
        plt.xlabel("No. of nearest neighbors (k)")
        plt.ylabel("Accuracy in %")
        plt.xticks(np.arange(1, 23, 2.0))
        plt.yticks(np.arange(0, 100.0, 5.0))
        plt.title('Accuracy % vs No. of Nearest Neighbors(k) for cross fold validation')
        plt.boxplot(accuracyList)
        ax.set_xticklabels(kList)

        ## change outline color, fill color and linewidth of the boxes
        for box in bp['boxes']:
            # change outline color
            box.set(color='#7570b3', linewidth=2)
            # change fill color
            box.set(facecolor='#1b9e77')

        ## change color and linewidth of the whiskers
        for whisker in bp['whiskers']:
            whisker.set(color='#7570b3', linewidth=2)

        ## change color and linewidth of the caps
        for cap in bp['caps']:
            cap.set(color='#7570b3', linewidth=2)

        ## change color and linewidth of the medians
        for median in bp['medians']:
            median.set(color='#b2df8a', linewidth=2)

        ## change the style of fliers and their fill
        for flier in bp['fliers']:
            flier.set(marker='o', color='#e7298a', alpha=0.5)

        plt.show()
