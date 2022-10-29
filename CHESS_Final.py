
import pygame
import keyboard
import random
import time
import turtle
import random
from pygame import mixer
import copy
import os
pygame.init()
opp = {
    "white" : "black",
    "black" : "white"
    
}
piecelist = {
    "wking" : pygame.transform.scale( pygame.image.load(os.getcwd() + "\whiteKing.png"),(107,107)),
    "wbishop" : pygame.transform.scale( pygame.image.load(os.getcwd() + "\whiteBishop.png"),(107,107)),
    "wrook" : pygame.transform.scale( pygame.image.load(os.getcwd() + "\whiteRook.png"),(107,107)),
    "wpawn" : pygame.transform.scale( pygame.image.load(os.getcwd() + "\whitePawn.png"),(107,107)),
    "wqueen" : pygame.transform.scale( pygame.image.load(os.getcwd() + "\whiteQueen.png"),(107,107)),
    "wknight": pygame.transform.scale( pygame.image.load(os.getcwd() + "\whiteKnight.png"),(107,107)),
    "bking" : pygame.transform.scale( pygame.image.load(os.getcwd() + "\\blackKing.png"),(107,107)),
    "bbishop" : pygame.transform.scale( pygame.image.load(os.getcwd() + "\\blackBishop.png"),(107,107)),
    "brook" : pygame.transform.scale( pygame.image.load(os.getcwd() + "\\blackRook.png"),(107,107)),
    "bpawn" : pygame.transform.scale( pygame.image.load(os.getcwd() + "\\blackPawn.png"),(107,107)),
    "bqueen" : pygame.transform.scale( pygame.image.load(os.getcwd() + "\\blackQueen.png"),(107,107)),
    "bknight": pygame.transform.scale( pygame.image.load(os.getcwd() + "\\blackKnight.png"),(107,107))
}
def convert(x):
    if x < 0:
        return 1
    elif x > 0:
        return -1
    else:
        return 0
class Visual:
    def __init__(self):
        self.screen = pygame.display.set_mode((900,900))
        self.font = pygame.font.SysFont(None, 70)  
        self.winner = [False,"none"]
        pygame.display.set_caption("Chess Mf")
        self.screen.fill((255,255,255))
        self.rowid=[['a', (33, 140)], ['b', (140, 247)], ['c', (247, 354)], ['d', (354, 461)], ['e', (461, 568)], ['f', (568, 675)], ['g', (675, 782)], ['h', (782, 889)]]
        self.colid= [['8', (12, 119)], ['7', (118, 225)], ['6', (224, 331)], ['5', (330, 437)], ['4', (436, 543)], ['3', (542, 649)], ['2', (648, 755)], ['1', (754, 861)]]
        self.letterlist = ["a","b","c","d","e","f","g","h"]
        self.cursor = pygame.transform.scale( pygame.image.load(os.getcwd() + '/blue_rect.png'),(107,107))
        self.boardimg = pygame.transform.scale( pygame.image.load(os.getcwd() + '/CHESSBOARD.png'), (900,900))
        pygame.display.update()
        #Key is a,1 pos is 335,443 and rowcol is 7,0
    def convert_fromkey_toCoord(self,key):
        letter = key[0] 
        number = key[1]
        xpos = None
        ypos = None
        for i in range(0,8):
            if  letter == self.rowid[i][0]:
                xpos = self.rowid[i][1][0] 
            if number == self.colid[i][0]:
                ypos = self.colid[i][1][0]
        return ([xpos,ypos])
        
    def convert_tokey_fromCoord(self,pos):
        xpos = pos[0] 
        ypos = pos[1] 
        letter = None
        number = None
        for i in range(0,8):
            if self.rowid[i][1][0] < xpos and self.rowid[i][1][1] > xpos :
                letter = self.rowid[i][0]
            if self.colid[i][1][0] < ypos and self.rowid[i][1][1] > ypos :
                number = self.colid[i][0]
        if letter != None and number != None:
            return [letter,number]
        else :
            return False
    
    def convert_index_tokey(self,rowcol):
        letter = self.letterlist[rowcol[1]]
        num = str(8 - rowcol[0])
        return([letter,num])
        
    def convert_key_toindex(self,key):
        col = self.letterlist.index(key[0])
        row = abs(int(key[1]) - 8)

        return([row,col])
    def blit_alpha(self, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(self.screen, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        self.screen.blit(temp, location)
    def drawboard(self,board,cursorindex = (0,0)):
        self.screen.fill((255,255,255))
        self.screen.blit(self.boardimg, (0, 0))
        for row in range(0,8):
            for col in range(0,8):
                index = [row,col]
                img = piecelist.get(list(getattr(board[row][col],"color"))[0] + getattr(board[row][col],"rank"))
                if img != None:
                    key = self.convert_index_tokey(index)
                    coord = self.convert_fromkey_toCoord(key)
                    self.screen.blit(img, (coord[0],coord[1]))
        key = self.convert_tokey_fromCoord(cursorindex)
        if key == False:
            print("invalid position")
        else:
            coord = self.convert_fromkey_toCoord(key)
            self.blit_alpha(self.cursor,(coord[0],coord[1]),120) 
        
        if self.winner[0]:
            pygame.image.save(self.screen,"screenshot.jpg")
            finalboardstate = pygame.transform.scale(pygame.image.load(os.getcwd() + "\screenshot.jpg"),(600,600))
            self.screen.fill((0,0,0))
            self.screen.blit(finalboardstate, (100,100))

            if self.winner[1] != "tie":
                print("Congrats")
                #pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(90, 640, 780, 100))
                img1 = self.font.render('Congratulations ' + self.winner[1] + "!!!", True, (0,0,255))
                self.screen.blit(img1,(100,800))
            else:
                print("Congrats")
                #pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(90, 640, 780, 100))
                img1 = self.font.render('Congratulations on choking', True, (0,0,255))
                self.screen.blit(img1,(100,800))
        
    def validcursor(self,clickpos):
        key = self.convert_tokey_fromCoord(clickpos)
        if key == False:
            print("invalid position")
            return False
        else:
            
            return self.convert_key_toindex(key)
    def changetitle(self,string):
        pygame.display.set_caption(string)
    def endscreen(self,winner):
        self.winner[0] = True
        self.winner[1] = winner
        

class Game:
    def __init__(self,visual,board):
        self.visual = visual
        self.board = board
        self.visual.drawboard(self.board)
        self.running = True
        self.selected = False
        self.selectedpeice = ''
        self.turn = "white"
        self.cursorpos = [0,0]
        self.currentking = ''
        self.attackingpeices = []
        self.teammates = []
        self.kinghasmoves = False
    def listener(self):
        while self.running:
            for event in pygame.event.get() :
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_x, mouse_y = event.pos
                        print(mouse_x,mouse_y)
                        self.cursorpos = [mouse_x,mouse_y]
                        self.visual.drawboard(self.board,self.cursorpos)
                        index = self.visual.validcursor([mouse_x,mouse_y])
                        self.recieveinput(index)
            pygame.display.update()
    def incrementturn(self):
        tags = ["king","empty"]
        self.turn = opp.get(self.turn)
        self.findteammates()
        if self.ismate():
            self.visual.endscreen(opp.get(self.turn))
        else:
            onlykings = True
            
            if len(self.teammates) == 0:
                for i in range(0,8):
                    for j in range(0,8):
                        if getattr(self.board[i][j],"rank") not in tags:
                            print(getattr(board[i][j],"rank"))
                            onlykings = False
                print(onlykings)
            else:
                onlykings = False

            if onlykings:
                self.visual.endscreen("tie")


            if not self.kinghasmoves and not self.incheck():
                if self.isstale():
                    self.visual.endscreen("tie")


            


        
    def resetboard(self,board):
        self.board = board
        self.visboard()
    def visboard(self):
            strboar = []
            for i in range(0,8):
                strboar.append([])
                for b in range(0,8):
                    if getattr(self.board[i][b],"color") == getattr(self.board[i][b],"rank"):
                        name = "_____"
                        
                    else:
                        name = list(getattr(self.board[i][b],"color"))[0] + getattr(self.board[i][b],"rank")
                    strboar[i].append(name.center(8)) 
            for i in strboar:
                print(i)
    def peicebetween(self,point1,point2):
        if( abs(point1[0]-point2[0]) == abs(point1[1]-point2[1]) or (point1[0]-point2[0] == 0 and point1[1]-point2[1]  != 0) or (point1[0]-point2[0]  != 0 and point1[1]-point2[1]  == 0) ):
            ystep = convert(point1[0] - point2[0])
            xstep = convert(point1[1] - point2[1])
            checkpoint = [point1[0],point1[1]]
            checkpoint[0] += ystep
            checkpoint[1] += xstep
            while checkpoint != list(point2):
                if getattr(self.board[checkpoint[0]][checkpoint[1]],"color") != "empty":
                    return True
                checkpoint[0] += ystep
                checkpoint[1] += xstep
            return False
        else:
            return False
    def getpeice(self,pos):
        return self.board[pos[0]][pos[1]]
    def squaresbetweenandincluding(self,point1,point2):
        squareslist = []
        ystep = convert(point1[0] - point2[0])
        xstep = convert(point1[1] - point2[1])
        checkpoint = [point1[0],point1[1]]
        while checkpoint != list(point2):
            squareslist.append(copy.copy(checkpoint))           
            checkpoint[0] += ystep
            checkpoint[1] += xstep
        return squareslist
    def isstale(self):

        for i in self.teammates:
            movesetpeices = ["knight","pawn"]
            moveset = []
            pos = getattr(i,"pos")
            if getattr(i,"rank") in movesetpeices:
                moveset = getattr(i,"moveset")   
            else:
                moveset = [(0,1),(1,0),(1,1),(-1,-1),(0,-1),(-1,0),(1,-1),(-1,1)] 
            print(moveset)
            print("^^^ " + getattr(i,"rank"))
            for n in moveset:
                    if pos[0]+n[0] in range(0,8) and pos[1]+n[1] in range(0,8):
                        pos2 = (pos[0]+n[0],pos[1]+n[1])
                        objonmovepath = self.getpeice(pos2)
                        if i.Moveworks(objonmovepath,True):
                            if self.movepeiceto(i,pos,pos2,True):
                                print("NO KING MOVE, HAS MOVES with " + (getattr(i,"rank")))
                                return False
        print("TIE GAME !")
        return True
    def recieveinput(self,index):
         if index != False:
            if self.selected == False:
                if getattr(self.board[index[0]][index[1]],"color") == self.turn:
                    self.selected = True
                    self.selectedpeice = self.board[index[0]][index[1]]
                    print("selected " + getattr(self.board[index[0]][index[1]],"color") + " " +getattr(self.board[index[0]][index[1]],"rank"))
                    print("it is " + self.turn + "'s turn")
            else :
                # needs to check here if is in check
                if self.selectedpeice.Moveworks(self.board[index[0]][index[1]],True):
                    if self.selectedpeice.Moveworks(self.board[index[0]][index[1]]):
                        self.incrementturn()
                        self.visual.changetitle("it is " + self.turn + "'s turn")
                self.selected = False
                
            self.visual.drawboard(self.board,self.cursorpos)

    def incheck(self):
        opppieces = []
        attackingpieces = []
        self.attackingpeices = []
        print("---------------------")
        self.visboard()
        print("---------------------")
        for i in range(0,8):
            for j in range(0,8):
                if opp.get(getattr(self.board[i][j],"color")) == self.turn:
                    opppieces.append(self.board[i][j])
                elif getattr(self.board[i][j],"rank") == "king":
                    kingobj = self.board[i][j]
                    self.currentking = kingobj
                
        print(getattr(kingobj,"pos"))
        for i in opppieces:
            if i.Moveworks(kingobj,True):
                attackingpieces.append(i)
                print(self.turn + " is in check" + "by " + getattr(i,"rank"))
        self.attackingpeices = attackingpieces
        if len(attackingpieces) > 0 : 
            return True
        else:
            return False
        
            
    def movepeiceto(self,object1,pos1,pos2,test=False):
        tempboard = copy.deepcopy(self.board)
        setattr(object1,"pos",pos2)
        self.board[pos1[0]][pos1[1]] = empty(pos1)
        self.board[pos2[0]][pos2[1]] = object1
        incheckvar = self.incheck()
        if incheckvar or test:
            self.board = tempboard
        if test:
            return not incheckvar
        if self.board == tempboard:
            return False
        else :
            return True 
    def ismate(self):
        # Two ways to leave check, move out of check or move to intercept
        #king movement logic :
            # pos - possiblemove == empty, movepieceto and record the result in a list
        incheckvar = self.incheck()
        emptysquares = []
        moveset = getattr(self.currentking,"moveset")
        kingpos = getattr(self.currentking,"pos")
        canblock = []
        # King move logic <<<<<    
        for i in moveset:
            if (kingpos[0] + i[0] in range(0,8) and kingpos[1] + i[1] in range(0,8)) and getattr(self.board[kingpos[0] + i[0]][kingpos[1]+i[1]],"color") != self.turn :
                emptysquares.append((kingpos[0] + i[0],kingpos[1]+i[1]))
        for i in emptysquares:
            #check if moving to this square is legal?
            if self.movepeiceto(self.currentking,kingpos,i,True):
                print("King has a square to move")
                self.kinghasmoves = True
                return False
        self.kinghasmoves = False
        print("No fucking legal squares, these can block")
        if incheckvar:
            print("currently in check, do I have empty squares around me?") 
            if len(self.attackingpeices) == 1:
                #intercept logic, find the squares between the peice and the king. 
                print("only one checker")
                for i in self.attackingpeices:
                    print(getattr(i,"pos"))
                    for teammate in self.teammates: 
                        for j in self.squaresbetweenandincluding(getattr(i,"pos"),kingpos):
                            #j is the squares a peice can move to to block
                            if teammate.Moveworks(self.board[j[0]][j[1]],True):
                                print(getattr(teammate,"rank"))
                                print("teammate can block")
                                canblock.append(teammate)
                            
            print(canblock)
            if len(canblock) == 0:
                print("OH NO YOU GOT MATED HAHA BITCH")
                return True
            else :
                return False

    def findteammates(self):
        self.teammates = []
        for i in range(0,8):
            for j in range(0,8):
                if getattr(self.board[i][j],"color") == self.turn and getattr(self.board[i][j],"rank") != "king":
                    self.teammates.append(self.board[i][j])
            
            

   

class empty:
    def __init__(self,pos):
        # Will be "black" or "white"
        self.color = "empty"
        self.pieceimg = None
        self.pos = pos
        self.rank = "empty"
class piece:
    def __init__(self,color,pos,rank):
        # Will be "black" or "white"
        self.color = color
        self.rank = rank
        self.pos = pos     
    def movepiece(self,targetobj):
        return game.movepeiceto(self,self.pos,getattr(targetobj,"pos"))
class king(piece):
    def __init__(self,color,pos):
        super().__init__(color,pos,"king")
        self.moveset = [(0,1),(1,0),(1,1),(-1,-1),(0,-1),(-1,0),(1,-1),(-1,1)] 
    def Moveworks(self,targetobj,test=False):
        if getattr(targetobj,"color") != self.color:
            targetsquare = getattr(targetobj,'pos')
            
            for i in range(len(self.moveset)):
                if (targetsquare[0]-self.pos[0]) == self.moveset[i][0] and (targetsquare[1]-self.pos[1]) == self.moveset[i][1]:
                    if not test:
                        return self.movepiece(targetobj)
                    else:
                        return True 
            return False     
    

    
class pawn(piece):
    def __init__(self,color,pos):
        super().__init__(color,pos,"pawn")
        self.mult = -1
        if self.color == "black":
            self.mult = 1
        self.moveset = [(1,0)]

    def Moveworks(self,targetobj,test=False):
        targetsquare = getattr(targetobj,'pos')
        if not game.peicebetween(self.pos,targetsquare) and getattr(targetobj,"color") != self.color:
            if targetobj.color == opp.get(self.color):
                self.moveset.pop()
                self.moveset.append((1,1))
                self.moveset.append((1,-1))
            elif (self.color == "white" and self.pos[0] == 6) or (self.color == "black" and self.pos[0] == 1) :
                self.moveset.append((2,0))
            
            for i in range(len(self.moveset)):
                    if (targetsquare[0] - self.pos[0]) * self.mult == self.moveset[i][0] and  (targetsquare[1] - self.pos[1]) * self.mult == self.moveset[i][1]:
                        print("works")
                        if not test:
                            return self.movepiece(targetobj)
                        else:
                            self.moveset = [(1,0)]
                            return True 
            self.moveset = [(1,0)]            
            return False
    def movepiece(self,targetobj):
        new_height = getattr(targetobj,"pos")[0]
        if (new_height == 0 and self.color == "white") or (new_height==7 and self.color == "black"):
            newqueen = queen(self.color,self.pos)
            print("Make a queen here")
            return game.movepeiceto(newqueen,self.pos,getattr(targetobj,"pos"))
        else :
            return game.movepeiceto(self,self.pos,getattr(targetobj,"pos"))        
class rook(piece):
    def __init__(self,color,pos):
        super().__init__(color,pos,"rook")
    def Moveworks(self,targetobj,test=False):
        targetsquare = getattr(targetobj,'pos')
        if getattr(targetobj,"color") != self.color and not game.peicebetween(self.pos,targetsquare):
            targetsquare = getattr(targetobj,'pos')
            
            if (targetsquare[0]-self.pos[0] == 0 and targetsquare[1]-self.pos[1]  != 0) or (targetsquare[0]-self.pos[0]  != 0 and targetsquare[1]-self.pos[1]  == 0):
                    if not test:
                        return self.movepiece(targetobj)
                    else:
                        return True 
        return False   
class bishop(piece):
    def __init__(self,color,pos):
        super().__init__(color,pos,"bishop")
    def Moveworks(self,targetobj,test=False):
        targetsquare = getattr(targetobj,'pos')
        if getattr(targetobj,"color") != self.color and not game.peicebetween(self.pos,targetsquare):
            targetsquare = getattr(targetobj,'pos')
            if(abs(targetsquare[0]-self.pos[0]) == abs(targetsquare[1]-self.pos[1])):
                    if not test:
                        return self.movepiece(targetobj)
                    else:
                        return True 
        return False   
class queen(piece):
    def __init__(self,color,pos):
        super().__init__(color,pos,"queen")
    def Moveworks(self,targetobj,test=False):
        targetsquare = getattr(targetobj,'pos')

        if getattr(targetobj,"color") != self.color and not game.peicebetween(self.pos,targetsquare):
            targetsquare = getattr(targetobj,'pos')
            if( abs(targetsquare[0]-self.pos[0]) == abs(targetsquare[1]-self.pos[1]) or (targetsquare[0]-self.pos[0] == 0 and targetsquare[1]-self.pos[1]  != 0) or (targetsquare[0]-self.pos[0]  != 0 and targetsquare[1]-self.pos[1]  == 0) ):
                    if not test:
                        return self.movepiece(targetobj)
                    else:
                        return True 
        
        return False   
class knight(piece):
    def __init__(self,color,pos):
        super().__init__(color,pos,"knight")
        self.moveset = [(2,1),(1,2),(-1,-2),(-2,-1),(1,-2),(-2,1),(2,-1),(-1,2)]
    def Moveworks(self,targetobj,test=False):
        if getattr(targetobj,"color") != self.color:
            targetsquare = getattr(targetobj,'pos')
            for i in range(len(self.moveset)):
                if (targetsquare[0]-self.pos[0]) == self.moveset[i][0] and (targetsquare[1]-self.pos[1]) == self.moveset[i][1]:
                    if not test:
                        return self.movepiece(targetobj)
                    else:
                        return True 
                
        return False   






board = []
frontrow = [pawn,pawn,pawn,pawn,pawn,pawn,pawn,pawn]
#frontrow = [empty,empty,empty,empty,empty,empty,empty,empty]
#backrow = [empty,king,empty,empty,empty,empty,empty,queen]
backrow = [rook,knight,bishop,queen,king,bishop,knight,rook]

nopawn = True
whitepawnrow = []
blackpawnrow = []
whitepiecerow = []
blackpiecerow = []

for i in range(0,8):
    if frontrow[i] == empty:
        whitepawnrow.append(empty((6,i)))
        blackpawnrow.append(empty((1,i)))
    else:
        whitepawnrow.append(frontrow[i]("white",(6,i)))
        blackpawnrow.append(frontrow[i]("black",(1,i)))
    if backrow[i] == empty:
        whitepiecerow.append(backrow[i]([7,i]))
        blackpiecerow.append(backrow[i]([0,i]))
    else:
        whitepiecerow.append(backrow[i]("white",[7,i]))
        blackpiecerow.append(backrow[i]("black",[0,i]))

for i in range (0,8):
    board.append([])
    for j in range(0,8):
        board[i].append(empty([i,j]))
board[0] = blackpiecerow
board[1] = blackpawnrow
board[6] = whitepawnrow
board[7] = whitepiecerow

for i in board :
    print(i)



creator = Visual()
game = Game(creator,board)
game.listener()





#BUGS Im going to kill myself if there are any more bugs
