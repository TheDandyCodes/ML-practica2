def createStates(direction, distance, walls):
    states = [(d, ds, m) for d in direction for ds in distance for m in walls]
    return states

