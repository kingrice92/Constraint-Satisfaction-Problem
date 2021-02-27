#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Fri Feb 26 11:52:59 2021
@author: kingrice
"""

class CSP():
    # Define a constraint satisfaction problem class using the textbook 
    # notation of X, D, and C.
    def __init__(self, vertices, edges, colors):
        # X is a set of variables. Here the variables are nodes from a graph.
        self.X = vertices
        # C is a set of  constraints that specify allowable combinations 
        # of values. Here the constraints are defined by edges connecting 
        # adjacent nodes.
        self.C = edges
        # v is the set of allowable values in each domain that can be 
        # assigned to variable X. Here the allowable values are all of the 
        # colors defined by the input but this will change for each domain 
        # as the algorithm attempts to solve the coloring problem.
        self.v = colors
        # D is a set of domains, one for each variable. Here they are the set
        # of colors that can be assigned to a node in the graph.
        self.getDomainSet()
        
    def getDomainSet(self):
        # Helper function to build out the set of domains for each variable.
        self.D = [0]*len(self.X)
        for iD in range(len(self.D)):
            self.D[iD] = list(range(1, self.v + 1))   
 
def backtrackingSearch(csp):
    # This is the top-level call to the backtracking algorithm.
    assignment = [0]*len(csp.X)
    if backtrack(assignment, csp):
        print("Solution Found.")
        if len(assignment) <= 20:
            for i in range(len(assignment)):
                print("Node = ", csp.X[i],', Color = ', assignment[i])       
        return True
    else:
        return False
    
def backtrack(assignment, csp):
    # This is the backtracking algorithm for constraint satisfaction problems. 
    # It is structured very similar to to the recursive depth-first search algorithm.
    
    # If all nodes have been assigned colors, the solution has been found.
    if 0 not in assignment:
        return True
    
    # This is the Select-Unassigned-Variable function. The method used here to
    # select new variables is the minimum-remaining-values (MRV) heauristic.
    var = MRV(assignment, csp)
    varIndex = csp.X.index(var)
    
    for val in csp.D[varIndex]:
        # Check if value is consistant with assignment.
        if isConsistent(var, assignment, val, csp):
            assignment[varIndex] = val
            # This is the Inference function. The method used here is the 
            # Maintaining Arc Consistency (MAC) algorithm. 
            cspRevisedD = MAC(var, assignment, csp)
            if cspRevisedD:
                if backtrack(assignment, cspRevisedD):    
                    return True
                assignment[varIndex] = 0           
    return False

def isConsistent(var, assignment, val, csp):
    # This is a function to check that the present value is consistent with assignment.
    for i in range(len(csp.C)):
        if csp.C[i][0] == var and assignment[csp.X.index(csp.C[i][1])] == val:
            return False
        elif csp.C[i][1] == var and assignment[csp.X.index(csp.C[i][0])] == val:
            return False
    return True

def MRV(assignment, csp):
    # This is the minimum-remaining-values (MRV) heuristic. This function 
    # chooses the variable with the fewest "legal " values as the next variable
    # in the search. By doing so, it picks the variable that is most likely to
    # cause a failure, avoiding pointless searches through other variables.
    
    # The maximum number of "legal" values possible for a variable is the 
    # original number of allowable values given by the input.
    maxAllowableVals = list(range(1, csp.v + 1))
    
    # After the first variable has been assigned a value, choose the next
    # variable to be the one with the smallest domain of allowable values.
    if assignment[0] != 0:
        for i in range(len(assignment)):
            if assignment[i] == 0:
                possibleNode = csp.X[i]
                possibleVals = csp.D[i]
                if len(possibleVals) < len(maxAllowableVals):
                    maxAllowableVals = possibleVals
                    var = possibleNode
    else:
        # If zero values have been assigned, use the first variable 
        # the starting point. 
        var = csp.X[0]
    return var    

def MAC(var, assignment, csp):
    # This is the Maintaining Arc Consistency (MAC) algorithm. This detects
    # inconsistencies using the arc-consistency (AC-3) algorithm to check the 
    # arcs (Xj, Xi) for unassigned variables Xj that are neighbors of Xi. This
    # is a advanced form of forward checking that helps the MRV heuristic 
    # operate even more efficiently.
    
    for i in range(len(csp.C)):
        if csp.C[i][0] == var:
            # Check for unassigned variables Xj that are neighbors of Xi.
            if assignment[csp.X.index(csp.C[i][1])] == 0:
                
                # Get the index of the current variable and the neighbor variable.
                nbrIndex = csp.X.index(csp.C[i][1])
                varIndex = csp.X.index(var)
                
                # If the most recent value assigned is in the domain of the 
                # neighbor variable, remove it.
                if assignment[varIndex] in csp.D[nbrIndex]:
                    csp.D[nbrIndex].remove(assignment[varIndex]) 
                
                # If all values have been removed from the neighbors domain,
                # throw a failure
                if not csp.D[nbrIndex]:
                    return False
        
        # This code works the same as described above, but since the edges in 
        # this problem are only defined once, both nodes in the edge constraint
        # need to be checked to see if they match var Xi
        elif csp.C[i][1] == var:
            if assignment[csp.X.index(csp.C[i][0])] == 0:
                nbrIndex = csp.X.index(csp.C[i][0])
                varIndex = csp.X.index(var)
                if assignment[varIndex] in csp.D[nbrIndex]:
                    csp.D[nbrIndex].remove(assignment[varIndex])
                if not csp.D[nbrIndex]:
                    return False      
    return csp

if __name__ == '__main__':
    
    # Example from problem statement
    #nodeList = [1,2,3,18,19]
    #edgeList = [[1,3],[2,18],[3,19],[2,19]]
    
    # Another, more complex example
    nodeList = [1,2,3,4,5,6,7,8,9,10,11,12]
    edgeList = [[1,2],[1,4],[1,5],[1,7],[1,10],[2,5],[2,6],[2,7],[3,6],[3,9], 
                [3,10],[4,5],[4,11],[5,6],[5,8],[5,9],[5,10],[7,8],[7,9],
                [8,9],[9,12],[11,12]]
    colors = 3
    
    csp = CSP(nodeList, edgeList, colors)
    backtrackingSearch(csp)