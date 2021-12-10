def split_to_numbers(line):
    return [int(char) for char in line]

class Board:
    def __init__(self, lines):
        self.allValues = []
        for line in lines:
            self.allValues.append(split_to_numbers(line))
    
    def size(self):
        return (len(self.allValues[0]), len(self.allValues))
    
    def val(self, x, y):
        if y < 0 or y >= len(self.allValues):
            return None
        yLine = self.allValues[y]
        if x < 0 or x >= len(yLine):
            return None
        
        return yLine[x]

lines = open("Input.txt",'r').read().splitlines()
board = Board(lines)
(xSize, ySize) = board.size()

minima =[]

for x in range(xSize):
    for y in range(ySize):
        left = board.val(x-1, y)
        right = board.val(x+1, y)
        up = board.val(x, y-1)
        down = board.val(x, y+1)

        val = board.val(x, y)
        def lessThan(edge):
            return edge == None or val < edge

        if lessThan(left) and lessThan(right) and lessThan(up) and lessThan(down):
            minima.append(val)

totalRiskLevel = sum(minima) + len(minima)

print(f'Total: {totalRiskLevel}')