import numpy as np
import pandas as pd

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


    """######################### SECTION TO COMPUTE MODAL NODE FOR ENTIRE ISOTOPE TREE ###############################"""
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
    """######################### END OF SECTION TO COMPUTE MODAL NODE FOR ENTIRE ISOTOPE TREE ###############################"""

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

    
