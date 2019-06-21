# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import random

import util
from game import Agent, Directions  # noqa
from util import manhattanDistance  # noqa


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        currFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPoints = successorGameState.getScore()
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()

        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"

        #check if the pacman in the ghost location
        i = 0
        while i < len(newGhostStates):
            ghostPos = newGhostStates[i].getPosition()
            if (manhattanDistance(newPos,ghostPos)<=2):
                return -99999
            i+=1

        # calculating distance bettween the pacman postion to food
        foodDistance = 0
        foods = newFood.asList()
        i = 0
        while (i < len(foods)):
            currDist = manhattanDistance(newPos,foods[i])
            foodDistance += float(1)/float(currDist)
            i+=1
        return newPoints+foodDistance

 


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn="scoreEvaluationFunction", depth="2"):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        maxMove = "" 
        maxValue = -88888
        index = 0
        directions = gameState.getLegalActions()
        while (index < len(directions)):
          nextState = gameState.generateSuccessor(0,directions[index])
          index+=1
          currValue = self.minMax(1, 0, nextState)
          if(currValue>=maxValue):
            maxValue = currValue
            maxMove = directions[index-1]
        return maxMove

    def minMax(self,index, depth, gameState):
      '''(self, int,int,gameState)-> int
        Return the current best action and move score'''
        # terminal situation: reach end node or depth bound
      #res = self.evaluationFunction(gameState)
        #currPots = self.evaluationFunction(gameState)
      if (self.depth==depth):
       	return self.evaluationFunction(gameState)
      elif(gameState.isWin()):
        return self.evaluationFunction(gameState)
      elif (gameState.isLose()):
        return self.evaluationFunction(gameState)
        # find all possible node of curr agent
      moves = gameState.getLegalActions(index)
      values = []
        
      for move in moves:
        nextState = gameState.generateSuccessor(index, move)
          # pacman
        if(index==0):
          points = self.minMax(index+1, depth, nextState)
          # last ghost
        elif (index +1 == gameState.getNumAgents()):
          points = self.minMax(0, depth+1,nextState)
          # middld layer ghost
        else:
          points = self.minMax(index+1, depth, nextState)
        values.append(points)
      res = 0
      if (index==0):
       	res = max(values)
      else:
       	res = min(values)
      return res


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        alpha = -999999
        beta = 999999
        moves = gameState.getLegalActions()
        res = None 

        for move in moves:
          nextState = gameState.generateSuccessor(0,move)
          currValue = self.abPruning(alpha,beta,0,1, nextState)
          if (currValue > alpha):
            alpha = currValue
            res = move
        return res

    def abPruning(self,alpha, beta, depth, player, gameState):
        #currPots = self.evaluationFunction(gameState)
        #print( 'sd' + str(self.depth)+'\n')
        #print('depth'+ str(depth) +'\n')
        if (self.depth==depth):
          	return self.evaluationFunction(gameState)
        elif(gameState.isWin()):
          	return self.evaluationFunction(gameState)
        elif (gameState.isLose()):
          	return self.evaluationFunction(gameState)
        # find all possible node of curr agent
        moves = gameState.getLegalActions(player)
        if (player==0):
          	for move in moves:
          		nextState = gameState.generateSuccessor(player,move)
          		alpha = max(alpha,self.abPruning(alpha,beta,depth,player+1,nextState))
          		if (alpha>=beta):
          			break
          	return alpha
        else:
          for move in moves:
            nextState = gameState.generateSuccessor(player,move)
            if (player+1==gameState.getNumAgents()):
              beta = min(beta,self.abPruning(alpha,beta,depth+1,0,nextState))
            else:
              beta = min(beta,self.abPruning(alpha,beta,depth,player+1,nextState))
            if (beta<=alpha):
              break
          return beta


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        moves = gameState.getLegalActions()
        res = None
        largest = -999999 
        for move in moves:
          nextState = gameState.generateSuccessor(0,move)
          currValue = self.expectMax(1,0,nextState)[0]
          if (currValue > largest):
            largest = currValue
            res = move
        return res

    def expectMax(self,player,depth,gameState):
        #currPots = self.evaluationFunction(gameState)
        if (self.depth==depth):
          return (self.evaluationFunction(gameState),None)
        elif(gameState.isWin()):
          return (self.evaluationFunction(gameState),None)
        elif (gameState.isLose()):
          return (self.evaluationFunction(gameState), None)

        moves = gameState.getLegalActions(player)
        value = -99999
        p = float(1)/float(len(moves))
        if (player>0):
          value = 0
        best_move = None
        if (player==0):
          localMax = -999
          best = None
          for move in moves:
            curr = self.expectMax(player+1,depth,gameState.generateSuccessor(player, move))
            if (curr[0]>value):
              value = curr[0]
          return (value,best_move)
        else:
          for move in moves:
            nextState = gameState.generateSuccessor(player,move)
            if (player+1 == gameState.getNumAgents()):
              curr = self.expectMax(0, depth+1,nextState)
            else:
              curr = self.expectMax(player+1, depth,nextState)
            value = value+ curr[0]*1.0/float(len(moves))
          return (value, None)          


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: this function search for the cloest food, closet capsules, run away from gohst
      if ghost is in scard time, pacman move toward ghost
    """
    "*** YOUR CODE HERE ***"
    currScore = currentGameState.getScore()
    newPos = currentGameState.getPacmanPosition()
    currFoods = currentGameState.getFood()

    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    pointsFood = 0
    # find the cloest food 
    nextFood = 9999
    for food in currFoods.asList():
      curr = manhattanDistance(newPos,food)
      if (curr <nextFood):
        nextFood = curr
    # if food is next assign large value since this state is good, else add inverse of nextFood 
    if (nextFood !=0):
      pointsFood = 1
    else:  
      pointsFood= float(1)/float(nextFood)

    # search through ghost list, if ghost is scared assign large value, else add the inverse of closest ghost
    ghostPositions = currentGameState.getGhostPositions()
    pointsGhost = 0  
    i = 0
    while (i<len(ghostPositionsos)):
      currDist = manhattanDistance(newPos,ghostPositions[i])
      currT = newScaredTimes[i]
      if (currDist>=1):
        #ghost normal, move away from it
        if (currT == 0 or currDist<=currT):
          pointsGhost+=float(2)/float(currDist)
        else:
          # ghost is scared, move toward it
          pointsGhost -= float(3)/float(currDist)
    res = currScore+pointsFood-pointsGhost
    return res



# Abbreviation
better = betterEvaluationFunction
