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
    
    def set_val(self, val, x, y):
        self.allValues[y][x] = val

    def print(self, startX, startY, width, height):
        for yPos in range(height):
            slice = self.allValues[startY + yPos][startX:startX + width]
            print(slice)

    def count_nines(self):
        nines = 0
        for y in range(len(self.allValues)):
            for x in range(len(self.allValues[0])):
                if self.val(x, y) == 9:
                    nines += 1
        return nines

class BassinCountItem:
    def __init__(self, bassin_number):
        self.bassins = [bassin_number]
        self.count = 1

    def matches_bassin_number(self, bassin_number):
        return bassin_number in self.bassins

    def increment(self):
        self.count += 1
    
    def merge(self, otherItem):
        for b in otherItem.bassins:
            self.bassins.append(b)
        
        self.count += otherItem.count
        self.print_item()

    def print_item(self):
        print(f'{self.bassins}: {self.count}.')

class BassinCounter:
    def __init__(self):
        self.bassinsCount = []

    def count_bassin(self, bassin_number):
        for item in self.bassinsCount:
            if item.matches_bassin_number(bassin_number):
                item.increment()
                return
        self.bassinsCount.append(BassinCountItem(bassin_number))

    def merge_bassins(self, bassin_number_1, bassin_number_2):
        itemToMerge = None
        deleteIndex = None
        alreadyMerged = False

        for i in range(len(self.bassinsCount)):
            item = self.bassinsCount[i]
            if item.matches_bassin_number(bassin_number_2):
                if (item).matches_bassin_number(bassin_number_1):
                    alreadyMerged = True
                else:
                    itemToMerge = item
                    deleteIndex = i
            
        if (not alreadyMerged):
            self.bassinsCount.pop(deleteIndex)

            for item in self.bassinsCount:
                if item.matches_bassin_number(bassin_number_1):
                    item.merge(itemToMerge)
                
    def print_count(self):
        for item in self.bassinsCount:
            item.print_item()

    def bassin_sizes(self):
        return [item.count for item in self.bassinsCount]
        
lines = open("Input.txt",'r').read().splitlines()
board = Board(lines)
(xSize, ySize) = board.size()

new_bassin_number = 1000

def get_bassin_number(val):
    if val != None and val >= 1000:
        return val
    else:
        return None

counter = BassinCounter() 

def process_location(x, y):
    global new_bassin_number

    left = board.val(x-1, y)
    up = board.val(x, y-1)
    val = board.val(x, y)
    
    bassinLeft = get_bassin_number(left)
    bassinUp = get_bassin_number(up)

    if val != 9:
        existing_bassins = []
        if bassinLeft != None:
            existing_bassins.append(bassinLeft)
        if bassinUp != None:
            existing_bassins.append(bassinUp)
        
        existing_bassins = list(set(existing_bassins))
        
        existin_bassin_len = len(existing_bassins)
        bassin_to_count = existing_bassins[0] if existin_bassin_len > 0 else new_bassin_number

        if existin_bassin_len == 0:
            new_bassin_number += 1

        board.set_val(bassin_to_count, x, y)
        counter.count_bassin(bassin_to_count)

        if existin_bassin_len == 2:
            counter.merge_bassins(existing_bassins[0], existing_bassins[1])
        
for y in range(ySize):
    for x in range(xSize):
        process_location(x, y)

counter.print_count()

allBassins = counter.bassin_sizes()
allBassins.sort()
allBassins.reverse()
print(f"All bassins {allBassins}, res = {allBassins[0]*allBassins[1]*allBassins[2]}")

print(sum(counter.bassin_sizes()))
print(board.count_nines())