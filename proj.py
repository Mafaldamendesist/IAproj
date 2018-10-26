# Group 23 86473 Margarida Parrado Morais 83502 Mafalda Joana Catita Neves Ferreira Mendes

from search import *
from utils import *
import copy

#TAI content
def c_peg ():
    return "O"
def c_empty ():
    return "_"
def c_blocked ():
    return "X"
def is_empty (e):
    return e == c_empty()
def is_peg (e):
    return e == c_peg()
def is_blocked (e):
    return e == c_blocked()

# TAI pos
# Tuple (line, collumn)
def make_pos (l, c):
    return (l, c)
def pos_l (pos):
    return pos[0]
def pos_c (pos):
    return pos[1]

# TAI move
# List [pos_initial, pos_final]
def make_move (i,f):
    return [i,f]
def move_initial (move):
    return move[0]
def move_final (move):
    return move[1]

#board height
def linhastab(tab):
    return len(tab)
#board width
def colunastab(tab):
    return len(tab[0])

#existing content in this position
def content(tab,pos):
    linha = pos_l(pos)
    coluna = pos_c(pos)
    return tab[linha][coluna]

#AuxFunction to check if pos is in tab
def lista(tab,pos):
    for i in tab:
        if i == pos:
            return True
    return False

#AuxFunction to check size of any item and if it is a tuple, in a group (list), and delete it
def grupo(group):
    for i in range(0,len(group)):
        if(len(group[i]) == 2 and isinstance(group[i], tuple)==False):
            return False
        if(isinstance(group[i], tuple)==True):
            del group[i]
            return False

#possible moves of a piece in a tab
def possible_peg_moves(tab, pos, group):
    linha = pos_l(pos)
    coluna = pos_c(pos)

    #Searches possible moves to the left
    coluna_aux = coluna - 2
    linha_aux = linha
    if (coluna_aux >= 0 and linha_aux >= 0):
        if(linha_aux < linhastab(tab) and coluna_aux < colunastab(tab)):
            poscomp = make_pos(linha_aux, coluna_aux)
            posmeio = make_pos(linha_aux, coluna_aux + 1)

            if(lista(group,poscomp) == False and is_peg(content(tab,pos)) and is_peg(content(tab, posmeio)) and is_empty(content(tab, poscomp))):
                group = [group + [poscomp]]
                possible_peg_moves(tab, poscomp, group)

    #Searches possible moves to the right
    coluna_aux = coluna + 2
    linha_aux = linha
    if (coluna_aux >= 0 and linha_aux >= 0):
        if(linha_aux < linhastab(tab) and coluna_aux < colunastab(tab)):
            poscomp= make_pos(linha_aux, coluna_aux)
            posmeio= make_pos(linha_aux, coluna_aux - 1)

            if(lista(group,poscomp) == False and is_peg(content(tab, pos)) and is_peg(content(tab, posmeio)) and is_empty(content(tab, poscomp))):
                group = group + [[pos,poscomp]]
                possible_peg_moves(tab, poscomp, group)

    #SEarches possible moves downward
    linha_aux = linha + 2
    coluna_aux = coluna
    if (coluna_aux >= 0 and linha_aux >= 0):
        if(linha_aux < linhastab(tab) and coluna_aux < colunastab(tab)):
            poscomp= make_pos(linha_aux, coluna_aux)
            posmeio= make_pos(linha_aux - 1, coluna_aux)

            if(lista(group,poscomp) == False and is_peg(content(tab, pos)) and is_peg(content(tab, posmeio)) and is_empty(content(tab, poscomp))):
                if(lista(group,pos) == True):
                    group = group + [[pos] + [poscomp]]
                    possible_peg_moves(tab, poscomp, group)

                else:
                    group = group + [[pos, poscomp]]
                    possible_peg_moves(tab, poscomp, group)

    #Searches possible moves upward
    linha_aux = linha - 2
    coluna_aux = coluna

    if (coluna_aux >= 0 and linha_aux >= 0):
        if(linha_aux < linhastab(tab) and coluna_aux < colunastab(tab)):
            poscomp= make_pos(linha_aux, coluna_aux)
            posmeio= make_pos(linha_aux + 1, coluna_aux)

            if(lista(group,poscomp) == False and is_peg(content(tab, posmeio)) and is_peg(content(tab, pos)) and is_empty(content(tab, poscomp))):
                if(lista(group,pos) == True):
                    group = group + [[pos] + [poscomp]]
                    possible_peg_moves(tab, poscomp, group)

                else:
                    group = group + [[pos, poscomp]]
                    possible_peg_moves(tab, poscomp, group)

    return group

def board_perform_move(tab, move):
    res = []
    res = copy.deepcopy(tab)

    initial_pos = move_initial(move)
    final_pos = move_final(move)

    if(pos_c(initial_pos) != pos_c(final_pos)):
        res[pos_l(initial_pos)][pos_c(initial_pos)] = '_'
        res[pos_l(final_pos)][pos_c(final_pos)] = 'O'

        res[pos_l(final_pos)][(int((pos_c(final_pos) + pos_c(initial_pos))/2.0))] = '_'

    elif(pos_l(initial_pos) != pos_l(final_pos)):
        res[pos_l(initial_pos)][pos_c(initial_pos)] = '_'
        res[pos_l(final_pos)][pos_c(final_pos)] = 'O'

        res[(int((pos_l(final_pos) + pos_l(initial_pos))/2.0))][pos_c(final_pos)] = '_'

    return res



def board_moves(tab):
    final = []

    for i in range(0,linhastab(tab)):
        for j in range(0,colunastab(tab)):
            pos = make_pos(i,j)

            if(content(tab,pos) != 0):
                group = [pos]
                group = possible_peg_moves(tab,pos,group)

                if grupo(group) == False:
                    final += group

    return final

#number of pieces in a board
def check_occupied(tab):
    count = 0

    for i in range(0,linhastab(tab)):
        for j in range(0,colunastab(tab)):
            pos = make_pos(i,j)

            if (is_peg(content(tab,pos))):
                count = count + 1

    return count

class sol_state:
    def __init__(self,board, action = None):
        self.board = board
        self.action = action

    def actions_aux(self):
        return board_moves(self.board)

    def act_size(self):
        return len(self.actions_aux())

    def __lt__(self,other_state):
        return self.act_size()  > other_state.act_size()

    def test(self):
        if check_occupied(self.board) > 1:
            return False
        else:
            return True

    def result_aux(self,action):
        self.action = action
        r = board_perform_move(self.board,action)
        return sol_state(r, action)


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
        if(node.state.action == None):
            return 0

        #primeira heuristica
        points = check_occupied(node.state.board) * 500

        #segunda heuristica
        pos_final = move_final(node.state.action)

        if(pos_l(pos_final) == linhastab(node.state.board) or \
        pos_c(pos_final) == colunastab(node.state.board) or \
        pos_l(pos_final) == 0 or pos_c(pos_final) == 0):
            points = points * 0.8

        #outra
        moves = len(board_moves(node.state.board)) + 1
        points = points * (1/moves)

        #outra
        

        return points

#Boards and functions to test the complexity of the algorithms used

board1 =\
[["_","O","O","O","_"],\
["O","_","O","_","O"],\
["_","O","_","O","_"],\
["O","_","O","_","_"],\
["_","O","_","_","_"]]

board2 =\
[["O","O","O","X"],\
["O","O","O","O"],\
["O","_","O","O"],\
["O","O","O","O"]]

board3 =\
[["O","O","O","X","X"],\
["O","O","O","O","O"],\
["O","_","O","_","O"],\
["O","O","O","O","O"]]

board4 =\
[["O","O","O","X","X","X"],\
["O","_","O","O","O","O"],\
["O","O","O","O","O","O"],\
["O","O","O","O","O","O"]]

problems = [solitaire(board1), solitaire(board2), solitaire(board3), solitaire(board4)]
searchers = [astar_search]
header = None

def compare_searchers(problems, header, searchers):
    def do(searcher, problem):
        p = InstrumentedProblem(problem)
        '''if(searcher == greedy_best_first_graph_search):
            searcher(p,p.h)
        else:
            searcher(p)'''
        searcher(p)
        print('done')
        return p
    table = [[name(s)] + [do(s, p) for p in problems] for s in searchers]
    print_table(table, header)


def compare_graph_searchers():
    compare_searchers(problems, header, searchers)

compare_graph_searchers()
