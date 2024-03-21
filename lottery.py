from ticket_operations import *
from user_operations import *

currentWinnerNumbers = [None]*numbersPerRow

# draw a row of winning numbers. Once a number is drawn it's removed from the pool of available numbers
def generateWinningNumbers():
    availableNumbers = [None]*maxPlayableNumbers #define array of playable numbers
    for i in range(maxPlayableNumbers):
        availableNumbers[i] = i+1 #add numbers from 1 to n-playable numbers, defined by maxPlayableNumbers (40 default)
    winningNumbers = [None]*numbersPerRow #set up local list of winning numbers, max defined by numbersPerRow
    for i in range(len(winningNumbers)):
        num = random.choice(availableNumbers) #select random number from available number and add it to winningNumbers
        winningNumbers[i] = num
        availableNumbers.remove(num) #remove num from pool of available numbers, simulating balls in a physical lottery
    return sorted(winningNumbers)
























