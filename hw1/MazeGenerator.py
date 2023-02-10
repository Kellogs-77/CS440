import numpy as np

class MazeGenerator:
    

    def __init__(self):
        self.heaplist = [0][0]

    def create_maze(w, h):
        array = np.random.randint(2, size=(w,h))
        array[0][0] = 0
        return array
    
    array = create_maze(10,10)
    print(array)
