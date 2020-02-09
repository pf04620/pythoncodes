import random
import copy
from colorama import Fore, Back, Style
import tkinter
from tkinter.filedialog import askopenfilename

def populatebox(rbox,cbox,grd):
    bl = numlist.copy()
    for rr in range(rbox,rbox+3):
        for cc in range(cbox,cbox+3):
            cl = [grd[ii][cc] for ii in range(9) if grd[ii][cc] != 0]
            rl = [grd[rr][jj] for jj in range(9) if grd[rr][jj] != 0]
            al = list(set(bl) - set(rl + cl))
            if len(al) > 0:
                tn = random.choice(al)
                grd[rr][cc] = tn
                bl.remove(tn)
            else:
                return False
    return True

def populategrid():
    while True:
        grd = copy.deepcopy(emptygrid)
        if populatebox(0,0,grd) == False: continue
        if populatebox(0,3,grd) == False: continue
        if populatebox(0,6,grd) == False: continue
        if populatebox(3,0,grd) == False: continue
        if populatebox(3,3,grd) == False: continue
        if populatebox(3,6,grd) == False: continue
        if populatebox(6,0,grd) == False: continue
        if populatebox(6,3,grd) == False: continue
        if populatebox(6,6,grd) == False: continue
        break
    return grd

def printgrid(grd):
    prntgrd = copy.deepcopy(grd)
    for rr in range(9):
        for cc in range(9):
            if grd[rr][cc] == 0:
                prntgrd[rr][cc] = '.'
                
    print('    ' + Back.CYAN + Fore.RED + Style.BRIGHT + '1 2 3   4 5 6   7 8 9' + Style.RESET_ALL)
    print('  +-------+-------+-------+')
    rn = 1
    for row in prntgrd[0:3]:
        print(Back.CYAN + Fore.RED + Style.BRIGHT + str(rn) +  Style.RESET_ALL + ' | ' + ' '.join([str(elem) for elem in row[0:3]]) + ' | ' + ' '.join([str(elem) for elem in row[3:6]]) + ' | ' + ' '.join([str(elem) for elem in row[6:9]]) + ' |')
        rn += 1
    print(Back.CYAN + Style.BRIGHT + ' ' +  Style.RESET_ALL + ' +-------+-------+-------+')
    for row in prntgrd[3:6]:
        print(Back.CYAN + Fore.RED + Style.BRIGHT + str(rn) +  Style.RESET_ALL + ' | ' + ' '.join([str(elem) for elem in row[0:3]]) + ' | ' + ' '.join([str(elem) for elem in row[3:6]]) + ' | ' + ' '.join([str(elem) for elem in row[6:9]]) + ' |')
        rn += 1
    print(Back.CYAN + Style.BRIGHT + ' ' +  Style.RESET_ALL + ' +-------+-------+-------+')
    for row in prntgrd[6:9]:
        print(Back.CYAN + Fore.RED + Style.BRIGHT + str(rn) +  Style.RESET_ALL + ' | ' + ' '.join([str(elem) for elem in row[0:3]]) + ' | ' + ' '.join([str(elem) for elem in row[3:6]]) + ' | ' + ' '.join([str(elem) for elem in row[6:9]]) + ' |')
        rn += 1
    print('  +-------+-------+-------+')
    
def generateallowedgrid(grd):
    aldgrd = [[[] for _ in range(9)] for _ in range(9)]
    for rra in range(9):
        for cca in range(9):
            if grd[rra][cca] != 0:
                aldgrd[rra][cca] = []
            elif grd[rra][cca] == 0:
                collist = [grd[ii][cca] for ii in range(9) if grd[ii][cca] != 0]
                rowlist = [grd[rra][jj] for jj in range(9) if grd[rra][jj] != 0]
                
                if rra in [0,1,2] and cca in [0,1,2]:
                    boxlist = [grd[rrb][ccb] for ccb in [0,1,2] for rrb in [0,1,2] if grd[rrb][ccb] != 0]
                if rra in [0,1,2] and cca in [3,4,5]:
                    boxlist = [grd[rrb][ccb] for ccb in [3,4,5] for rrb in [0,1,2] if grd[rrb][ccb] != 0]
                if rra in [0,1,2] and cca in [6,7,8]:
                    boxlist = [grd[rrb][ccb] for ccb in [6,7,8] for rrb in [0,1,2] if grd[rrb][ccb] != 0]
                if rra in [3,4,5] and cca in [0,1,2]:
                    boxlist = [grd[rrb][ccb] for ccb in [0,1,2] for rrb in [3,4,5] if grd[rrb][ccb] != 0]
                if rra in [3,4,5] and cca in [3,4,5]:
                    boxlist = [grd[rrb][ccb] for ccb in [3,4,5] for rrb in [3,4,5] if grd[rrb][ccb] != 0]
                if rra in [3,4,5] and cca in [6,7,8]:
                    boxlist = [grd[rrb][ccb] for ccb in [6,7,8] for rrb in [3,4,5] if grd[rrb][ccb] != 0]
                if rra in [6,7,8] and cca in [0,1,2]:
                    boxlist = [grd[rrb][ccb] for ccb in [0,1,2] for rrb in [6,7,8] if grd[rrb][ccb] != 0]
                if rra in [6,7,8] and cca in [3,4,5]:
                    boxlist = [grd[rrb][ccb] for ccb in [3,4,5] for rrb in [6,7,8] if grd[rrb][ccb] != 0]              
                if rra in [6,7,8] and cca in [6,7,8]:
                    boxlist = [grd[rrb][ccb] for ccb in [6,7,8] for rrb in [6,7,8] if grd[rrb][ccb] != 0]

                tmpald = list(set(numlist) - set(boxlist + rowlist + collist))
                aldgrd[rra][cca] = tmpald
    return aldgrd

def numfullsquares(grd):
    numsq = 0
    for rr in range(9):
        for cc in range(9):
            if grd[rr][cc] != 0:
                numsq += 1
    return numsq

def occursonce(lst, item):
    return lst.count(item) == 1

def checkbysquare(grd):
    allowedgrid = generateallowedgrid(grd)
    for rr in range(9):
        for cc in range(9):
            tempallowed = allowedgrid[rr][cc]
            if len(tempallowed) == 1:
                grd[rr][cc] = tempallowed[0]
    return grd

def checkbybox(grd):
    allowedgrid = generateallowedgrid(grd)
    allowedbybox = [[] for _ in range(9)]
    
    for rr1 in [0,1,2]:
        for cc1 in [0,1,2]:
            allowedbybox[0] += allowedgrid[rr1][cc1]
    for rr2 in [0,1,2]:
        for cc2 in [3,4,5]:
            allowedbybox[1] += allowedgrid[rr2][cc2]
    for rr3 in [0,1,2]:
        for cc3 in [6,7,8]:
            allowedbybox[2] += allowedgrid[rr3][cc3]        
    for rr4 in [3,4,5]:
        for cc4 in [0,1,2]:
            allowedbybox[3] += allowedgrid[rr4][cc4]
    for rr5 in [3,4,5]:
        for cc5 in [3,4,5]:
            allowedbybox[4] += allowedgrid[rr5][cc5]
    for rr6 in [3,4,5]:
        for cc6 in [6,7,8]:
            allowedbybox[5] += allowedgrid[rr6][cc6]        
    for rr7 in [6,7,8]:
        for cc7 in [0,1,2]:
            allowedbybox[6] += allowedgrid[rr7][cc7]        
    for rr8 in [6,7,8]:
        for cc8 in [3,4,5]:
            allowedbybox[7] += allowedgrid[rr8][cc8]
    for rr9 in [6,7,8]:
        for cc9 in [6,7,8]:
            allowedbybox[8] += allowedgrid[rr9][cc9]
    
    for nn in numlist:
        if occursonce(allowedbybox[0],nn) == True:
            for rr1 in [0,1,2]:
                for cc1 in [0,1,2]:
                    if nn in allowedgrid[rr1][cc1]:
                        grd[rr1][cc1] = nn
        if occursonce(allowedbybox[1],nn) == True:
            for rr2 in [0,1,2]:
                for cc2 in [3,4,5]:
                    if nn in allowedgrid[rr2][cc2]:
                        grd[rr2][cc2] = nn                
        if occursonce(allowedbybox[2],nn) == True:
            for rr3 in [0,1,2]:
                for cc3 in [6,7,8]:
                    if nn in allowedgrid[rr3][cc3]:
                        grd[rr3][cc3] = nn
        if occursonce(allowedbybox[3],nn) == True:
            for rr4 in [3,4,5]:
                for cc4 in [0,1,2]:
                    if nn in allowedgrid[rr4][cc4]:
                        grd[rr4][cc4] = nn
        if occursonce(allowedbybox[4],nn) == True:
            for rr5 in [3,4,5]:
                for cc5 in [3,4,5]:
                    if nn in allowedgrid[rr5][cc5]:
                        grd[rr5][cc5] = nn                
        if occursonce(allowedbybox[5],nn) == True:
            for rr6 in [3,4,5]:
                for cc6 in [6,7,8]:
                    if nn in allowedgrid[rr6][cc6]:
                        grd[rr6][cc6] = nn
        if occursonce(allowedbybox[6],nn) == True:
            for rr7 in [6,7,8]:
                for cc7 in [0,1,2]:
                    if nn in allowedgrid[rr7][cc7]:
                        grd[rr7][cc7] = nn
        if occursonce(allowedbybox[7],nn) == True:
            for rr8 in [6,7,8]:
                for cc8 in [3,4,5]:
                    if nn in allowedgrid[rr8][cc8]:
                        grd[rr8][cc8] = nn    
        if occursonce(allowedbybox[8],nn) == True:
            for rr9 in [6,7,8]:
                for cc9 in [6,7,8]:
                    if nn in allowedgrid[rr9][cc9]:
                        grd[rr9][cc9] = nn
    return grd

def checkbyrow(grd):
    allowedgrid = generateallowedgrid(grd)
    allowedbyrow = [[] for _ in range(9)]
    
    for cc1 in range(9):
        allowedbyrow[0] += allowedgrid[0][cc1]
    for cc2 in range(9):
        allowedbyrow[1] += allowedgrid[1][cc2]
    for cc3 in range(9):
        allowedbyrow[2] += allowedgrid[2][cc3]
    for cc4 in range(9):
        allowedbyrow[3] += allowedgrid[3][cc4]
    for cc5 in range(9):
        allowedbyrow[4] += allowedgrid[4][cc5]
    for cc6 in range(9):
        allowedbyrow[5] += allowedgrid[5][cc6]
    for cc7 in range(9):
        allowedbyrow[6] += allowedgrid[6][cc7]
    for cc8 in range(9):
        allowedbyrow[7] += allowedgrid[7][cc8]
    for cc9 in range(9):
        allowedbyrow[8] += allowedgrid[8][cc9]
        
    for nn in numlist:
        for rrr in range(9):
            if occursonce(allowedbyrow[rrr],nn) == True:
                for ccr in range(9):
                    if nn in allowedgrid[rrr][ccr]:
                        grd[rrr][ccr] = nn
    return grd

def checkbycol(grd):
    allowedgrid = generateallowedgrid(grd)
    allowedbycol = [[] for _ in range(9)]
    
    for rr1 in range(9):
        allowedbycol[0] += allowedgrid[rr1][0]
    for rr2 in range(9):
        allowedbycol[1] += allowedgrid[rr2][1]
    for rr3 in range(9):
        allowedbycol[2] += allowedgrid[rr3][2]
    for rr4 in range(9):
        allowedbycol[3] += allowedgrid[rr4][3]
    for rr5 in range(9):
        allowedbycol[4] += allowedgrid[rr5][4]
    for rr6 in range(9):
        allowedbycol[5] += allowedgrid[rr6][5]
    for rr7 in range(9):
        allowedbycol[6] += allowedgrid[rr7][6]
    for rr8 in range(9):
        allowedbycol[7] += allowedgrid[rr8][7]
    for rr9 in range(9):
        allowedbycol[8] += allowedgrid[rr9][8]
        
    for nn in numlist:
        for ccc in range(9):
            if occursonce(allowedbycol[ccc],nn) == True:
                for rrc in range(9):
                    if nn in allowedgrid[rrc][ccc]:
                        grd[rrc][ccc] = nn
    return grd
    
def checkcomplete(grd):
    gridsum = 0
    for kk in range(9):
        gridsum += sum(grd[kk])
    if gridsum == 405: return True
    else: return False

def issolvable(grd):
    nl = 0
    sgrd = copy.deepcopy(grd)
    while nl <= 81:
        startloop = numfullsquares(sgrd)
        sgrd = checkbysquare(sgrd)
        sgrd = checkbybox(sgrd)
        sgrd = checkbyrow(sgrd)
        sgrd = checkbycol(sgrd)
    
        if numfullsquares(sgrd) == 81 and checkcomplete(sgrd) == True:
            return True
        
        if numfullsquares(sgrd) == startloop:
            return False
        nl += 1
    return False

def creategridfrominput(grd):
    grd = grd.replace('ï»¿','')
    grd = grd.replace('\n','')
    grd = grd.replace(',','')
    ii = 0
    outgrd = copy.deepcopy(emptygrid)
    for rr in range(9):
        for cc in range(9):
            outgrd[rr][cc] = int(grd[ii])
            ii += 1
    return outgrd
            
def printallowed(aldsq):
    print('========')
    for x in [3,6,9]:
        if x-2 in aldsq: z1 = str(x-2)
        else: z1 = ' '
        if x-1 in aldsq: z2 = str(x-1)
        else: z2 = ' '
        if x in aldsq: z3 = str(x)
        else: z3 = ' '
        print(z1,z2,z3,'||')
    print('========')

def haserror(plygrd,slngrd):
    for rr in range(9):
        for cc in range(9):
            if plygrd[rr][cc] != 0 and plygrd[rr][cc] != slngrd[rr][cc]:
                return True
    return False

# MAIN CODE
numlist = [n for n in range(1,10)]
emptygrid = [[0] * 9 for _ in range(9)]

print('Welcome to Sudoku')
while True:
    playchoice = input('Use pre-loaded play grid = 0, have computer make play grid = 1: ')
    if playchoice != '0' and playchoice != '1':
        print('Bad input')
        continue
    elif playchoice == '0':
        tkinter.Tk().withdraw()
        playname = askopenfilename()
        with open(playname) as f:
            rawplaygrid = f.read()
        playgrid = creategridfrominput(rawplaygrid)
        while True:
            solnchoice = input('Use a pre-loaded solution = 0, have computer find solution = 1: ')
            if solnchoice != '0' and solnchoice != '1':
                print('Bad input')
                continue
            elif solnchoice == '0':
                tkinter.Tk().withdraw()
                solnname = askopenfilename()
                with open(solnname) as f:
                    rawsolngrid = f.read()
                solngrid = creategridfrominput(rawsolngrid)
                if numfullsquares(solngrid) != 81 or checkcomplete(solngrid) != True:
                    print('May not be a correct solution')
                    continue
                break
            elif solnchoice == '1':
                if issolvable(playgrid) == False:
                    print('Can\'t solve this grid using basic techniques')
                    continue
                else:
                    while True:
                        playgrid = checkbysquare(playgrid)
                        playgrid = checkbybox(playgrid)
                        playgrid = checkbyrow(playgrid)
                        playgrid = checkbycol(playgrid)
                        if numfullsquares(playgrid) == 81 and checkcomplete(playgrid) == True:
                            break
                break
    elif playchoice == '1':
        solngrid = populategrid()
        playgrid = copy.deepcopy(solngrid)
        for _ in range(40):
            rand1 = random.choice(range(9))
            rand2 = random.choice(range(9))
            
            if playgrid[rand1][rand2] != 0:
                numholder = playgrid[rand1][rand2]
                playgrid[rand1][rand2] = 0
                if issolvable(playgrid) == False:
                    playgrid[rand1][rand2] = numholder
                    break
    break

print('\nEnter as: row (space) column')
prow = -1
pcol = -1
while True:
    if playgrid == solngrid:
        print('You win')
        break
    printgrid(playgrid)
    print(str(numfullsquares(playgrid)) + ' full squares')
    
    playeraction = str(input('a = add a number,\nd = delete a number,\nh = random hint,\nu = undo previous add,\np = see allowed moves (pencilmarks),\nc = check for errors,\ncrtl+d = quit: '))
    if playeraction not in ['a','d','h','u','p','c','A','D','H','U','P','C']:
        print('Bad input')
        continue
    elif playeraction == 'h' or playeraction == 'H':
        while True:
            randrow = random.choice(range(9))
            randcol = random.choice(range(9))
            if playgrid[randrow][randcol] == 0:
                playgrid[randrow][randcol] = solngrid[randrow][randcol]
                break
            else: continue
    elif playeraction == 'u' or playeraction == 'U':
        if prow == -1 and pcol == -1:
            print('Haven\'t added anything yet\n')
        else:
            playgrid[prow][pcol] = 0        
    elif playeraction == 'c' or playeraction == 'C':
        if haserror(playgrid,solngrid) == True:
            print('\nThere is a least one error\n')
        else:
            print('\nThere are no errors\n')
    else:
        while True:
            try:
                ir, ic = input('Which square? ').split()
            except:
                print('Bad input')
                continue
            else:
                break
        inrow = int(ir) - 1
        incol = int(ic) - 1
        if inrow < 0 or inrow > 8 or incol < 0 or incol > 8:
            print('Bad input')
            continue
        if playeraction == 'a' or playeraction == 'A':
            addnum = int(input('What value? '))
            if addnum < 1 or addnum > 9:
                print('Bad input')
                continue
            else:
                playgrid[inrow][incol] = addnum
                prow = inrow
                pcol = incol
        elif playeraction == 'p' or playeraction == 'P':
            allowedgrid = generateallowedgrid(playgrid)
            printallowed(allowedgrid[inrow][incol])
        elif playeraction == 'd' or playeraction == 'D':
            playgrid[inrow][incol] = 0