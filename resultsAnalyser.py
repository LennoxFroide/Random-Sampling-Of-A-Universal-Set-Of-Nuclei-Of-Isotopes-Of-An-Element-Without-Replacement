import Sampling as smp
import traversals as travs
import graphVIsualizer as visualizer
import computeStatistics as stats
import matplotlib.pyplot as pt
import numpy as np
sampler = smp.Sampling(1)
sampler.printHere()
tree = sampler.generateSampleTree(1000000,[0.50,0.40,0.10],0.38,True,50)
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

""" (1.) SECTION PLOTTING THE ISOTOPE PARTITION IDS DIGRAPH"""
# visualiser.buildNodeIdDigraph(parentList)

"""(2.) SECTION PLOTTING THE ISOTOPE DISTRIBUTION DIGRAPH"""
visualiser.buildIsotopeDistributionDigraph(parentList)

getStatistics = stats.Statistics()
votingBooth = getStatistics.modalNodesPerLevel(tree.root)
getStatistics.announceResults(votingBooth)
print(getStatistics.modalNodeAcrossTree(votingBooth))
instanteneousNodeCounts = getStatistics.computeInstantaneousIsotopeDistributions(tree.root)
isotopePerPathId = 1
isotopeParticleCountsPerPath = getStatistics.getParticleDistributionAlongPath(tree.root,isotopePerPathId)
counter = 1

"""(3.) SECTION PLOTTING THE REALIZATIONS OF ISOTOPE PARTICLE COUNTS FOR EACH ISOTOPE(RANDOM WALK)"""
getStatistics.randomProcessPlotter(instanteneousNodeCounts)
counter = 10

"""(4.) SECTION PLOTTING THE PARTICLE COUNTS FOR ISOTOPE 1 ALONG A SINGLE PATH FOR ALL ISOTOPE TREE PATHS."""
# TODO: We need the plots for the other 2 isotopes as well along same paths to use for comparison
pathNumber = 1
for _, isotopeParticles in isotopeParticleCountsPerPath.items():
    # while counter < 3:
    pt.figure(counter)
    pt.title(f"Number of Particles of Isotope {isotopePerPathId} Along Path {pathNumber} of the Isotope Tree")
    pt.xlabel("Partition of Universal Set")
    pt.ylabel("Number of Isotope Particles")
    pt.plot(isotopeParticles)
    counter += 1
    pathNumber += 1
pt.show()

"""(4.) SECTION PLOTTING THE PARTICLE COUNTS FOR ISOTOPE 2 ALONG A SINGLE PATH FOR ALL ISOTOPE TREE PATHS."""
isotopePerPathId = 2
isotopeParticleCountsPerPath = getStatistics.getParticleDistributionAlongPath(tree.root,isotopePerPathId)
counter = 15
pathNumber = 1
for _, isotopeParticles in isotopeParticleCountsPerPath.items():
    # while counter < 3:
    pt.figure(counter)
    pt.title(f"Number of Particles of Isotope {isotopePerPathId} Along Path {pathNumber} of the Isotope Tree")
    pt.xlabel("Partition of Universal Set")
    pt.ylabel("Number of Isotope Particles")
    pt.plot(isotopeParticles)
    counter += 1
    pathNumber += 1
pt.show()


"""(4.) SECTION PLOTTING THE PARTICLE COUNTS FOR ISOTOPE 3 ALONG A SINGLE PATH FOR ALL ISOTOPE TREE PATHS."""
isotopePerPathId = 3
isotopeParticleCountsPerPath = getStatistics.getParticleDistributionAlongPath(tree.root,isotopePerPathId)
counter = 20
pathNumber = 1
for _, isotopeParticles in isotopeParticleCountsPerPath.items():
    # while counter < 3:
    pt.figure(counter)
    pt.title(f"Number of Particles of Isotope {isotopePerPathId} Along Path {pathNumber} of the Isotope Tree")
    pt.xlabel("Partition of Universal Set")
    pt.ylabel("Number of Isotope Particles")
    pt.plot(isotopeParticles)
    counter += 1
    pathNumber += 1
pt.show()
# Plotting probabilities
isotopesProbabilities = dict()
"""
probabilities = getStatistics.isotopeProbabilities(tree.root,1)
probabilities2 = getStatistics.isotopeProbabilities(tree.root,2)
probabilities3 = getStatistics.isotopeProbabilities(tree.root,3)
isotopesProbabilities.append(probabilities)
isotopesProbabilities.append(probabilities2)
isotopesProbabilities.append(probabilities3)
"""

"""(5.) SECTION PLOTTING THE PROBABILITES FOR EACH ISOTOPE ACROSS ALL PARTITIONS (MODAL PROBABILITIES)."""
for isotope, _ in instanteneousNodeCounts.items():
    currentProbability = getStatistics.isotopeProbabilities(tree.root,isotope)
    isotopesProbabilities[isotope] = currentProbability

counter = 40
for isotope, currentProbabilities in isotopesProbabilities.items():
    pt.figure(counter)
    pt.grid(True)
    pt.title(f"Probability of Drawing Isotope {isotope}'s Particle Across Sampling Process")
    pt.xlabel(f"Probability of Drawing Isotope {isotope}'s Particles (%)")
    pt.ylabel("Number of Partitions with the Probability")
    counts, binEdges, _ = pt.hist(currentProbabilities)
    midpoints = (binEdges[:-1] + binEdges[1:]) / 2
    pt.plot(midpoints,counts,color='red')
    counter += 1
pt.show()


# Computing mean and variance
"""(6.) SECTION CALCULATING THE MEAN AND VARIANCE OF PARTICLE COUNTS FOR EACH ISOTOPE."""
means = dict()
variances = dict()
for isotopeId, instataneousCounts in instanteneousNodeCounts.items():
    currentExpectation = getStatistics.mean(instataneousCounts)
    currentVariance = getStatistics.variance(instataneousCounts)
    means[isotopeId] = currentExpectation
    variances[isotopeId] = currentVariance
print("The mean particles counts for each isotope:")
print(means)
print("\n")
print("The variance of particle counts for each isotope:")
print(variances)
print("\n")
# Computing mean probabilities
"""(7.) SECTION CALCULATING THE MEAN PROBABILITY FOR EACH ISOTOPE"""
meanProbabilities = dict()
for isotope, currentProbabilities in isotopesProbabilities.items():
    currentMeanProbability = getStatistics.mean(currentProbabilities)
    meanProbabilities[isotope]= currentMeanProbability
print("The mean probabilities for each isotope across sampling process:")
print(meanProbabilities)
"""(8.) SECTION GENERATING AND PLOTTING BERNOULLI RANDOM PROCESSES TO COMPARE WITH OURS"""
# Generating a Bernoulli Random Process for cross-validation
realizations = dict()
for isotope, meanProbability in meanProbabilities.items():
    currentRealization = np.random.binomial(len(instanteneousNodeCounts[isotope]),(meanProbability/100),len(isotopesProbabilities[isotope]))
    # currentRealization.append(isotope)
    currentRealization = np.append(currentRealization,isotope,axis=None)
    realizations[isotope] = currentRealization
# Plotting the generated Bernoulli random processes
counter = 100
for isotope, bernoulliValues in realizations.items():
    pt.figure(counter)
    pt.title(f"Bernoulli Random Process Generated Using the Mean Probability of Isotope {bernoulliValues[-1]}")
    pt.xlabel("Instance of Observation")
    pt.ylabel("Value of Bernoulli Random Process")
    pt.plot(bernoulliValues[:-1])
    counter += 1

"""SECTION TO COMPUTE THE VARIANCE OF THE BERNOULLI PROCESS"""
bernoulliVariances = dict()
for isotope, bernoulliValues in realizations.items():
    currentVariance = getStatistics.variance(bernoulliValues[:-1])
    bernoulliVariances[isotope] = currentVariance
    
print("The variances of the Bernoulli random processes are:")
print(bernoulliVariances)


