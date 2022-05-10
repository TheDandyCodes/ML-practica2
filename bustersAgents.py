from __future__ import print_function
# bustersAgents.py
# ----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from builtins import range
from builtins import object
import util
from game import Agent
from game import Directions
from keyboardAgents import KeyboardAgent
import inference
import busters
import os
from game import Configuration

prevPacmanPosition = (0,0)
'''This score is a global variable that is changed in ChooseAction method so that it will save the next value of Score considering wether pac-man is
eating a ghost'''
nextScore = 0 
instance_line = []

class NullGraphics(object):
    "Placeholder for graphics"
    def initialize(self, state, isBlue = False):
        pass
    def update(self, state):
        pass
    def pause(self):
        pass
    def draw(self, state):
        pass
    def updateDistributions(self, dist):
        pass
    def finish(self):
        pass

class KeyboardInference(inference.InferenceModule):
    """
    Basic inference module for use with the keyboard.
    """
    def initializeUniformly(self, gameState):
        "Begin with a uniform distribution over ghost positions."
        self.beliefs = util.Counter()
        for p in self.legalPositions: self.beliefs[p] = 1.0
        self.beliefs.normalize()

    def observe(self, observation, gameState):
        noisyDistance = observation
        emissionModel = busters.getObservationDistribution(noisyDistance)
        pacmanPosition = gameState.getPacmanPosition()
        allPossible = util.Counter()
        for p in self.legalPositions:
            trueDistance = util.manhattanDistance(p, pacmanPosition)
            if emissionModel[trueDistance] > 0:
                allPossible[p] = 1.0
        allPossible.normalize()
        self.beliefs = allPossible

    def elapseTime(self, gameState):
        pass

    def getBeliefDistribution(self):
        return self.beliefs


class BustersAgent(object):
    "An agent that tracks and displays its beliefs about ghost positions."
    def __init__( self, index = 0, inference = "ExactInference", ghostAgents = None, observeEnable = True, elapseTimeEnable = True):
        inferenceType = util.lookup(inference, globals())
        self.inferenceModules = [inferenceType(a) for a in ghostAgents]
        self.observeEnable = observeEnable
        self.elapseTimeEnable = elapseTimeEnable
        '''self.weka = Weka()
        self.weka.start_jvm()'''

    def registerInitialState(self, gameState):
        "Initializes beliefs and inference modules"
        import __main__
        self.display = __main__._display
        for inference in self.inferenceModules:
            inference.initialize(gameState)
        self.ghostBeliefs = [inf.getBeliefDistribution() for inf in self.inferenceModules]
        self.firstMove = True

    def observationFunction(self, gameState):
        "Removes the ghost states from the gameState"
        agents = gameState.data.agentStates
        gameState.data.agentStates = [agents[0]] + [None for i in range(1, len(agents))]
        return gameState

    def getAction(self, gameState):
        "Updates beliefs, then chooses an action based on updated beliefs."
        #for index, inf in enumerate(self.inferenceModules):
        #    if not self.firstMove and self.elapseTimeEnable:
        #        inf.elapseTime(gameState)
        #    self.firstMove = False
        #    if self.observeEnable:
        #        inf.observeState(gameState)
        #    self.ghostBeliefs[index] = inf.getBeliefDistribution()
        #self.display.updateDistributions(self.ghostBeliefs)
        return self.chooseAction(gameState)

    def chooseAction(self, gameState):
        "By default, a BustersAgent just stops.  This should be overridden."
        return Directions.STOP
    
    def getNextScore(self, gameState):
        '''calculates next Score by using gameState data. nextScore variable is Global'''
        global nextScore

    def getSuccesor(self, gameState):
        print("Succesor: ")  #gameState.generateSuccesor(0, action --> move = DIRECTION.West?)

    def printLineData(self, gameState, nextState):
        new_line = []

        #Current State Data
        pacmanXPosition = gameState.getPacmanPosition()[0]
        pacmanYPosition = gameState.getPacmanPosition()[1]
        pacmanDirection = gameState.data.agentStates[0].getDirection()
        livingGhosts = gameState.getLivingGhosts()[1:]
        instance_line = [pacmanDirection, pacmanXPosition, pacmanYPosition]+livingGhosts
        ghostPositions = gameState.getGhostPositions()
        ghostDistances = gameState.data.ghostDistances[:] #Copy the list, there'll be changes, so change the assigment
        currentScore = gameState.getScore()
        
        for i in range(len(ghostDistances)):
            if ghostDistances[i] == None: ghostDistances[i] = 0

        for x in ghostPositions:
            for i in x:
                instance_line.append(i)
        instance_line.extend(ghostDistances)
        instance_line.append(currentScore)
        #Taken Action (Class)
        takenAction = BustersAgent.getAction(self, gameState)

        #Next State Data
        pacmanNextXPosition = pacmanXPosition
        pacmanNextYPosition = pacmanYPosition
        if takenAction == 'North': pacmanNextYPosition = pacmanYPosition+1
        elif takenAction == 'South': pacmanNextYPosition = pacmanYPosition-1
        elif takenAction == 'Right': pacmanNextXPosition = pacmanXPosition+1
        elif takenAction == 'Left': pacmanNextXPosition = pacmanXPosition-1
        nextScore = nextState.getScore()
        nextDataLine=[pacmanNextXPosition, pacmanNextYPosition, nextScore]

        instance_line.extend(nextDataLine)

        instance_line.append(takenAction)
        new_line.append(instance_line)
            
        print(new_line)

    def getInstanceToPredict(self, gameState):
        #Current State Data
        pacmanXPosition = gameState.getPacmanPosition()[0]
        pacmanYPosition = gameState.getPacmanPosition()[1]
        pacmanDirection = gameState.data.agentStates[0].getDirection()
        instance_line = [pacmanDirection, pacmanXPosition, pacmanYPosition]
        ghostPositions = gameState.getGhostPositions()
        ghostDistances = gameState.data.ghostDistances[:] #Copy the list, there'll be changes, so change the assigment
        
        for i in range(len(ghostDistances)):
            if ghostDistances[i] == None: ghostDistances[i] = 0

        for x in ghostPositions:
            for i in x:
                instance_line.append(i)
        instance_line.extend(ghostDistances)

        #print(instance_line)

        return instance_line


    def printFilterData2(self, gameState):
        new_line = []
        livingGhosts = gameState.getLivingGhosts()[1:]
        new_info = livingGhosts[:]
        ghostDistances = gameState.data.ghostDistances[:] #Copy the list, there'll be changes, so change the assigment
        
        for i in range(len(ghostDistances)):
            if ghostDistances[i] == None: ghostDistances[i] = 0

        takenAction = BustersAgent.getAction(self, gameState)
        
        new_info = new_info+ghostDistances
        new_info.append(takenAction)
        new_line.append(new_info)
        
        print("filter 2: ", new_info)

class BustersKeyboardAgent(BustersAgent, KeyboardAgent):
    "An agent controlled by the keyboard that displays beliefs about ghost positions."

    def __init__(self, index = 0, inference = "KeyboardInference", ghostAgents = None):
        KeyboardAgent.__init__(self, index)
        BustersAgent.__init__(self, index, inference, ghostAgents)

    def getAction(self, gameState):
        return BustersAgent.getAction(self, gameState)

    def chooseAction(self, gameState):
        return KeyboardAgent.getAction(self, gameState)


from distanceCalculator import Distancer
from game import Actions
from game import Directions
import random, sys

'''Random PacMan Agent'''
class RandomPAgent(BustersAgent):

    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        
    ''' Example of counting something'''
    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if(height == True):
                    food = food + 1
        return food
    
    ''' Print the layout'''  
    def printGrid(self, gameState):
        table = ""
        ##print(gameState.data.layout) ## Print by terminal
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table
        
    def chooseAction(self, gameState):
        move = Directions.STOP
        legal = gameState.getLegalActions(0) ##Legal position from the pacman
        move_random = random.randint(0, 3)
        if   ( move_random == 0 ) and Directions.WEST in legal:  move = Directions.WEST
        if   ( move_random == 1 ) and Directions.EAST in legal: move = Directions.EAST
        if   ( move_random == 2 ) and Directions.NORTH in legal:   move = Directions.NORTH
        if   ( move_random == 3 ) and Directions.SOUTH in legal: move = Directions.SOUTH
        return move
        
class GreedyBustersAgent(BustersAgent):
    "An agent that charges the closest ghost."

    def registerInitialState(self, gameState):
        "Pre-computes the distance between every two points."
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)

    def chooseAction(self, gameState):
        """
        First computes the most likely position of each ghost that has
        not yet been captured, then chooses an action that brings
        Pacman closer to the closest ghost (according to mazeDistance!).

        To find the mazeDistance between any two positions, use:
          self.distancer.getDistance(pos1, pos2)

        To find the successor position of a position after an action:
          successorPosition = Actions.getSuccessor(position, action)

        livingGhostPositionDistributions, defined below, is a list of
        util.Counter objects equal to the position belief
        distributions for each of the ghosts that are still alive.  It
        is defined based on (these are implementation details about
        which you need not be concerned):

          1) gameState.getLivingGhosts(), a list of booleans, one for each
             agent, indicating whether or not the agent is alive.  Note
             that pacman is always agent 0, so the ghosts are agents 1,
             onwards (just as before).

          2) self.ghostBeliefs, the list of belief distributions for each
             of the ghosts (including ghosts that are not alive).  The
             indices into this list should be 1 less than indices into the
             gameState.getLivingGhosts() list.
        """
        pacmanPosition = gameState.getPacmanPosition()
        legal = [a for a in gameState.getLegalPacmanActions()]
        livingGhosts = gameState.getLivingGhosts()
        livingGhostPositionDistributions = \
            [beliefs for i, beliefs in enumerate(self.ghostBeliefs)
             if livingGhosts[i+1]]
        return Directions.EAST

class BasicAgentAA(BustersAgent): #############################INTERESA#############################

    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        self.countActions = 0
        
    ''' Example of counting something'''
    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if(height == True):
                    food = food + 1
        return food
    
    ''' Print the layout'''  
    def printGrid(self, gameState):
        table = ""
        #print(gameState.data.layout) ## Print by terminal
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table

    def printInfo(self, gameState): 
        print("---------------- TICK ", self.countActions, " --------------------------")
        # Map size
        width, height = gameState.data.layout.width, gameState.data.layout.height
        print("Width: ", width, " Height: ", height)
        # Pacman position
        print("Pacman position: ", gameState.getPacmanPosition())
        # Legal actions for Pacman in current position
        print("Legal actions: ", gameState.getLegalPacmanActions())
        # Pacman direction
        print("Pacman direction: ", gameState.data.agentStates[0].getDirection())
        # Number of ghosts
        print("Number of ghosts: ", gameState.getNumAgents() - 1)  
        # Alive ghosts (index 0 corresponds to Pacman and is always false)
        print("Living ghosts: ", gameState.getLivingGhosts())
        # Ghosts positions
        print("Ghosts positions: ", gameState.getGhostPositions())
        # Ghosts directions
        print("Ghosts directions: ", [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)]) ##THIS
        # Manhattan distance to ghosts
        print("Ghosts distances: ", gameState.data.ghostDistances) ##THIS
        # Pending pac dots
        print("Pac dots: ", gameState.getNumFood()) ##THIS
        # Manhattan distance to the closest pac dot
        print("Distance nearest pac dots: ", gameState.getDistanceNearestFood()) ##THIS
        # Map walls
        print("Map:")
        print(gameState.getWalls())
        # Score
        print("Score: ", gameState.getScore())
        
        
    def chooseAction(self, gameState): 
        #Tutorial 01 - IA
        global prevPacmanPosition

        self.countActions = self.countActions + 1
        move = Directions.STOP
        legal = gameState.getLegalActions(0) ##Legal position from the pacman
        nearestGhost = min(d for d in gameState.data.ghostDistances if d is not None) #Distance - problem whit None type
        nearestGhostPosition = gameState.getGhostPositions()[gameState.data.ghostDistances.index(nearestGhost)] #With index from neares Ghost in list ghostDistances, we get position of the ghost with list getghostPositions
        pacmanPosition = gameState.getPacmanPosition() #Tuple
        pacmanCurrentDirection = 0
        if gameState.data.agentStates[0].getDirection() == "North": pacmanCurrentDirection = 2
        elif gameState.data.agentStates[0].getDirection() == "South": pacmanCurrentDirection = 3
        elif gameState.data.agentStates[0].getDirection() == "West": pacmanCurrentDirection = 0
        elif gameState.data.agentStates[0].getDirection() == "East": pacmanCurrentDirection = 1

        dx = nearestGhostPosition[0]-pacmanPosition[0] #Distance x axis between Ghost and Pacman (horizontal movement)
        dy = nearestGhostPosition[1]-pacmanPosition[1] #Distance y axis between Ghost and Pacman (vertical movement)

        #Walls araound pacman
        pacmanWallUp = gameState.getWalls()[gameState.getPacmanPosition()[0]][gameState.getPacmanPosition()[1]+1] #If there is a wall in current pacman's position
        pacmanWallDown = gameState.getWalls()[gameState.getPacmanPosition()[0]][gameState.getPacmanPosition()[1]-1]
        pacmanWallLeft = gameState.getWalls()[gameState.getPacmanPosition()[0]-1][gameState.getPacmanPosition()[1]]
        pacmanWallRight = gameState.getWalls()[gameState.getPacmanPosition()[0]+1][gameState.getPacmanPosition()[1]]
        wallsAroundPacman = [pacmanWallLeft, pacmanWallRight,  pacmanWallUp, pacmanWallDown]

        movement = random.randint(0,3)
        if dy < 0 and not pacmanWallDown and pacmanPosition[1]-1 is not prevPacmanPosition[1]:
            movement = 3
        elif dy > 0 and not pacmanWallUp and pacmanPosition[1]+1 is not prevPacmanPosition[1]:
            movement = 2
        elif dx < 0 and not pacmanWallLeft and pacmanPosition[0]-1 is not prevPacmanPosition[0]:
            movement = 0
        elif dx > 0 and not pacmanWallRight and pacmanPosition[0]+1 is not prevPacmanPosition[0]:
            movement = 1
        
        elif pacmanWallUp and pacmanWallDown and not pacmanWallLeft and not pacmanWallRight: movement = pacmanCurrentDirection
        elif pacmanWallRight and pacmanWallLeft and not pacmanWallUp and not pacmanWallDown: movement = pacmanCurrentDirection
        elif pacmanWallLeft and pacmanWallUp and not pacmanWallRight and not pacmanWallDown:
            if pacmanCurrentDirection == 2: movement = 1 
            else: movement = 3
        elif pacmanWallLeft and pacmanWallDown and not pacmanWallRight and not pacmanWallUp:
            if pacmanCurrentDirection == 3: movement = 1
            else: movement = 2
        elif pacmanWallRight and pacmanWallUp and not pacmanWallLeft and not pacmanWallDown:  
            if pacmanCurrentDirection == 2: movement = 0
            else: movement = 3
        elif pacmanWallRight and pacmanWallDown and not pacmanWallLeft and not pacmanWallUp:
            if pacmanCurrentDirection == 3: movement = 0
            else: movement = 2
        elif wallsAroundPacman.count(False) == 1:
            wall = wallsAroundPacman.index(False)
            movement = wall
        elif wallsAroundPacman.count(True) == 1:
            wall = wallsAroundPacman.index(True)
            if pacmanCurrentDirection is not wall: movement = pacmanCurrentDirection
        
    
        if   ( movement == 0 ) and Directions.WEST in legal:  move = Directions.WEST
        if   ( movement == 1 ) and Directions.EAST in legal: move = Directions.EAST
        if   ( movement == 2 ) and Directions.NORTH in legal:   move = Directions.NORTH
        if   ( movement == 3 ) and Directions.SOUTH in legal: move = Directions.SOUTH
        prevPacmanPosition = pacmanPosition
        print("dirNearest: ",gameState.getDirectionNearestGhost())
        print("relative dist pacdot: ",gameState.getRelativeDistanceNearestPacdot())
        print("relative dist ghost: ",gameState.getRelativeDistanceNearestGhost())
        print("Legal actions: ", gameState.getLegalPacmanActions())
        print("Type of Wall: ", gameState.getTypeOfWall(), wallsAroundPacman)

        #print(gameState.getDirectionNearestFood())
        
        return move
from states import createStates
class QLearningAgent(BustersAgent): #############################INTERESA#############################

    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        self.countActions = 0
        
    """
      Q-Learning Agent

      Functions you should fill in:
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)
    """
    def __init__(self, **args):
        "Initialize Q-values"
        BustersAgent.__init__(self, **args)

        self.actions = {'East':0, 'West':1, 'North':2, 'South':3, 'Stop':4}
        self.table_file = open("qtable.txt", "r+")
#        self.table_file_csv = open("qtable.csv", "r+")        
        self.q_table = self.readQtable()
        self.epsilon = 0.2
        self.alpha = 0.4
        self.discount = 0.5
        dir = ['East', 'West', 'North', 'South', 'North-East', 'North-West', 'South-East', 'South-West']
        dist = ['Close', 'Mid', 'Far']
        mur = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        self.states = createStates(dir, dist, mur)

    def readQtable(self):
        "Read qtable from disc"
        table = self.table_file.readlines()
        q_table = []

        for i, line in enumerate(table):
            row = line.split()
            row = [float(x) for x in row]
            q_table.append(row)

        return q_table

    def writeQtable(self):
        "Write qtable to disc"
        self.table_file.seek(0)
        self.table_file.truncate()
        for line in self.q_table:
            for item in line:
                self.table_file.write(str(item)+" ")
            self.table_file.write("\n")

#         self.table_file_csv.seek(0)
#         self.table_file_csv.truncate()
#         for line in self.q_table:
#             for item in line[:-1]:
#                 self.table_file_csv.write(str(item)+", ")
#             self.table_file_csv.write(str(line[-1]))                
#             self.table_file_csv.write("\n")

            
    def printQtable(self):
        "Print qtable"
        for line in self.q_table:
            print(line)
        print("\n")    
            
    def __del__(self):
        "Destructor. Invokation at the end of each episode"
        self.writeQtable()
        self.table_file.close()

    def computePosition(self, state):
        currentState = (state.getDirectionNearestGhost(), state.getRelativeDistanceNearestGhost(), state.getTypeOfWall())
        print(currentState)
        return self.states.index(currentState)

    def getQValue(self, state, action):

        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        position = self.computePosition(state)
        action_column = self.actions[action]
        return self.q_table[position][action_column]


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        legalActions = state.getLegalPacmanActions()
        if len(legalActions)==0:
          return 0
        return max(self.q_table[self.computePosition(state)])

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        legalActions = state.getLegalPacmanActions()
        if len(legalActions)==0:
          return None

        best_actions = [legalActions[0]]
        best_value = self.getQValue(state, legalActions[0])
        for action in legalActions:
            value = self.getQValue(state, action)
            if value == best_value:
                best_actions.append(action)
            if value > best_value:
                best_actions = [action]
                best_value = value

        return random.choice(best_actions)

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.
        """
        # Pick Action
        legalActions = state.getLegalPacmanActions()

        action = None

        if len(legalActions) == 0:
             return action

        flip = util.flipCoin(self.epsilon)

        if flip:
            return random.choice(legalActions)
        return self.getPolicy(state)


    def update(self, state, action, nextState, reward):
        """
        The parent class calls this to observe a
        state = action => nextState and reward transition.
        You should do your Q-Value update here

        Good Terminal state -> reward 1
        Bad Terminal state -> reward -1
        Otherwise -> reward 0

        Q-Learning update:

        if terminal_state:
        Q(state,action) <- (1-self.alpha) Q(state,action) + self.alpha * (r + 0)
        else:
        Q(state,action) <- (1-self.alpha) Q(state,action) + self.alpha * (r + self.discount * max a' Q(nextState, a'))

        """
        # TRACE for transition and position to update. Comment the following lines if you do not want to see that trace
#         print("Update Q-table with transition: ", state, action, nextState, reward)
#         position = self.computePosition(state)
#         action_column = self.actions[action]
#         print("Corresponding Q-table cell to update:", position, action_column)

        #MODIFICAR EL STATE QUE ME LLEGA AQUI -> state = ('East', 'Close', 1)
        
        '''if currentState == (4,2) or currentState == (4,3):
            self.q_table[self.computePosition(state)][self.actions[action]] = (1-self.alpha)*self.getQValue(state, action) + self.alpha*reward
        else:'''
        
        self.q_table[self.computePosition(state)][self.actions[action]] = (1-self.alpha)*self.getQValue(state, action) + self.alpha*(reward + self.discount*self.computeValueFromQValues(nextState))
            
        # TRACE for updated q-table. Comment the following lines if you do not want to see that trace
#         print("Q-table:")
#         self.printQtable()

    def getPolicy(self, state):
        "Return the best action in the qtable for a given state"
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        "Return the highest q value for a given state"
        return self.computeValueFromQValues(state)

'''print("dirNearest: ",gameState.getDirectionNearestGhost())
print("relative dist pacdot: ",gameState.getRelativeDistanceNearestPacdot())
print("relative dist ghost: ",gameState.getRelativeDistanceNearestGhost())
print("Legal actions: ", gameState.getLegalPacmanActions())
print("Wall in front: ", gameState.isWallPacmanDirection())
#print(gameState.getDirectionNearestFood())'''