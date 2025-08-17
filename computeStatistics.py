import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy

class Statistics:
    def __init__(self):
        self.initializer = True
    #-------------------------------Utility Functions-------------------------------#
    def computeIsotopeDistribution(self,nodesMap):
        isotopeCounts = {}
        for nodeId, isotopesMap in nodesMap.items():
            for isotopeId, numberOfParticles in isotopesMap.items():
                if isotopeId not in isotopeCounts:
                    isotopeCounts[isotopeId] = []
                isotopeCounts[isotopeId].append(numberOfParticles)
        # Plotting
        # Need to add cumsum to make it into a "random???" process 
        for isotopeId, particleCounts in isotopeCounts.items():
            particleCounts.plot()


    """######################### SECTION TO COMPUTE MODAL NODE PER LEVEL ###############################"""

    """These set of functions will let all nodes in a particular level to cast their vote on which 
    isotopes has the most particles. The isotope voted for by most nodes in a level is declared the 
    modal node per level of the isotopeTree."""
    def modalNodesPerLevel(self,root):
        """Helper ..."""
        currentLevel = 1
        currentNode = root
        modalLevelVotes = self.getVotes(root,currentLevel,{})

        return modalLevelVotes
    
    def getVotes(self,node,currentLevel,votingBooth):
        """Helper ..."""
        if node is None:
            return
        # In-order Traversal
        self.getVotes(node.left,currentLevel + 1, votingBooth)
        # Processing current node
        nodeIsotopesMap = node.countsIsotopes
        if currentLevel not in votingBooth:
            votingBooth[currentLevel] = {}
            self.addIsotopeIds(votingBooth[currentLevel],nodeIsotopesMap)
        # Casting current level's votes
        votingMachinePerLevel = votingBooth[currentLevel]
        #nodeIsotopesMap = node.countsIsotopes
        # Get the modal isotope in this current node
        modalIsotopePerNode = self.getMode(nodeIsotopesMap)
        """
        for isotope in nodeIsotopesMap.keys():
            if isotope == 'parentId' or isotope == 'myId':
                continue
            else:
                currentIsotopeVotes = nodeIsotopesMap[isotope]
                if isotope not in votingMachinePerLevel:
                    votingMachinePerLevel[isotope] = 0
                votingMachinePerLevel[isotope] += currentIsotopeVotes
        """
        votingMachinePerLevel[modalIsotopePerNode] += 1
        self.getVotes(node.right,currentLevel + 1,votingBooth)

        return votingBooth
    
    def addIsotopeIds(self,newVotingMachinePerLevel,nodeIsotopesMap):
        for isotope in nodeIsotopesMap.keys():
            if isotope == 'parentId' or isotope == 'myId':
                continue
            else:
                newVotingMachinePerLevel[isotope] = 0

    def announceResults(self,votingBooth):
        "Helper ..."
        for level, votingMachinePerLevel in votingBooth.items():
            maxVotes = float('-inf')
            print(f"The isotope node in level  {str(level)} is: " + str(self.getMode(votingMachinePerLevel)))

    def getMode(self,levelIsotopeVotesMap):
        """Helper ..."""
        maxVotes = float("-inf")
        modalIsotope = None
        for isotope, isotopeVotes in levelIsotopeVotesMap.items():
            if isotope == 'parentId' or isotope == 'myId':
                continue
            if isotopeVotes >= maxVotes:
                maxVotes = isotopeVotes
                modalIsotope = isotope
        return modalIsotope
    """######################### END OF SECTION TO COMPUTE MODAL NODE PER LEVEL ###############################"""


    """######################### SECTION TO COMPUTE MODAL NODE PER LEVEL ###############################"""
    def modalNodeAcrossTree(self,modalNodePerLevelMap):
        isotopeCounts = dict()
        modalNode = None
        for level, isotopeMap in modalNodePerLevelMap.items():
            modalNodeForLevel = self.getMode(isotopeMap)
            if modalNodeForLevel not in isotopeCounts:
                isotopeCounts[modalNodeForLevel] = 1
                if modalNode is None:
                    modalNode = modalNodeForLevel
                    continue
            isotopeCounts[modalNodeForLevel] += 1
            if isotopeCounts[modalNodeForLevel] >= isotopeCounts[modalNode]:
                modalNode = modalNodeForLevel
        return modalNode  


    """######################### SECTION TO COMPUTE INSTANTENEOUS ISOTOPE DISTRIBUTION NODE PER LEVEL ###############################"""
    def computeInstantaneousIsotopeDistributions(self,root):
        "Helper ..."
        current = root
        instantaneousIsotopeCounts = dict()
        self.addIsotopeIds(instantaneousIsotopeCounts,current.countsIsotopes)
        return self.getIsotopesInstantaneousCounts(current,instantaneousIsotopeCounts)

    def getIsotopesInstantaneousCounts(self,node,instantaneousMap):
        if node is None:
            return
        self.getIsotopesInstantaneousCounts(node.left,instantaneousMap)
        isotopesMap = node.countsIsotopes
        for isotope, counts in isotopesMap.items():
            if isotope == 'parentId' or isotope == 'myId':
                continue
            else:
                if instantaneousMap[isotope] == 0:
                    instantaneousMap[isotope] = list()
                instantaneousMap[isotope].append(counts)
        self.getIsotopesInstantaneousCounts(node.right,instantaneousMap)
        return instantaneousMap

    """######################### END OF SECTION TO COMPUTE INSTANTENEOUS ISOTOPE DISTRIBUTION NODE PER LEVEL ###############################"""


    """######################### SECTION TO PLOT RANDOM PROCESSES ###############################"""
    def randomProcessPlotter(self,instantaneousMap):
        array = []
        counter = 1
        for isotopeId, instantaneousCounts in instantaneousMap.items():
            listDistribution = [isotopeId] + instantaneousCounts
            plt.figure(counter)
            plt.plot(listDistribution[1:])
            array.append(listDistribution)
            counter += 1
        npArray = np.array(array)

        """
        df = pd.DataFrame(instantaneousMap,columns = list(instantaneousMap.keys()))
        df = df.T
        # dataToPlot = df[1:2]
        dataToPlot = df
        dataToPlot = dataToPlot.cumsum()
        # plt.figure(1)
        dataToPlot.plot()
        # plt.plot(dataToPlot)
        plt.show()
        """

    """######################### END OF SECTION TO PLOT RANDOM PROCESSES ###############################"""
    
    """######################### SECTION TO GET THE DISTRB. OF PARTICLES ALONG A BRANCH ###############################"""
    def meanLevelIsotopeCounts(self,instantaneousMap):
        pass

    def getParticleDistributionAlongPath(self,root,isotopeId):
        listParticlesPerPath = {}
        return self.getActualDistribution(root,listParticlesPerPath,isotopeId,[])
    
    def getActualDistribution(self,node,map,isotopeId,nodesList):
        if node.left is None and node.right is None:
            nodesList.append(node.countsIsotopes[isotopeId])
            completePathParticlesList = copy.deepcopy(nodesList)
            map[node.nodeId] = completePathParticlesList
            leafNodesCounts = nodesList.pop()
            return map
        nodesList.append(node.countsIsotopes[isotopeId])
        self.getActualDistribution(node.left,map,isotopeId,copy.deepcopy(nodesList))
        self.getActualDistribution(node.right,map,isotopeId,copy.deepcopy(nodesList))
        return map


    """######################### END OF SECTION TO GET THE DISTRB. OF PARTICLES ALONG A BRANCH ###############################"""


    """######################### SECTION TO GET THE PROBABILITIES OF ISOTOPES ACROSS ISOTOPE TREE ###############################"""
    def isotopeProbabilities(self,root,isotopeId):
        current = root
        listSubsetCounts = list()
        isotopeParticlesSubsetCounts = self.getSubsetCounts(current,listSubsetCounts,isotopeId)
        return self.calculateProbabilities(isotopeParticlesSubsetCounts)
    
    def getSubsetCounts(self,node,array,isotopeId):
        if node is None:
            return
        
        # Using pre-order traversal
        isotopeDistributions = node.countsIsotopes
        totalNumberOfParticles = 0

        currentSubsetData = []
        for currentIsotopeId, particleCount in isotopeDistributions.items():
            if currentIsotopeId == 'parentId' or currentIsotopeId == 'myId':
                continue
            if currentIsotopeId == isotopeId:
                currentSubsetData.append(particleCount)
            totalNumberOfParticles += particleCount
        currentSubsetData.append(totalNumberOfParticles)

        array.append(currentSubsetData)
        self.getSubsetCounts(node.left,array,isotopeId)
        self.getSubsetCounts(node.right,array,isotopeId)

        return array
    
    def calculateProbabilities(self,array):
        probabilities = list()
        for data in array:
            isotopeParticles, totalParticles = data
            ratio = (isotopeParticles / totalParticles) * 100
            probabilities.append(ratio)
        return probabilities
            
        

    """######################### END OF SECTION TO GET THE PROBABILITIES OF ISOTOPES ACROSS ISOTOPE TREE ###############################"""

    def mean(self,array):
        numberOfSubsets = len(array)
        total = sum(array)
        return (total / numberOfSubsets)
    
    def variance(self,array):
        mean = self.mean(array)
        numberOfSubsets = len(array)
        difference = 0
        for randomValue in array:
            difference += (randomValue - mean)**2
        return (difference / numberOfSubsets)
    
    def generateBernoulli(self,numOfRepeatedTrials,meanExpectation,epochs):
        return np.random.binomial(numOfRepeatedTrials,meanExpectation,epochs)

