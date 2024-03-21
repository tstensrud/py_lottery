from ticket_operations import *
from user_operations import *

currentWinnerNumbers = [None]*numbersPerRow

# draw a row of winning numbers. Once a number is drawn it's removed from the pool of available numbers
def generateWinningNumbers():
    availableNumbers = [None]*maxNumbers
    for i in range(maxNumbers):
        availableNumbers[i] = i+1
    
    winningNumbers = [None]*numbersPerRow
    
    for i in range(len(winningNumbers)):
        num = random.choice(availableNumbers)
        winningNumbers[i] = num
        availableNumbers.remove(num)
    
    return sorted(winningNumbers)
    

currentWinnerNumbers = generateWinningNumbers()
print(currentWinnerNumbers)





















