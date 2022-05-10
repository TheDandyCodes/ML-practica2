
def createStates(direction, distance, walls):
    states = [(d, ds, m) for d in direction for ds in distance for m in walls]
    return states
dir = ['East', 'West', 'North', 'South', 'North-East', 'North-West', 'South-East', 'South-West']
dist = ['Close', 'Mid', 'Far']
mur = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
states = createStates(dir, dist, mur)

print(len(states))

