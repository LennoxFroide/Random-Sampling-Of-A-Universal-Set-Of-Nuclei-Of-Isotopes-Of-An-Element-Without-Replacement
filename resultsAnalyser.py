import Sampling as smp
import traversals as travs
import graphVIsualizer as visualizer
import computeStatistics as stats
import matplotlib.pyplot as pt
sampler = smp.Sampling(1)
sampler.printHere()
tree = sampler.generateSampleTree(1000000,[0.60,0.30,0.10],0.38,True,100)
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
isotopeParticleCountsPerPath = getStatistics.getParticleDistributionAlongPath(tree.root,1)
counter = 1
getStatistics.randomProcessPlotter(instanteneousNodeCounts)
counter = 10
"""
for _, isotopeParticles in isotopeParticleCountsPerPath.items():
    # while counter < 3:
    pt.figure(counter)
    pt.plot(isotopeParticles)
    counter += 1
pt.show()
"""
# Plotting probabilities
isotopesProbabilities = list()
probabilities = getStatistics.isotopeProbabilities(tree.root,1)
probabilities2 = getStatistics.isotopeProbabilities(tree.root,2)
probabilities3 = getStatistics.isotopeProbabilities(tree.root,3)
isotopesProbabilities.append(probabilities)
isotopesProbabilities.append(probabilities2)
isotopesProbabilities.append(probabilities3)
counter = 40
for currentProbabilities in isotopesProbabilities:
    pt.figure(counter)
    pt.grid(True)
    counts, binEdges, _ = pt.hist(currentProbabilities)
    midpoints = (binEdges[:-1] + binEdges[1:]) / 2
    pt.plot(midpoints,counts,color='red')
    counter += 1
pt.show()
# getStatistics.randomProcessPlotter(instanteneousNodeCounts)
# sortedParentChild = dict(sorted(visualiser.parentChildMatcher.items(), key= lambda item: item[1][0]))

"""
print("\n")
print(sortedParentChild)
print("\n")
print(sortedParentChild.keys())
print("\n")
print(visualiser.nodeIDNodeMatcher)
"""

