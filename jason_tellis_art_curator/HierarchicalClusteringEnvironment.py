"""
Clustering Environment for Headshots and Landscapes
"""
from HierarchicalClusteringAgent import HierarchicalClusteringAgent
from Trainer import Trainer

trainer = Trainer()
table = trainer.getLookUpTable()
agent = HierarchicalClusteringAgent(table)
