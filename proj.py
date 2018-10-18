import copy
import search
import utils
from search import *
from utils import *

#================================================================
#   Functions to manipulate or consult board
#================================================================
#TAI space
#Peg
def c_peg ():
    return "O"
#Empty Space
def c_empty ():
    return "_"
#Interdite Space
def c_blocked ():
    return "X"
#If space is empty returns True
def is_empty (e):
    return e == c_empty()
#If space has a peg returns True
def is_peg (e):
    return e == c_peg()
#If space is blocked returns True
def is_blocked (e):
    return e == c_blocked()

# TAI pos
# Tuplo (l, c)
def make_pos (l, c):
    return (l, c)
#Line from position
def pos_l (pos):
    return pos[0]
#collumn from position
def pos_c (pos):
    return pos[1]

# TAI move
# Lista [p_initial, p_final]
def make_move (i,f):
    return [i,f]
#Beginning position
def move_initial (move):
    return move[0]
#Final position
def move_final (move):
    return move[1]

#Number of lines of table
def linhastab(tab):
    return len(tab)
#Number of collumns of table
def colunastab(tab):
    return len(tab[0])

#Element of table on that position
def cor(tab,pos):
    linha = pos_l(pos)
    coluna = pos_c(pos)
    return tab[linha][coluna]

#Returns True if that position in inside the range of table (CORRIGIR ACHO QUE ESTÁ MAL)
def lista(tab,pos):
    for i in tab:
        if i == pos:
            return True
    return False

def grupo(final,group):
    for i in final:
        if len(i) == 1:
            if i == group:
                return True
        if isinstance(i,list):
            for j in i:
                if j == group:
                    return True
        else:
            if i == group:
                return True

    if len(group) >= 1:
        group = group[0]
    return False

def possiveisgruposlinhas(tab, pos, group):


    linha = pos_l(pos)
    coluna = pos_c(pos)

    if ((coluna < 0 or linha < 0) or linha > linhastab(tab)-1 or coluna > colunastab(tab)-1):
        return

    #procuraesquerda
    colunacomp=coluna -2
    linhacomp=linha
    if (colunacomp >= 0 and linhacomp >= 0):
        if(linhacomp < linhastab(tab) and colunacomp < colunastab(tab)):
            poscomp= make_pos(linhacomp, colunacomp)
            posmeio= make_pos(linhacomp, colunacomp+1)
            if(lista(group,poscomp) == False and is_peg(cor(tab,pos)) and is_peg(cor(tab, posmeio)) and is_empty(cor(tab, poscomp))):
                group = [group + [poscomp]]
                possiveisgruposlinhas(tab, poscomp, group)


    #procuradireita
    colunacomp = coluna +2
    linhacomp=linha
    if (colunacomp >= 0 and linhacomp >= 0):
        if(linhacomp < linhastab(tab) and colunacomp < colunastab(tab)):
            poscomp= make_pos(linhacomp, colunacomp)
            posmeio= make_pos(linhacomp, colunacomp-1)
            if(lista(group,poscomp) == False and is_peg(cor(tab, pos)) and is_peg(cor(tab, posmeio)) and is_empty(cor(tab, poscomp))):
                    group = group + [[pos,poscomp]]
                    possiveisgruposlinhas(tab, poscomp, group)

    #procurabaixo
    linhacomp= linha + 2
    colunacomp=coluna
    if (colunacomp >= 0 and linhacomp >= 0):
        if(linhacomp < linhastab(tab) and colunacomp < colunastab(tab)):
            poscomp= make_pos(linhacomp, colunacomp)
            posmeio= make_pos(linhacomp -1, colunacomp)
            if(lista(group,poscomp) == False and is_peg(cor(tab, pos)) and is_peg(cor(tab, posmeio)) and is_empty(cor(tab, poscomp))):
                #print (group)
                #print("gordo")
                if(lista(group,pos) == True):
                    #print ("hallo")
                    group = [group + [poscomp]]
                    possiveisgruposlinhas(tab, poscomp, group)
                else:
                    #print("noiceee")
                    group = group + [[pos, poscomp]]
                    possiveisgruposlinhas(tab, poscomp, group)


    #procuracima
    linhacomp=linha-2
    colunacomp=coluna
    if (colunacomp >= 0 and linhacomp >= 0):
        if(linhacomp < linhastab(tab) and colunacomp < colunastab(tab)):
            poscomp= make_pos(linhacomp, colunacomp)
            posmeio= make_pos(linhacomp+1, colunacomp)
            if(lista(group,poscomp) == False and is_peg(cor(tab, posmeio)) and is_peg(cor(tab, pos)) and is_empty(cor(tab, poscomp))):
                group = [group + [poscomp]]
                possiveisgruposlinhas(tab, poscomp, group)
                #print("gordo4")

    return group

def checksize(group):
    for i in range(0,len(group)):
            if(len(group[i]) == 2 and isinstance(group[i], tuple)==False):
                #print(group[i])
                #print("AQUIII")
                return False

def board_moves(tab):
    final = []
    for i in range(0,linhastab(tab)):
        for j in range(0,colunastab(tab)):
            pos = make_pos(i,j)
            if(cor(tab,pos) != 0):
                group = [pos]
                group = possiveisgruposlinhas(tab,pos,group)
                if grupo(final,group) == False and checksize(group) == False:
                    #print("entrei")
                    final += group

    return final

def board_perform_move(tab, move):
    res = []
    res = copy.deepcopy(tab)
    initial_pos = move_initial(move)
    final_pos = move_final(move)

    if(pos_l(initial_pos) == pos_l(final_pos) and pos_c(initial_pos) != pos_c(final_pos)):
        res[pos_l(initial_pos)][pos_c(initial_pos)] = '_'

        if(pos_c(initial_pos) > pos_c(final_pos)):
            res[pos_l(initial_pos)][pos_c(initial_pos) - 1] = '_'
            res[pos_l(initial_pos)][pos_c(final_pos)] = 'O'

        elif(pos_c(initial_pos) < pos_c(final_pos)):
            res[pos_l(initial_pos)][pos_c(initial_pos) + 1] = '_'
            res[pos_l(initial_pos)][pos_c(final_pos)] = 'O'

    elif(pos_l(initial_pos) != pos_l(final_pos) and pos_c(initial_pos) == pos_c(final_pos)):
        if(pos_l(initial_pos) > pos_l(final_pos)):
            res[pos_c(initial_pos)][pos_l(initial_pos) - 1] = '_'
            res[pos_c(initial_pos)][pos_l(final_pos)] = 'O'

        elif(pos_l(initial_pos) < pos_l(final_pos)):
            res[pos_c(initial_pos)][pos_l(initial_pos) + 1] = '_'
            res[pos_c(initial_pos)][pos_l(final_pos)] = 'O'


    return res

class sol_state:
    def __init__(self,board):
        self.board = board

    def actions_aux(self): #idk
        find = board_moves(self.board)
        actions = []
        for i in find:
            if len(i) > 1:
                actions += [i]
        return actions

    def act_size(self):
        return len(self.actions_aux())

    def __lt__(self,other_state):
        return self.act_size()  > other_state.act_size()

    def test(self):
        for i in range(0,linhastab(self.board)):
            for j in range(0,colunastab(self.board)):
                pos = make_pos(i,j)
                if is_empty(cor(self.board,pos)) == False:
                    return False
        return True

    def result_aux(self,action):
        r = board_perform_move(self.board,action)
        return sol_state(r)


class solitaire(Problem):

    def __init__(self, board):
        self.initial = sol_state(board)

    def actions(self, state):
        return state.actions_aux()

    def result(self, state, action):
        return state.result_aux(action)

    def goal_test(self, state):
        return state.test()

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def h(self, node):
        acth = board_moves(node.state.board)
        return len(acth)

def greedy_search(solitaire):
        return best_first_graph_search(solitaire, solitaire.h)


'''
- Procura em largura primeiro não deve ser usada aqui, para problemas simples vai resultar, mas para problemas mais complexos não irá funcionar.
- Procura em profundidade é preferível, pois já sabemos que o máximo de profundidade que a árvore vai ter é N, sendo N o número de peças.
- Qual é uma heurística boa para conseguir encontrar a solução otima??? Por exemplo, se a heuristica for ter uma peça a menos em cada jogada, não é uma
heurística, uma vez que em cada jogada é sempre retirada uma peça independentemente de ser uma jogada boa ou má...
- Para motivos do relatório, podemos ter várias heurísticas para podermos experimentar.

game = Solitaire(board)
p = InstrumentedProblem(game)
result = depth_first_search(p)
result = greedy_best_first_graph_search(p, p.h -> h é a heurística)
result = astar.search(p, p.h -> não é obrigatório, mas podemos ter uma heurística diferente da que está implementada na função)
'''
