
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
# Tuplo (l, c)
def make_pos (l, c):
    return (l, c)
def pos_l (pos):
    return pos[0]
def pos_c (pos):
    return pos[1] 

# TAI move
# Lista [p_initial, p_final]
def make_move (i,f):
    return [i,f]
def move_initial (move):
    return move[0]
def move_final (move):
    return move[1] 

def linhastab(tab):
    return len(tab)

def colunastab(tab):
    return len(tab[0])

def cor(tab,pos):
    linha = pos_l(pos)
    coluna = pos_c(pos)
    return tab[linha][coluna]

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
    
    esq=[]
    dir=[]
    
    linha = pos_l(pos)
    coluna = pos_c(pos)
    pos=make_pos(linha, coluna)
    
    #procuraesquerda
    colunacomp=coluna -2
    linhacomp=linha
    if (colunacomp >= 0 and linhacomp >= 0):
        if(linhacomp < linhastab(tab) and colunacomp < colunastab(tab)):
            poscomp= make_pos(linhacomp, colunacomp)
            posmeio= make_pos(linhacomp, colunacomp+1)
            if(lista(esq,poscomp) == False and is_peg(cor(tab, posmeio)) and is_empty(cor(tab, poscomp))):
                    esq += [poscomp, pos]
                    possiveisgruposlinhas(tab, poscomp, esq)    
      

    #procuradireita
    colunacomp = coluna +2
    linhacomp=linha
    if (colunacomp >= 0 and linhacomp >= 0):
        if(linhacomp < linhastab(tab) and colunacomp < colunastab(tab)):
            poscomp= make_pos(linhacomp, colunacomp)
            posmeio= make_pos(linhacomp, colunacomp-1)
            if(lista(dir,poscomp) == False  and is_peg(cor(tab, posmeio)) and is_empty(cor(tab, poscomp))):
                dir += [pos,poscomp]
                possiveisgruposlinhas(tab, poscomp, dir)        
   

    group = [esq] + [dir]
    return group

def possiveisgruposcolunas(tab, pos, group):

    
    linha = pos_l(pos)
    coluna = pos_c(pos)
    
    #procurabaixo
    linhacomp= linha + 2
    colunacomp=coluna
    if (colunacomp >= 0 and linhacomp >= 0):
        if(linhacomp < linhastab(tab) and colunacomp < colunastab(tab)):
            poscomp= make_pos(linhacomp, colunacomp)
            posmeio= make_pos(linhacomp-1, colunacomp)
            if(lista(group,poscomp) == False and is_peg(cor(tab, posmeio)) and is_empty(cor(tab, poscomp))):
                    group += [poscomp]
                    possiveisgruposlinhas(tab, poscomp, group)    
      

    #procuracima
    linhacomp=linha-2
    colunacomp=coluna
    if (colunacomp >= 0 and linhacomp >= 0):
        if(linhacomp < linhastab(tab) and colunacomp < colunastab(tab)):
            poscomp= make_pos(linhacomp, colunacomp)
            posmeio= make_pos(linhacomp+1, colunacomp)
            if(lista(group,poscomp) == False and is_peg(cor(tab, posmeio)) and is_empty(cor(tab, poscomp))):
                    group += [poscomp]
                    possiveisgruposlinhas(tab, poscomp, group)        
   


    return group


def board_moves(tab):
    final = []
    for i in range(0,linhastab(tab)):
        for j in range(0,colunastab(tab)):
            pos = make_pos(i,j)
            if(cor(tab,pos) != 0):
                group = [pos]
                group = possiveisgruposlinhas(tab,pos,group)
                if grupo(final,group) == False:
                    final += [group]
    for i in range(0,linhastab(tab)):
        for j in range(0,colunastab(tab)):
            pos = make_pos(i,j)
            if(cor(tab,pos) != 0):
                group = [pos]
                group = possiveisgruposcolunas(tab,pos,group)
                if grupo(final,group) == False:
                    final += [group]    
                
    return final

