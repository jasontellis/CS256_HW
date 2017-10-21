from FlagLookUpTableBuilder import FlagLookUpTableBuilder
from HierarchicalClusteringAgent import HierarchicalClusteringAgent


class FlagClusteringEnvironment:
    """
    Passes table of flags to Hierarchical Clustering Agent for clustering
    """

    def __init__(self):
        flagVectorTable = FlagLookUpTableBuilder().getLookUpTable()
        hca = HierarchicalClusteringAgent(flagVectorTable)


fce = FlagClusteringEnvironment()
