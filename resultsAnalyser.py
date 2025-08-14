import Sampling as smp
import traversals as travs
import graphVIsualizer as visualizer
import computeStatistics as stats
sampler = smp.Sampling(1)
sampler.printHere()
tree = sampler.generateSampleTree(10000,[0.35,0.35,0.30],0.38,True,5)
# print(tree.root.right.parentLevel)
print(sampler.nodeIds)
print(tree.root.right.countsIsotopes)
print(tree.root.right.parentId)
print(tree.root.left.parentId)
listOfNodes = list()
traverse = travs.TraverseSamplingTree()
traverse.inorderTraversal(tree.root,listOfNodes)
print(len(listOfNodes))
traverse.iterateNodesList(listOfNodes)
visualiser = visualizer.GraphVisualizer()
visualiser.preprocessTree(tree.root)
parentList = visualiser.getListOfParentNodes()
# visualiser.buildNodeIdDigraph(parentList)
visualiser.buildIsotopeDistributionDigraph(parentList)
getStatistics = stats.Statistics()
votingBooth = getStatistics.modalNodesPerLevel(tree.root)
getStatistics.announceResults(votingBooth)
print(getStatistics.modalNodeAcrossTree(votingBooth))
instanteneousNodeCounts = getStatistics.computeInstantaneousIsotopeDistributions(tree.root)
getStatistics.randomProcessPlotter(instanteneousNodeCounts)
# sortedParentChild = dict(sorted(visualiser.parentChildMatcher.items(), key= lambda item: item[1][0]))
"""
print("\n")
print(sortedParentChild)
print("\n")
print(sortedParentChild.keys())
print("\n")
print(visualiser.nodeIDNodeMatcher)
"""

