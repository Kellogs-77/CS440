import numpy as np

class MazeGenerator:
    

    def __init__(self):
        self.heaplist = [0][0]

    def create_maze(w, h):

        weights=np.array([0.3, 0.7])
        items=np.array([1, 0])
        rng = np.random.default_rng()
        array = rng.choice(items, size=w*h, p=weights / sum(weights))
        array = np.reshape(array, (w, h))
        array[0][0] = 0
        

        array[w-1][h-1] = 0
        return array
    
    
