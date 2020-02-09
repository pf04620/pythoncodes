#optional / unimportant:
#    - allow player to go back to previous turns
#    - convert movelog to standard chess notation
#    - record captured pieces
#    - pawn exchange only for captured pieces
#    - display checkered board
#    - give player option for a random move
#    - ability to quit at any time using ctrl+d
#    - implement other types of draws: 3x repitition, 50x no capture, king vs king [+ bishop or knight]
#    - castling doesn't account for attack by pawn;
#    - in rare cases, sometimes thinks it can en passant when it actually can't

from colorama import Fore, Back, Style
import copy

class blank:
    def __init__(self,row,col,side):
        self.row = row
        self.col = col
        self.side = side
    
    def __str__(self):
        return '.'

class pawn:
    def __init__(self,row,col,side,brd):
        self.row = row
        self.col = col
        self.side = side
        self.brd = brd
    
    def __str__(self):
        if self.side == 'w':
            return str(Fore.CYAN + 'p')
        if self.side == 'b':
            return str(Style.BRIGHT + 'P')
    
    @property
    def allowed(self):
        tempallowed = list()
        
        if self.side == 'w':
            if str(self.brd[self.row-1][self.col]) == '.':
                tempallowed.append([self.row-1,self.col])
                if self.row == 6 and str(self.brd[self.row-2][self.col]) == '.':
                    tempallowed.append([self.row-2,self.col])
            
            if self.col != 7:
                if self.brd[self.row-1][self.col+1].side == 'b':
                    tempallowed.append([self.row-1,self.col+1])
            
            if self.col != 0:
                if self.brd[self.row-1][self.col-1].side == 'b':
                    tempallowed.append([self.row-1,self.col-1])
                
        if self.side == 'b':
            if str(self.brd[self.row+1][self.col]) == '.':
                tempallowed.append([self.row+1,self.col])
                if self.row == 1 and str(self.brd[self.row+2][self.col]) == '.':
                    tempallowed.append([self.row+2,self.col])
                    
            if self.col != 7:
                if self.brd[self.row+1][self.col+1].side == 'w':
                    tempallowed.append([self.row+1,self.col+1])
            if self.col != 0:
                if self.brd[self.row+1][self.col-1].side == 'w':
                    tempallowed.append([self.row+1,self.col-1])
                    
        return tempallowed
    
    def ispawnexchange(self):
        if (self.side == 'w' and self.row == 0) or (self.side == 'b' and self.row == 7):
            return True
        else:
            return False
    
    def pawnexchange(self):
        while True:
            exchangepiece = input('Pawn exchange. Choose only R, N, B, or Q (not case sensitive): ')
            if exchangepiece not in ['R','r','N','n','B','b','Q','q']:
                print('Bad input')
                continue
            elif exchangepiece == 'R' or exchangepiece ==  'r':
                self.brd[self.row][self.col] = rook(self.row,self.col,self.side,self.brd)
                break
            elif exchangepiece == 'N' or exchangepiece ==  'n':
                self.brd[self.row][self.col] = knight(self.row,self.col,self.side,self.brd)
                break
            elif exchangepiece == 'B' or exchangepiece ==  'b':
                self.brd[self.row][self.col] = bishop(self.row,self.col,self.side,self.brd)
                break
            elif exchangepiece == 'Q' or exchangepiece ==  'q':
                self.brd[self.row][self.col] = queen(self.row,self.col,self.side,self.brd)
                break
        return self.brd

class rook:
    def __init__(self,row,col,side,brd):
        self.row = row
        self.col = col
        self.side = side
        self.brd = brd
        
    def __str__(self):
        if self.side == 'w':
            return str(Fore.CYAN + 'r')
        if self.side == 'b':
            return str(Style.BRIGHT + 'R')
    
    @property
    def allowed(self):
        tempallowed = list()        
        
        for nn in range(1,8):
            fr = self.row - nn
            if fr >= 0:
                if str(self.brd[fr][self.col]) == '.':
                    tempallowed.append([fr,self.col])
                elif self.brd[fr][self.col].side != self.side:
                    tempallowed.append([fr,self.col])
                    break
                elif self.brd[fr][self.col].side == self.side:
                    break
        
        for ss in range(1,8):
            fr = self.row + ss
            if fr <= 7:
                if str(self.brd[fr][self.col]) == '.':
                    tempallowed.append([fr,self.col])
                elif self.brd[fr][self.col].side != self.side:
                    tempallowed.append([fr,self.col])
                    break
                elif self.brd[fr][self.col].side == self.side:
                    break
        
        for ee in range(1,8):
            fc = self.col + ee
            if fc <= 7:
                if str(self.brd[self.row][fc]) == '.':
                    tempallowed.append([self.row,fc])
                elif self.brd[self.row][fc].side != self.side:
                    tempallowed.append([self.row,fc])
                    break
                elif self.brd[self.row][fc].side == self.side:
                    break
        
        for ww in range(1,8):
            fc = self.col - ww
            if fc >= 0:
                if str(self.brd[self.row][fc]) == '.':
                    tempallowed.append([self.row,fc])
                elif self.brd[self.row][fc].side != self.side:
                    tempallowed.append([self.row,fc])
                    break
                elif self.brd[self.row][fc].side == self.side:
                    break

        return tempallowed

class knight:
    def __init__(self,row,col,side,brd):
        self.row = row
        self.col = col
        self.side = side
        self.brd = brd
    
    def __str__(self):
        if self.side == 'w':
            return str(Fore.CYAN + 'n')
        if self.side == 'b':
            return str(Style.BRIGHT + 'N')
        
    @property
    def allowed(self):
        tempallowed = list()
        
        for drow1 in [-2,2]:
            for dcol1 in [-1,1]:
                fr = self.row + drow1
                fc = self.col + dcol1
                if fr >= 0 and fr <= 7 and fc >= 0 and fc <= 7:
                    if self.brd[fr][fc].side != self.side:
                        tempallowed.append([fr,fc])
                    
        for drow2 in [-1,1]:
            for dcol2 in [-2,2]:
                fr = self.row + drow2
                fc = self.col + dcol2
                if fr >= 0 and fr <= 7 and fc >= 0 and fc <= 7:
                    if self.brd[fr][fc].side != self.side:
                        tempallowed.append([fr,fc])
        return tempallowed
        
class bishop:
    def __init__(self,row,col,side,brd):
        self.row = row
        self.col = col
        self.side = side
        self.brd = brd
    
    def __str__(self):
        if self.side == 'w':
            return str(Fore.CYAN + 'b')
        if self.side == 'b':
            return str(Style.BRIGHT + 'B')
        
    @property
    def allowed(self):
        tempallowed = list()
        
        for ne in range(1,8):
            fr = self.row - ne
            fc = self.col + ne
            if fr >= 0 and fr <= 7 and fc >= 0 and fc <= 7:
                if str(self.brd[fr][fc]) == '.':
                    tempallowed.append([fr,fc])
                elif self.brd[fr][fc].side != self.side:
                    tempallowed.append([fr,fc])
                    break
                elif self.brd[fr][fc].side == self.side:
                    break
                
        for nw in range(1,8):
            fr = self.row - nw
            fc = self.col - nw
            if fr >= 0 and fr <= 7 and fc >= 0 and fc <= 7:
                if str(self.brd[fr][fc]) == '.':
                    tempallowed.append([fr,fc])
                elif self.brd[fr][fc].side != self.side:
                    tempallowed.append([fr,fc])
                    break
                elif self.brd[fr][fc].side == self.side:
                    break
                
        for se in range(1,8):
            fr = self.row + se
            fc = self.col + se
            if fr >= 0 and fr <= 7 and fc >= 0 and fc <= 7:
                if str(self.brd[fr][fc]) == '.':
                    tempallowed.append([fr,fc])
                elif self.brd[fr][fc].side != self.side:
                    tempallowed.append([fr,fc])
                    break
                elif self.brd[fr][fc].side == self.side:
                    break
                
        for sw in range(1,8):
            fr = self.row + sw
            fc = self.col - sw
            if fr >= 0 and fr <= 7 and fc >= 0 and fc <= 7:
                if str(self.brd[fr][fc]) == '.':
                    tempallowed.append([fr,fc])
                elif self.brd[fr][fc].side != self.side:
                    tempallowed.append([fr,fc])
                    break
                elif self.brd[fr][fc].side == self.side:
                    break
        return tempallowed

class queen:
    def __init__(self,row,col,side,brd):
        self.row = row
        self.col = col
        self.side = side
        self.brd = brd

    def __str__(self):
        if self.side == 'w':
            return str(Fore.CYAN + 'q')
        if self.side == 'b':
            return str(Style.BRIGHT + 'Q')
    
    @property
    def allowed(self):
        tempallowed = list()
        
        for nn in range(1,8):
            fr = self.row - nn
            if fr >= 0:
                if str(self.brd[fr][self.col]) == '.':
                    tempallowed.append([fr,self.col])
                elif self.brd[fr][self.col].side != self.side:
                    tempallowed.append([fr,self.col])
                    break
                elif self.brd[fr][self.col].side == self.side:
                    break
        
        for ss in range(1,8):
            fr = self.row + ss
            if fr <= 7:
                if str(self.brd[fr][self.col]) == '.':
                    tempallowed.append([fr,self.col])
                elif self.brd[fr][self.col].side != self.side:
                    tempallowed.append([fr,self.col])
                    break
                elif self.brd[fr][self.col].side == self.side:
                    break
        
        for ee in range(1,8):
            fc = self.col + ee
            if fc <= 7:
                if str(self.brd[self.row][fc]) == '.':
                    tempallowed.append([self.row,fc])
                elif self.brd[self.row][fc].side != self.side:
                    tempallowed.append([self.row,fc])
                    break
                elif self.brd[self.row][fc].side == self.side:
                    break
        
        for ww in range(1,8):
            fc = self.col - ww
            if fc >= 0:
                if str(self.brd[self.row][fc]) == '.':
                    tempallowed.append([self.row,fc])
                elif self.brd[self.row][fc].side != self.side:
                    tempallowed.append([self.row,fc])
                    break
                elif self.brd[self.row][fc].side == self.side:
                    break

        for ne in range(1,8):
            fr = self.row - ne
            fc = self.col + ne
            if fr >= 0 and fr <= 7 and fc >= 0 and fc <= 7:
                if str(self.brd[fr][fc]) == '.':
                    tempallowed.append([fr,fc])
                elif self.brd[fr][fc].side != self.side:
                    tempallowed.append([fr,fc])
                    break
                elif self.brd[fr][fc].side == self.side:
                    break
                
        for nw in range(1,8):
            fr = self.row - nw
            fc = self.col - nw
            if fr >= 0 and fr <= 7 and fc >= 0 and fc <= 7:
                if str(self.brd[fr][fc]) == '.':
                    tempallowed.append([fr,fc])
                elif self.brd[fr][fc].side != self.side:
                    tempallowed.append([fr,fc])
                    break
                elif self.brd[fr][fc].side == self.side:
                    break
                
        for se in range(1,8):
            fr = self.row + se
            fc = self.col + se
            if fr >= 0 and fr <= 7 and fc >= 0 and fc <= 7:
                if str(self.brd[fr][fc]) == '.':
                    tempallowed.append([fr,fc])
                elif self.brd[fr][fc].side != self.side:
                    tempallowed.append([fr,fc])
                    break
                elif self.brd[fr][fc].side == self.side:
                    break
                
        for sw in range(1,8):
            fr = self.row + sw
            fc = self.col - sw
            if fr >= 0 and fr <= 7 and fc >= 0 and fc <= 7:
                if str(self.brd[fr][fc])== '.':
                    tempallowed.append([fr,fc])
                elif self.brd[fr][fc].side != self.side:
                    tempallowed.append([fr,fc])
                    break
                elif self.brd[fr][fc].side == self.side:
                    break
        return tempallowed
            
class king:
    def __init__(self,row,col,side,brd):
        self.row = row
        self.col = col
        self.side = side
        self.brd = brd
    
    def __str__(self):
        if self.side == 'w':
            return str(Fore.CYAN + 'k')
        if self.side == 'b':
            return str(Style.BRIGHT + 'K')
    
    @property
    def allowed(self):
        tempallowed = list()
        for rr in [-1,0,1]:
            for cc in [-1,0,1]:
                if not (rr == 0 and cc == 0):
                    fr = self.row + rr
                    fc = self.col + cc
                    if fr >= 0 and fr <= 7 and fc >= 0 and fc <= 7:
                        if str(self.brd[fr][fc]) == '.' or self.brd[fr][fc].side != self.side:
                            tempallowed.append([fr,fc])
        return tempallowed
                    
def ischeck(brd,trn):
    for rr1 in range(8):
        for cc1 in range(8):
            if (brd[rr1][cc1].__class__ == king and brd[rr1][cc1].side == sidedict2[turn]):
                kr = rr1
                kc = cc1
                break
    for rr2 in range(8):
        for cc2 in range(8):
            if brd[rr2][cc2].side == sidedict2[(trn + 1) % 2]:
                oppallowed = brd[rr2][cc2].allowed
                for mm in range(len(oppallowed)):
                    if oppallowed[mm] == [kr,kc]:
                        return True
    return False

def removecheckmoves(ir,ic,trn,brd,am,cpt):
    tmpbrd = copy.deepcopy(brd)
    tmpmvs = copy.deepcopy(am)
    for mm in am:
        tr = int(mm[0])
        tc = int(mm[1])
        tmpbrd[tr][tc] = cpt(tr,tc,sidedict2[trn],tmpbrd)
        tmpbrd[ir][ic] = blank(ir,ic,'.')
        if ischeck(tmpbrd,trn) == True:
            tmpmvs.remove([tr,tc])
        tmpbrd = copy.deepcopy(brd)
    return tmpmvs

def ischeckmate(brd,trn):
    tmpbrd = copy.deepcopy(brd)
    if ischeck(brd,trn) == False:
        return False
    else:
        for rr in range(8):
            for cc in range(8):
                if brd[rr][cc].side == sidedict2[trn]:
                    temppiece = board[rr][cc]
                    temppiecetype = temppiece.__class__
                    tempallowed = temppiece.allowed
                    tempallowed = removecheckmoves(rr,cc,trn,tmpbrd,tempallowed,temppiecetype)
                    if len(tempallowed) > 0:
                        return False
    return True
    

def isstalemate(brd,trn):
    for rr in range(8):
        for cc in range(8):
            if brd[rr][cc].side == sidedict2[trn]:
                if len(brd[rr][cc].allowed) > 0:
                    return False
    return True

def issquareattacked(ar,ac,brd,atrn):
    # asking if the square at [ar,arc] is being attacked by the side in the argument
    for rr in range(8):
        for cc in range(8):
            if brd[rr][cc].side == sidedict2[atrn]:
                tempallowed = brd[rr][cc].allowed
                if ([ar,ac] in tempallowed) == True:
                    return True
    return False

def cancastle(brd,trn):
    othertrn = (turn + 1) % 2
    crow = castledict[trn]
    ks = True
    qs = True
    if ischeck(brd,trn) == True:
        ks = False
        qs = False
    if brd[crow][5].side != '.' or brd[crow][6].side != '.':
        ks = False
    if brd[crow][3].side != '.' or brd[crow][2].side != '.' or brd[crow][1].side != '.':
        qs = False
    if issquareattacked(crow,5,brd,othertrn) == True or issquareattacked(crow,6,brd,othertrn) == True:
        ks = False
    if issquareattacked(crow,3,brd,othertrn) == True or issquareattacked(crow,2,brd,othertrn) == True:
        qs = False
    return ks, qs

def initializeboard():
    brd = [[blank(rr,cc,'.') for rr in range(8)] for cc in range(8)]
    
    for cc in range(0,8):
        brd[1][cc] = pawn(1,cc,'b',brd)
        brd[6][cc] = pawn(6,cc,'w',brd)
    
    brd[0][0] = rook(0,0,'b',brd)
    brd[0][1] = knight(0,1,'b',brd)
    brd[0][2] = bishop(0,2,'b',brd)
    brd[0][3] = queen(0,3,'b',brd)
    brd[0][4] = king(0,4,'b',brd)
    brd[0][5] = bishop(0,5,'b',brd)
    brd[0][6] = knight(0,6,'b',brd)
    brd[0][7] = rook(0,7,'b',brd)
    brd[7][0] = rook(7,0,'w',brd)
    brd[7][1] = knight(7,1,'w',brd)
    brd[7][2] = bishop(7,2,'w',brd)
    brd[7][3] = queen(7,3,'w',brd)
    brd[7][4] = king(7,4,'w',brd)
    brd[7][5] = bishop(7,5,'w',brd)
    brd[7][6] = knight(7,6,'w',brd)
    brd[7][7] = rook(7,7,'w',brd)
    
    return brd

def initializesparseboard():
    # board must be initialized with both kings present
    brd = [[blank(rr,cc,'.') for rr in range(8)] for cc in range(8)]

    brd[0][0] = rook(0,0,'b',brd)
    brd[0][4] = king(0,4,'b',brd)
    brd[0][7] = rook(0,7,'b',brd)
    brd[1][3] = pawn(1,3,'b',brd)
    
    brd[6][2] = pawn(6,2,'w',brd)
    brd[7][0] = rook(7,0,'w',brd)
    brd[7][4] = king(7,4,'w',brd)
    brd[7][7] = rook(7,7,'w',brd)
    return brd

def displayboard(brd):
    rnk = 8
    for row in brd:
        print(Fore.WHITE + Back.RED + Style.BRIGHT + str(rnk) + Style.RESET_ALL +  ' ' + ' '.join([str(elem) for elem in row]))
        rnk -= 1
    print('  ' + Fore.WHITE + Back.RED + Style.BRIGHT + ' '.join([str(file) for file in files]))

def displayjustboard(brd):
    for rnk in brd:
        print(' '.join([str(elem) for elem in rnk]))

###############################################################################
# start main code

ranks = ['1','2','3','4','5','6','7','8']
files = ['a','b','c','d','e','f','g','h']
rankdict = {'8':0, '7':1, '6':2, '5':3, '4':4, '3':5, '2':6, '1':7}
filedict = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
rankinv = {vv: kk for kk, vv in rankdict.items()}
fileinv = {vv: kk for kk, vv in filedict.items()}

sidedict1 = {0:'White', 1:'Black'}
sidedict2 = {0:'w', 1:'b'}
turn = 0

numturns = 0
movelog = list()

castledict = {0:7, 1:0}
kinghasmoved = [False, False]
rookhasmoved = [[False, False], [False, False]] # [king-side, queen-side]

canenpassant = False
enpassantmove = [0,0]

print('\nWelcome to chess\n')
board = initializeboard()
displayboard(board)
print(Style.RESET_ALL + '\n=================')

irow = 0
icol = 0
irank = 0
ifile = 0
frow = 0
fcol = 0
frank = 0
ffile = 0

print('Enter moves by rank (row, a number 1-8) and file (column, a letter a-h), separated by a space')

while True:
    if ischeckmate(board,turn) == True:
        print('Checkmate,', sidedict1[(turn + 1) % 2], 'wins')
        raise SystemExit
    if isstalemate(board,turn) == True and ischeck(board,turn) == False:
        print('Stalemate')
        raise SystemExit
        
    while True:
        print('\n     ' + sidedict1[turn] + '\'s turn')
        if ischeck(board,turn) == True:
            print('Currently in check')
        
        while True:
            try:
                irank,ifile = input('What piece do you want to move? ').split()
            except:
                print('Bad input')
                continue
            else:
                break
        if (irank not in ranks) or (ifile not in files):
            print('Bad input')
            continue
        else:
            irow = rankdict[irank]
            icol = filedict[ifile]
            castlerow = castledict[turn]
            chosenpiece = board[irow][icol]
            chosenpiecetype = chosenpiece.__class__
            if str(chosenpiece) == '.':
                print('Space is empty')
                continue
            elif chosenpiece.side != sidedict2[turn]:
                print('Wrong side')
                continue            
            allowedmoves = list(chosenpiece.allowed)
            allowedmoves = removecheckmoves(irow,icol,turn,board,allowedmoves,chosenpiecetype)
            
            if kinghasmoved[turn] == False and chosenpiecetype == king:
                if rookhasmoved[turn][0] == False and cancastle(board,turn)[0] == True:
                    allowedmoves.append([castlerow,6])
                if rookhasmoved[turn][1] == False and cancastle(board,turn)[1] == True:
                    allowedmoves.append([castlerow,2])
            
            if chosenpiecetype == pawn and canenpassant == True and abs(fcol - icol) == 1 and frow == irow:
                if turn == 0:
                    allowedmoves.append([2,fcol])
                    enpassantmove = [2,fcol]
                if turn == 1:
                    allowedmoves.append([5,fcol])
                    enpassantmove = [5,fcol]
                        
            if len(allowedmoves) == 0:
                print('This piece has no legal moves')
                continue
            break
        canenpassant = False
    
    while True:
        print('\nAllowed moves: ')
        for aa in range(len(allowedmoves)):
            print(rankinv[allowedmoves[aa][0]],fileinv[allowedmoves[aa][1]])
        
        while True:
            try:
                frank,ffile = input('Where do you want to move? (enter "0 0" to move a different piece): ').split()
            except:
                print('Bad input')
                continue
            else:
                break
        if frank == '0' and ffile == '0':
            turn = (turn + 1) % 2
            break
        elif (irank not in ranks) or (ifile not in files):
            print('Bad input')
            continue
        else:
            frow = rankdict[frank]
            fcol = filedict[ffile]
            chosendestination = board[frow][fcol]            
            if chosenpiece.side == chosendestination.side:
                print('Can\'t move to a spot you already control')
                continue
            elif [frow,fcol] not in allowedmoves:
                print('Not an allowed move')
                continue
            else:
                if str(chosendestination) == '.' or str(chosendestination.side) != sidedict2[turn]:
                    board[frow][fcol] = chosenpiecetype(frow,fcol,sidedict2[turn],board)
                    board[irow][icol] = blank(irow,icol,'.')
                    
                    if chosenpiecetype == pawn:
                        if board[frow][fcol].ispawnexchange() == True:
                            board = board[frow][fcol].pawnexchange()
                        if abs(frow - irow) == 2:
                            canenpassant = True
                        if abs(frow - irow) == 1 and abs(fcol - icol) == 1 and enpassantmove == [frow,fcol]:
                            if turn == 0:
                                board[3][fcol] = blank(3,fcol,'.')
                            if turn == 1:
                                board[4][fcol] = blank(4,fcol,'.')
                                                    
                    if chosenpiecetype == king:
                        if fcol - icol == 2:
                            board[castlerow][5] = rook(castlerow,5,sidedict2[turn],board)
                            board[castlerow][7] = blank(castlerow,7,'.')
                        elif fcol - icol == -2:
                            board[castlerow][3] = rook(castlerow,3,sidedict2[turn],board)
                            board[castlerow][0] = blank(castlerow,0,'.')
                    
                    print('\n')
                    displayboard(board)
                    print(Style.RESET_ALL + '\n=================')
                    
                    if chosenpiecetype == king:
                        kinghasmoved[turn] = True
                    if chosenpiecetype == rook:
                        if icol == 7: rookhasmoved[turn][0] = True
                        if icol == 0: rookhasmoved[turn][1] = True
                    break                
    turn = (turn + 1) % 2
    enpassantmove = [0,0]
    movelog.append([[irank,ifile],[frank,ffile]])
    numturns += 1