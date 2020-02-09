def isboxfull(box,grd):
    if grd[box] == 'O' or grd[box] == 'X':
        return True
    else:
        return False

def isboardfull(grd):
    if (isboxfull(0,grd) == True and
        isboxfull(1,grd) == True and
        isboxfull(2,grd) == True and 
        isboxfull(3,grd) == True and 
        isboxfull(4,grd) == True and 
        isboxfull(5,grd) == True and 
        isboxfull(6,grd) == True and 
        isboxfull(7,grd) == True and 
        isboxfull(8,grd) == True):
        return True
    else: return False

def displaygrid(grd):
    print(grd[0] + '|' + grd[1] + '|' + grd[2])
    print('-+-+-')
    print(grd[3] + '|' + grd[4] + '|' + grd[5])
    print('-+-+-')
    print(grd[6] + '|' + grd[7] + '|' + grd[8])

def checkwin(grd,playertemp):
    OXt = playerdict[playertemp]
    if grd[0] == OXt and grd[4] == OXt and grd[8] == OXt: return True
    elif grd[2] == OXt and grd[4] == OXt and grd[6] == OXt: return True
    elif grd[0] == OXt and grd[1] == OXt and grd[2] == OXt: return True
    elif grd[3] == OXt and grd[4] == OXt and grd[5] == OXt: return True
    elif grd[6] == OXt and grd[7] == OXt and grd[8] == OXt: return True
    elif grd[0] == OXt and grd[3] == OXt and grd[6] == OXt: return True
    elif grd[1] == OXt and grd[4] == OXt and grd[7] == OXt: return True
    elif grd[2] == OXt and grd[5] == OXt and grd[8] == OXt: return True
    else: return False

currentgrid = [' ']*9
numbergrid = [str(n) for n in range(1,10)]
currentplayer = 0
playerdict = {0:'O',1:'X'}

displaygrid(numbergrid)
print('\nO goes first. Enter ctrl+d to quit')

while True:
    OX = playerdict[currentplayer]
    if isboardfull(currentgrid) == True:
        print('Tie game')
        break
    else:
        print('\n' + OX + '\'s turn')
        try:
            readinput = input('Select a box between 1 and 9: ')
            currentbox = int(readinput) - 1
        except:
            print('Needs to be an integer between 1 and 9')
        else:
            if currentbox < 0 or currentbox > 8:
                print('Needs to be an integer between 1 and 9')
                continue
            else:
                if isboxfull(currentbox,currentgrid) == True:
                    print('Box is already full')
                    continue
                else:
                    currentgrid[currentbox] = OX
                    displaygrid(currentgrid)
                    if checkwin(currentgrid,currentplayer) == True:
                        print('\n' + OX + ' wins')
                        break
                    else:
                        currentplayer = (currentplayer + 1) % 2
                        continue