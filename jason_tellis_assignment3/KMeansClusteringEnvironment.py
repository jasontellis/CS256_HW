from KMeansClusteringAgent import KMeansClusteringAgent
from Trainer import Trainer

trainer = Trainer()
table = trainer.getLookUpTable()
clusters = KMeansClusteringAgent(table, 2).getClusters()

for (clusterIndex, cluster) in enumerate(clusters):

    classCounts = {}

    print ("************************************")
    print ("\nCluster#: " + str(clusterIndex + 1) + " with " + str(len(cluster.members)) + " members")
    for member in cluster.members:

        print("\n" + member.imageFileName)
        if classCounts.has_key(member.imageClass):
            classCounts[member.imageClass] += 1
        else:
            classCounts[member.imageClass] = 1

    summary = "Cluster with "
    for (imageClass, classCounts) in classCounts.iteritems():
        summary += str(classCounts) + " " + imageClass + " ,"
    print ("************************************")
    print summary
