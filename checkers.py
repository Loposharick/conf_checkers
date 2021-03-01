from tkinter import *
import random
import os
root = Tk()


n = 8
k_prev = 0
turns_amount = 0
prev_boards = []
size = 80
hei = 600
wid = 1000
root.title('Решатель шашечных задач')
root.resizable(False,False)
canv = Canvas(width=wid, height=hei, bg='#00032F')
x_y_from = []
x_y_to = []
turn = 1
type_choice = 0
ov_rect = 0
canv.pack()

def sort_set(l):
    a = []
    for i in l:
        if i not in a:
            a.append(i)
    return a

def turns_conv(a):
    b = []
    for i in range(3):
        a = [a]
    while True:
        try:
            b.append(a)
            a = a[0]
        except TypeError:
            return b[-3]

def sort_pos():
    possible_turns = []
    for i in range(len(froms)):
        for j in range(len(pos[froms[i][0], froms[i][1]])):
            x_y_from = froms[i]
            x_y_to = pos[froms[i][0], froms[i][1]][j]
            possible_turns.append([x_y_from, x_y_to])
    return possible_turns
    
def get_n():
    global b
    global type_choice
    global n
    global size
    global game_choice
    n = message.get()
    game_choice = var.get()
    type_choice = 1
    size = hei//(n + 1)
    b = Board()
    message_entry.destroy()
    message_button.destroy()
    pod_check.destroy()
    norm_check.destroy()
    message_label.destroy()
    graph()
    canv.delete
    mainloop()

def oval_func(event):
     global x_y_from
     global x_y_to
     global ov_rect
     global m
     if ov_rect == 0:
         abs_coord_x = root.winfo_pointerx() - root.winfo_rootx()
         abs_coord_y = root.winfo_pointery() - root.winfo_rooty()
         x_y_from = [(abs_coord_x // size) - 1, (abs_coord_y // size) - 1]
         ov_rect = 1

def rect_func(event):
     global x_y_to
     global x_y_from
     global ov_rect
     if ov_rect == 1:
         abs_coord_x = root.winfo_pointerx() - root.winfo_rootx()
         abs_coord_y = root.winfo_pointery() - root.winfo_rooty()
         x_y_to = [(abs_coord_x // size) - 1, (abs_coord_y // size) - 1]
         game()
         ov_rect = 0
         graph()

def prev_board(event):
    global turn
    global k_prev
    b.reinit(prev_boards[turns_amount - 1 - k_prev].board)
    if turn == 1:
        turn = 2
    else:
        turn = 1
    k_prev += 1
    graph()    

def start_pos(event):
    global turn
    global b
    b = Board()
    turn = 1
    graph()

def zad_resh(event):
    reshenie(4)

def reshenie(it):
    global turn
    global boards
    global resh
    global depth
    global jk_sum
    boards = []
    mod = 0
    zaf_board = Board()
    zaf_turns = 0
    boards.append([])
    sol = 0
    start_turn = turn
    jk_sum = 0
    #print('')
    b.get_turns(turn)
    for i in sort_pos():
        mod += 1
        boards[0].append([Board(), [i]])
        boards[0][-1][0].reinit(b.board)
        if boards[0][-1][0].zafuk(turn):
            if boards[0][-1][0].get_deleted(i[0][0], i[0][1], i[1][0], i[1][1], turn) == None:
                boards[0].remove(boards[0][-1])
                continue
            boards[0][-1][0].delete(boards[0][-1][0].get_deleted(i[0][0], i[0][1], i[1][0], i[1][1], turn))
            boards[0][-1][0].move(i[0], i[1])
            boards[0][-1][0].dam_check(i[1])
            while True:
                if boards[0][-1][0].zafuk(turn):
                    zaf_turns = boards[0][-1][1]
                    boards[0][-1][0].get_turns(turn)
                    zaf_board.reinit(boards[0][-1][0].board)
                    boards[0].remove(boards[0][-1])
                    for k in sort_pos():
                        boards[0].append([Board(), []])
                        zaf_turns.append(k)
                        boards[0][-1][1].append(zaf_turns)
                        boards[0][-1][0].reinit(zaf_board.board)
                        if boards[0][-1][0].zafuk(turn):
                            if boards[0][-1][0].get_deleted(k[0][0], k[0][1], k[1][0], k[1][1], turn) == None:
                                boards[0].remove(boards[0][-1])
                                continue
                            boards[0][-1][0].delete(boards[0][-1][0].get_deleted(k[0][0], k[0][1], k[1][0], k[1][1], turn))
                            boards[0][-1][0].move(k[0], k[1])
                            boards[0][-1][0].dam_check(k[1])
                    if boards[0][-1][0].zafuk(turn) == False:
                        break
                else:
                    break
        else:
            boards[0][-1][0].move(i[0], i[1])
            boards[0][-1][0].dam_check(i[1])            
    for c in range(it):
        boards.append([])
        if turn == 1:
            turn = 2        
        else:
            turn = 1
        for i in boards[c]:
            i[0].get_turns(turn)
            for j in sort_pos():
                mod += 1
                #print(i, '\n', '\n', i[1])
                boards[c + 1].append([Board(), i[1:len(i) + 1], j])
                boards[c + 1][-1][0].reinit(i[0].board)
                if boards[c + 1][-1][0].zafuk(turn):
                    if boards[c + 1][-1][0].get_deleted(j[0][0], j[0][1], j[1][0], j[1][1], turn) == None:
                        boards[c + 1].remove(boards[c + 1][-1])
                        continue
                    boards[c + 1][-1][0].delete(boards[c + 1][-1][0].get_deleted(j[0][0], j[0][1], j[1][0], j[1][1], turn))
                    boards[c + 1][-1][0].move(j[0], j[1])
                    boards[c + 1][-1][0].dam_check(j[1])
                    while True:
                        if boards[c + 1][-1][0].zafuk(turn):
                            zaf_turns = boards[c + 1][-1][1]
                            boards[c + 1][-1][0].get_turns(turn)
                            zaf_board.reinit(boards[c + 1][-1][0].board)
                            boards[c + 1].remove(boards[c + 1][-1])
                            for k in sort_pos():
                                boards[c + 1].append([Board(), []])
                                zaf_turns.append(k)
                                boards[c + 1][-1][1].append(zaf_turns)
                                boards[c + 1][-1][0].reinit(zaf_board.board)
                                if boards[c + 1][-1][0].zafuk(turn):
                                    if boards[c + 1][-1][0].get_deleted(k[0][0], k[0][1], k[1][0], k[1][1], turn) == None:
                                        boards[c + 1].remove(boards[c + 1][-1])
                                        continue
                                    boards[c + 1][-1][0].delete(boards[c + 1][-1][0].get_deleted(k[0][0], k[0][1], k[1][0], k[1][1], turn))
                                    boards[c + 1][-1][0].move(k[0], k[1])
                                    boards[c + 1][-1][0].dam_check(k[1])
                            if boards[c + 1][-1][0].zafuk(turn) == False:
                                break
                        else:
                            break
                else:
                    boards[c + 1][-1][0].move(j[0], j[1])
                    boards[c + 1][-1][0].dam_check(j[1])
            if turn != start_turn:
                jk_sum += len(boards[-1])
    for i in boards[::-1]:
        if i == []:
            boards.remove(i)
    if start_turn == 1:
        turn = 2
    else:
        turn = 1
    resh = []
    for i in boards[-1]:
        if i[0].is_win():
            resh.append(turns_conv(i[1:len(i)]))
    for i in boards[-1]:
        if i[0].is_win() == False:
            resh = list(filter((turns_conv(i[1:len(i)])).__ne__, resh))
    sort_set(resh)           
    for i in boards[-1]:
        if turns_conv(i[1:len(i)]) in resh:
            if it == depth:
                print('\n', i[1:len(i)], '\n', i[0])
            sol = 1
    turn = start_turn
    if sol == 1:
        if it == depth:
            print(jk_sum)
            print('----------------------------------------')    
        return(True)
                                            
def zad_gen(event):
    global turn
    global a
    global depth
    global jk_sum
    bas = Board()
    bas.reinit(b.board)
    depth = 2
    ch = 0
    count = 0
    while True:
        graph()
        b.get_turns(turn)
        a = sort_pos()
        random.shuffle(a)
        count += 1
        for i in a:
            if b.zafuk(turn):
                if b.get_deleted(i[0][0], i[0][1], i[1][0], i[1][1], turn) == None:
                    continue
                b.delete(b.get_deleted(i[0][0], i[0][1], i[1][0], i[1][1], turn))
            b.move(i[0], i[1])
            b.dam_check(i[1])
        if turn == 1:
            turn = 2
        else:
            turn = 1
        if b.is_win() == True:
            b.reinit(bas.board)
        if reshenie(depth):
            for l in range(0, depth, 2):
                if reshenie(l) == True:
                    ch = 1
                else:
                    ch = 2
        if ch == 2:
            if reshenie(depth):
                if jk_sum >= (n * n * depth) or True:
                    graph()
                    break
                else:
                    print(jk_sum)
def graph():
    global x_y_from
    global x_y_to
    global end_game
    text_size = 'Verdana ' + '21'
    county = size
    canv.delete('text')
    canv.delete('button')
    canv.delete('button1')
    canv.delete('prev')
    canv.delete('start_b')
    b.get_turns(turn)
    if type_choice == 1:
        if end_game == 1:
            if turn == 1:
                canv.create_text(100, 20, text='Ход Белых', font = text_size, tag ='text', fill="white")
            else:
                canv.create_text(100, 20, text='Ход Черных', font = text_size, tag ='text', fill="white")
            canv.create_text((wid // 2), 20, text='Решение', font = text_size, tag ='button', fill="white")
            canv.create_text((wid // 3.5), 20, text='Генерация', font = text_size, tag ='button1', fill="white")
            canv.create_text((wid // 1.4), 20, text='Вернуть ход', font = text_size, tag ='prev', fill="white")
            if game_choice == 1:
                canv.create_text(wid - 100, 20, text='Шашки', font = text_size, tag ='text', fill="white")
            elif game_choice == 2:
                canv.create_text(wid - 100, 20, text='Поддавки', font = text_size, tag ='text', fill="white")
            canv.create_text(wid - 100, 120, text='Начало', font = text_size, tag ='start_b', fill="white")    
            for j in range(n):
                countx = size
                if j % 2 == 1:
                    for i in range(n):
                        if i % 2 == 0:
                            canv.create_rectangle(countx, county, countx + size, county + size,
                                outline="#000000", fill="brown", tag='rect')
                        else:
                            canv.create_rectangle(countx, county, countx + size, county + size,
                                outline='#000000', fill='white', tag='rect')
                        if b.type_of(i, j) == Checker and b.get_color(i, j) == 1:
                            canv.create_oval(countx + size // 10, county + size // 10, countx - size // 10 + size, county - size // 10 + size,
                                tag='oval', outline='#000000', fill='white')
                        if b.type_of(i, j) == Checker and b.get_color(i, j) == 2:
                            canv.create_oval(countx + size // 10, county + size // 10, countx - size // 10 + size, county - size // 10 + size,
                                tag='oval', outline='#000000', fill='black')
                        if b.type_of(i, j) == Dam and b.get_color(i, j) == 1:
                            canv.create_oval(countx + size // 10, county + size // 10, countx - size // 10 + size, county - size // 10 + size,
                                tag='oval', outline='#000000', fill='white')
                            canv.create_oval(countx + size // 3, county + size // 3, countx - size // 3 + size, county - size // 3 + size,
                                tag='oval', outline='#000000', fill='black')
                        if b.type_of(i, j) == Dam and b.get_color(i, j) == 2:
                            canv.create_oval(countx + size // 10, county + size // 10, countx - size // 10 + size, county - size // 10 + size,
                                tag='oval', outline='#000000', fill='black')
                            canv.create_oval(countx + size // 3, county + size // 3, countx - size // 3 + size, county - size // 3 + size,
                                tag='oval', outline='#000000', fill='white')
                        countx = countx + size
                else:
                    for i in range(n):
                        if i % 2 == 1:
                            canv.create_rectangle(countx, county, countx + size, county + size,
                                outline="#000000", fill="brown", tag='rect')
                        else:
                            canv.create_rectangle(countx, county, countx + size, county + size,
                                outline='#000000', fill='white', tag='rect')
                        if b.type_of(i, j) == Checker and b.get_color(i, j) == 1:
                            canv.create_oval(countx + size // 10, county + size // 10, countx - size // 10 + size, county - size // 10 + size,
                                tag='oval', outline='#000000', fill='white')
                        if b.type_of(i, j) == Checker and b.get_color(i, j) == 2:
                            canv.create_oval(countx + size // 10, county + size // 10, countx - size // 10 + size, county - size // 10 + size,
                                tag='oval', outline='#000000', fill='black')
                        if b.type_of(i, j) == Dam and b.get_color(i, j) == 1:
                            canv.create_oval(countx + size // 10, county + size // 10, countx - size // 10 + size, county - size // 10 + size,
                                tag='oval', outline='#000000', fill='white')
                            canv.create_oval(countx + size // 3, county + size // 3, countx - size // 3 + size, county - size // 3 + size,
                                tag='oval', outline='#000000', fill='black')
                        if b.type_of(i, j) == Dam and b.get_color(i, j) == 2:
                            canv.create_oval(countx + size // 10, county + size // 10, countx - size // 10 + size, county - size // 10 + size,
                                tag='oval', outline='#000000', fill='black')
                            canv.create_oval(countx + size // 3, county + size // 3, countx - size // 3 + size, county - size // 3 + size,
                                tag='oval', outline='#000000', fill='white')
                        countx = countx + size
                county = county + size
        else:
            if game_choice == 1:
                canv.create_text((wid // 5), 20, text='Вернуть ход', font = text_size, tag ='prev', fill="white")
                if win_side == 1:
                    canv.create_text(wid - 150, 20, text='Белые победили', font = text_size, tag ='text', fill="white")
                elif win_side == 2:
                    canv.create_text(wid - 150, 20, text='Черные победили', font = text_size, tag ='text', fill="white")
            elif game_choice == 2:
                if win_side == 2:
                    canv.create_text(wid - 150, 20, text='Белые победили', font = text_size, tag ='text', fill="white")
                elif win_side == 1:
                    canv.create_text(wid - 150, 20, text='Черные победили', font = text_size, tag ='text', fill="white")
            for j in range(n):
                countx = size
                if j % 2 == 1:
                    for i in range(n):
                       if i % 2 == 0:
                           canv.create_rectangle(countx, county, countx + size, county + size,
                               outline="#000000", fill="brown", tag='rect')
                       else:
                           canv.create_rectangle(countx, county, countx + size, county + size,
                               outline='#000000', fill='white', tag='rect')
                       if b.type_of(i, j) == Checker and b.get_color(i, j) == 1:
                           canv.create_oval(countx + size // 10, county + size // 10, countx - size // 10 + size, county - size // 10 + size,
                               tag='oval', outline='#000000', fill='white')
                       if b.type_of(i, j) == Checker and b.get_color(i, j) == 2:
                           canv.create_oval(countx + size // 10, county + size // 10, countx - size // 10 + size, county - size // 10 + size,
                               tag='oval', outline='#000000', fill='black')
                       if b.type_of(i, j) == Dam and b.get_color(i, j) == 1:
                           canv.create_oval(countx + size // 10, county + size // 10, countx - size // 10 + size, county - size // 10 + size,
                               tag='oval', outline='#000000', fill='white')
                           canv.create_oval(countx + size // 3, county + size // 3, countx - size // 3 + size, county - size // 3 + size,
                               tag='oval', outline='#000000', fill='black')
                       if b.type_of(i, j) == Dam and b.get_color(i, j) == 2:
                           canv.create_oval(countx + size // 10, county + size // 10, countx - size // 10 + size, county - size // 10 + size,
                               tag='oval', outline='#000000', fill='black')
                           canv.create_oval(countx + size // 3, county + size // 3, countx - size // 3 + size, county - size // 3 + size,
                               tag='oval', outline='#000000', fill='white')
                       countx = countx + size
                else:
                    for i in range(n):
                        if i % 2 == 1:
                            canv.create_rectangle(countx, county, countx + size, county + size,
                                outline="#000000", fill="brown", tag='rect')
                        else:
                            canv.create_rectangle(countx, county, countx + size, county + size,
                                outline='#000000', fill='white', tag='rect')
                        if b.type_of(i, j) == Checker and b.get_color(i, j) == 1:
                            canv.create_oval(countx + size // 10, county + size // 10, countx - size // 10 + size, county - size // 10 + size,
                                tag='oval', outline='#000000', fill='white')
                        if b.type_of(i, j) == Checker and b.get_color(i, j) == 2:
                            canv.create_oval(countx + size // 10, county + size // 10, countx - size // 10 + size, county - size // 10 + size,
                                tag='oval', outline='#000000', fill='black')
                        if b.type_of(i, j) == Dam and b.get_color(i, j) == 1:
                            canv.create_oval(countx + size // 10, county + size // 10, countx - size // 10 + size, county - size // 10 + size,
                                tag='oval', outline='#000000', fill='white')
                            canv.create_oval(countx + size // 3, county + size // 3, countx - size // 3 + size, county - size // 3 + size,
                                tag='oval', outline='#000000', fill='black')
                        if b.type_of(i, j) == Dam and b.get_color(i, j) == 2:
                            canv.create_oval(countx + size // 10, county + size // 10, countx - size // 10 + size, county - size // 10 + size,
                                tag='oval', outline='#000000', fill='black')
                            canv.create_oval(countx + size // 3, county + size // 3, countx - size // 3 + size, county - size // 3 + size,
                                tag='oval', outline='#000000', fill='white')
                        countx = countx + size
                county = county + size
            canv.pack()
def game():
    global turn
    global m
    global pos
    global turns_amount
    global prev_boards
    global k_prev
    ap = Board()
    k_prev = 0
    rub_choice = 0
    x_y_del = []
    zn = []
    m = b.get_moves(x_y_from[0], x_y_from[1])
    ap.reinit(b.board)
    if x_y_from[0] >= 0 and x_y_from[0] <= n - 1 and x_y_from[1] >= 0 and x_y_from[1] <= n - 1:
        if b.zafuk(turn) == False:
               if type(m) == tuple:
                    m = m[0]
               if x_y_to in m:
                   if type(m) == list:
                        if len(m) > 0:
                           b.move(x_y_from, x_y_to)
                           b.dam_check(x_y_to)
                           if turn == 1:
                               turn = 2
                               turns_amount += 1
                               prev_boards.append(Board())
                               prev_boards[-1].reinit(ap.board)
                           elif turn == 2:
                               turn = 1
                               turns_amount += 1
                               prev_boards.append(Board())
                               prev_boards[-1].reinit(ap.board)
        elif b.zafuk(turn):
            if len(m) != 0:
                if type(m[0]) == list:
                    if len(m[0]) > 0:
                        if x_y_to in m[0]:
                            x_y_del = b.get_deleted(x_y_from[0], x_y_from[1], x_y_to[0], x_y_to[1], turn)
                            if len(x_y_del) != 0:
                                b.delete(x_y_del)
                            b.move(x_y_from, x_y_to)
                            b.dam_check(x_y_to)
                            if turn == 1:
                                if b.zafuk(1):
                                    turn = 1
                                else:
                                    turn = 2
                                    turns_amount += 1
                                    prev_boards.append(Board())
                                    prev_boards[-1].reinit(ap.board)                                    
                            elif turn == 2:
                                if b.zafuk(2):
                                    turn = 2
                                else:
                                    turn = 1
                                    turns_amount += 1
                                    prev_boards.append(Board())
                                    prev_boards[-1].reinit(ap.board)

class Color(object):
    EMPTY = 0
    BLACK = 2
    WHITE = 1

class Empty(object):
    color = Color.EMPTY

    def get_moves(self, board, x, y):
        moves = []
        return moves

    def __str__(self):
        return '.'

    def type_of(self, board, x, y):
        return Empty

class CheckerMan(object):
    IMG = None

    def __init__(self, color):
        self.color = color

    def __str__(self):
        return self.IMG[0 if self.color == Color.WHITE else 1]


class Checker(CheckerMan):
    IMG = ('б', 'ч')

    def type_of(self, board, x, y):
        return Checker

    def get_moves(self, board, x, y):
        moves = []
        deleted = []
        global turn
        if x <= n - 1 and y <= n - 1:
            if board.zafuk(turn) == False:
                if x < n and y < n:
                    if turn == 1:
                        if x + 1 <= n - 1 and y + 1 <=n - 1:
                            if board.get_color(x, y) == Color.WHITE and y <= n - 1 and board.get_color(x+1, y+1) == Color.EMPTY:
                                moves.append([x+1, y+1])
                        if x - 1 >= 0 and y + 1 <=n - 1:
                            if board.get_color(x, y) == Color.WHITE and y <= n - 1 and board.get_color(x-1, y+1) == Color.EMPTY:
                                moves.append([x-1, y+1])
                    elif turn == 2:
                        if x + 1 <= n - 1 and y - 1 >= 0:
                            if board.get_color(x, y) == Color.BLACK and y <= n - 1 and board.get_color(x+1, y-1) == Color.EMPTY:
                                moves.append([x+1, y-1])
                        if x - 1 >= 0 and y - 1 >= 0:
                            if board.get_color(x, y) == Color.BLACK and y <= n - 1 and board.get_color(x-1, y-1) == Color.EMPTY:
                                moves.append([x-1, y-1])
                return moves
            else:
                if x < n and y < n:
                    if turn == 1:
                        if x + 2 <= n - 1 and y + 2 <= n - 1:
                            if board.get_color(x, y) == Color.WHITE and board.get_color(x+1, y+1) == Color.BLACK and board.get_color(x+2, y+2) == Color.EMPTY:
                                moves.append([x+2, y+2])
                                deleted.append([x+1, y+1])
                        if x - 2 >= 0 and y + 2 <= n - 1:
                            if board.get_color(x, y) == Color.WHITE and board.get_color(x-1, y+1) == Color.BLACK and board.get_color(x-2, y+2) == Color.EMPTY:
                                moves.append([x-2, y+2])
                                deleted.append([x-1, y+1])
                        if x + 2 <= n - 1 and y - 2 >= 0:
                            if board.get_color(x, y) == Color.WHITE and board.get_color(x+1, y-1) == Color.BLACK and board.get_color(x+2, y-2) == Color.EMPTY:
                                moves.append([x+2, y-2])
                                deleted.append([x+1, y-1])
                        if x - 2 >= 0 and y - 2 >= 0:
                            if board.get_color(x, y) == Color.WHITE and board.get_color(x-1, y-1) == Color.BLACK and board.get_color(x-2, y-2) == Color.EMPTY:
                                moves.append([x-2, y-2])
                                deleted.append([x-1, y-1])
                    elif turn == 2:
                        if x + 2 <= n - 1 and y + 2 <= n - 1:
                            if board.get_color(x, y) == Color.BLACK and board.get_color(x+1, y+1) == Color.WHITE and board.get_color(x+2, y+2) == Color.EMPTY:
                                moves.append([x+2, y+2])
                                deleted.append([x+1, y+1])
                        if x - 2 >= 0 and y + 2 <= n - 1:
                            if board.get_color(x, y) == Color.BLACK and board.get_color(x-1, y+1) == Color.WHITE and board.get_color(x-2, y+2) == Color.EMPTY:
                                moves.append([x-2, y+2])
                                deleted.append([x-1, y+1])
                        if x + 2 <= n - 1 and y - 2 >= 0:
                            if board.get_color(x, y) == Color.BLACK and board.get_color(x+1, y-1) == Color.WHITE and board.get_color(x+2, y-2) == Color.EMPTY:
                                moves.append([x+2, y-2])
                                deleted.append([x+1, y-1])
                        if x - 2 >= 0 and y - 2 >= 0:
                            if board.get_color(x, y) == Color.BLACK and board.get_color(x-1, y-1) == Color.WHITE and board.get_color(x-2, y-2) == Color.EMPTY:
                                moves.append([x-2, y-2])
                                deleted.append([x-1, y-1])
        return moves, deleted

class DamMan(object):
    IMG = None

    def type_of(self, board, x, y):
        return Dam

    def __init__(self, color):
        self.color = color

    def __str__(self):
        return self.IMG[0 if self.color == Color.WHITE else 1]
class Dam(DamMan):
    IMG = ('3', '4')

    def get_moves(self, board, x, y):
        moves_zaf = []
        var = 0
        moves = []
        deleted = []
        check_var = [0, 0, 0, 0]
        d = dict()
        global turn
        if board.get_color(x, y) == turn:
            for k in range(n):
                if board.zafuk(turn) == False:
                    if x < n - k and y < n - k:
                        if board.get_color(x + k, y + k) == Color.EMPTY and check_var[0] == 0:
                            moves.append([x + k, y + k])
                        else:
                            if k > 0:
                                check_var[0] = 1
                    if x - k >= 0  and y - k >= 0:
                        if board.get_color(x - k, y - k) == Color.EMPTY and check_var[1] == 0:
                            moves.append([x - k, y - k])
                        else:
                            if k > 0:
                                check_var[1] = 1
                    if x < n - k and y - k >= 0:
                        if board.get_color(x + k, y - k) == Color.EMPTY and check_var[2] == 0:
                            moves.append([x + k, y - k])
                        else:
                            if k > 0:
                                check_var[2] = 1
                    if x - k >= 0 and y < n - k:
                        if board.get_color(x - k, y + k) == Color.EMPTY and check_var[3] == 0:
                            moves.append([x - k, y + k])
                        else:
                            if k > 0:
                                check_var[3] = 1
                else:
                    if x + k <= n - 1 and y + k <= n - 1:
                        if board.type_of(x + k, y + k) == Checker or Dam:
                            for c in range(n):
                                if (x + k) + c <= n - 1 and (y + k) + c <= n - 1:
                                    if board.type_of((x + k) + c, (y + k) + c) == Empty:
                                        moves.append([(x + k) + c, (y + k) + c])
                    if x - k >= 0 and y - k >= 0:
                        if board.type_of(x - k, y - k) == Checker or Dam:
                            for c in range(n):
                                if (x - k) - c >= 0 and (y - k) - c >= 0:
                                    if board.type_of((x - k) - c, (y - k) - c) == Empty:
                                        moves.append([(x - k) - c, (y - k) - c])
                    if x + k <= n - 1 and y - k >= 0:
                        if board.type_of(x + k, y - k) == Checker or Dam:
                            for c in range(n):
                                if (x + k) + c <= n - 1 and (y - k) - c >= 0:
                                    if board.type_of((x + k) + c, (y - k) - c) == Empty:
                                        moves.append([(x + k) + c, (y - k) - c])
                    if x - k >= 0 and y + k <= n - 1:
                        if board.type_of(x - k, y + k) == Checker or Dam:
                            for c in range(n):
                                if (x - k) - c >= 0 and (y + k) + c <= n - 1:
                                    if board.type_of((x - k) - c, (y + k) + c) == Empty:
                                        moves.append([(x - k) - c, (y + k) + c])
        return moves, d, deleted

class Board(object):
    def __init__(self):
        self.board = [[Empty()] * n for y in range(n)]
        r = (n - 2) // 2
        for i in range(n):
            if i % 2 == 0:
                if i < r:
                    for j in range(n):
                        if j % 2 != 0:
                            self.board[i][j] = Checker(Color.WHITE)
                if i > n - (r + 1):
                    for j in range(n):
                        if j % 2 != 0:
                            self.board[i][j] = Checker(Color.BLACK)
            else:
                if i < r:
                    for j in range(n):
                        if j % 2 == 0:
                            self.board[i][j] = Checker(Color.WHITE)
                if i > n - (r + 1):
                    for j in range(n):
                        if j % 2 == 0:
                            self.board[i][j] = Checker(Color.BLACK)
        
    def reinit(self, positions):
         for i in range(n):
              for j in range(n):
                   self.board[i][j] = positions[i][j]

    def ravn(self, positions):
         for i in range(n):
              for j in range(n):
                   if self.board[i][j] != positions[i][j]:
                       return False
         return True           
    
    def type_of(self, x, y):
        return self.board[y][x].type_of(self, x, y)

    def get_turns(self, t):
        global pos
        global froms
        global end_game
        global win_side
        end_game = 0
        win_side = 0
        m1 = []
        froms = []
        pos = dict()
        for i in range(n):
            for j in range(n):
                if self.get_color(j, i) == t:
                    if len(self.get_moves(j, i)) != 0:
                        end_game = 1
                        if self.type_of(j, i) != Empty:
                            if self.zafuk(t) == False:
                                m1 = self.get_moves(j, i)
                                froms.append([j, i])
                                if type(m1) == tuple:
                                    m1 = m1[0]
                                pos[j, i] = m1
                            else:
                                m1 = self.get_moves(j, i)
                                if len(m1[0]) != 0:
                                    froms.append([j, i])
                                    pos[j, i] = m1[0]
                            try:
                                pos[j, i] = sort_set(pos[j, i])        
                            except KeyError:
                                a = 0
        if end_game == 0:
          if t == 1:
              win_side = 2
          else:
              win_side = 1
    def get_color(self, x, y):
        return self.board[y][x].color

    def get_deleted(self, x_f, y_f, x_t, y_t, t):
        if self.type_of(x_f, y_f) == Dam or self.type_of(x_f, y_f) == Checker:
            #print(x_f, y_f, x_t, y_t)
            if x_f > x_t and y_f > y_t:
                 for i in range(x_f - x_t):
                     if t == 1:
                         if self.get_color(x_f - i, y_f - i) == Color.BLACK:
                             return [x_f - i, y_f - i]
                     elif t == 2:
                         if self.get_color(x_f - i, y_f - i) == Color.WHITE:
                             return [x_f - i, y_f - i]
            if x_f > x_t and y_f < y_t:
                 for i in range(x_f - x_t):
                     if t == 1:
                         if self.get_color(x_f - i, y_f + i) == Color.BLACK:
                             return [x_f - i, y_f + i]
                     elif t == 2:
                         if self.get_color(x_f - i, y_f + i) == Color.WHITE:
                             return [x_f - i, y_f + i]
            if x_f < x_t and y_f < y_t:
                 for i in range(x_t - x_f):
                     if t == 1:
                         if self.get_color(x_f + i, y_f + i) == Color.BLACK:
                             return [x_f + i, y_f + i]
                     elif t == 2:
                         if self.get_color(x_f + i, y_f + i) == Color.WHITE:
                             return [x_f + i, y_f + i]
            if x_f < x_t and y_f > y_t:
                 for i in range(x_t - x_f):
                     if t == 1:
                         if self.get_color(x_f + i, y_f - i) == Color.BLACK:
                             return [x_f + i, y_f - i]
                     elif t == 2:
                         if self.get_color(x_f + i, y_f - i) == Color.WHITE:
                             return [x_f + i, y_f - i]


    def is_win(self):
        global end_game
        end_game = 0
        for i in range(n):
            for j in range(n):
                if self.get_color(j, i) == turn:
                    if len(self.get_moves(j, i)) != 0:
                        end_game = 1
        if end_game == 1:
            return False
        else:
            return True

    def get_moves(self, x, y):
        return self.board[y][x].get_moves(self, x, y)

    def move(self, xy_from, xy_to):
        self.board[xy_to[1]][xy_to[0]] = self.board[xy_from[1]][xy_from[0]]
        self.board[xy_from[1]][xy_from[0]] = Empty()

    def delete(self, xy_del):
        self.board[xy_del[1]][xy_del[0]] = Empty()

    def dam_check(self, xy_to):
        if self.board[xy_to[1]][xy_to[0]].color == Color.WHITE:
            if xy_to[1] == n - 1:
                self.board[xy_to[1]][xy_to[0]] = Dam(Color.WHITE)
        elif self.board[xy_to[1]][xy_to[0]].color == Color.BLACK:
            if xy_to[1] == 0:
                self.board[xy_to[1]][xy_to[0]] = Dam(Color.BLACK)

    def __str__(self):
        res = ''
        for y in range(n):
            res += ''.join(str(y)) + ' '
            res += ''.join(map(str, self.board[y])) + "\n"
        return res

    def zafuk(self, tu):
        global n
        var = 0
        rub = 0
        for j in range(n):
            for i in range(n):
                if self.type_of(i, j) == Checker:
                    if self.board[j][i].color == tu:
                        if self.board[j][i].color == Color.WHITE:
                            if j + 1 <= n - 1 and i + 1 <= n - 1:
                                if self.board[j + 1][i + 1].color == Color.BLACK:
                                    if j + 2 <= n - 1 and i + 2 <= n - 1:
                                        if self.board[j + 2][i + 2].color == Color.EMPTY:
                                            return(True)
                            if j + 1 <= n - 1 and i - 1 >= 0:
                                if self.board[j + 1][i - 1].color == Color.BLACK:
                                    if j + 2 <= n - 1 and i - 2 >= 0:
                                        if self.board[j + 2][i - 2].color == Color.EMPTY:
                                            return(True)
                            if j - 1 >= 0 and i + 1 <= n - 1:
                                if self.board[j - 1][i + 1].color == Color.BLACK:
                                    if j - 2 >= 0 and i + 2 <= n - 1:
                                        if self.board[j - 2][i + 2].color == Color.EMPTY:
                                            return(True)
                            if j - 1 >= 0 and i - 1 >= 0:
                                if self.board[j - 1][i - 1].color == Color.BLACK:
                                    if j - 2 >= 0 and i - 2 >= 0:
                                        if self.board[j - 2][i - 2].color == Color.EMPTY:
                                            return(True)
                        elif self.board[j][i].color == Color.BLACK:
                            if j - 1 >= 0 and i + 1 <= n - 1:
                                if self.board[j - 1][i + 1].color == Color.WHITE:
                                    if j - 2 >= 0 and i + 2 <= n - 1:
                                        if self.board[j - 2][i + 2].color == Color.EMPTY:
                                            return(True)
                            if j - 1 >= 0 and i - 1 >= 0:
                                if self.board[j - 1][i - 1].color == Color.WHITE:
                                    if j - 2 >= 0 and i - 2 >= 0:
                                        if self.board[j - 2][i - 2].color == Color.EMPTY:
                                            return(True)
                            if j + 1 <= n - 1 and i + 1 <= n - 1:
                                if self.board[j + 1][i + 1].color == Color.WHITE:
                                    if j + 2 <= n - 1 and i + 2 <= n - 1:
                                        if self.board[j + 2][i + 2].color == Color.EMPTY:
                                            return(True)
                            if j + 1 <= n - 1 and i - 1 >= 0:
                                if self.board[j + 1][i - 1].color == Color.WHITE:
                                    if j + 2 <= n - 1 and i - 2 >= 0:
                                        if self.board[j + 2][i - 2].color == Color.EMPTY:
                                            return(True)
                    else:
                        continue
                elif self.type_of(i, j) == Dam:
                    if self.board[j][i].color == tu:
                        if self.board[j][i].color == Color.WHITE:
                            for c in range(n):
                                if j + c <= n - 1 and i + c <= n - 1:
                                    if self.board[j + c][i + c].color == Color.BLACK:
                                        if j + (c + 1) <= n - 1 and i + (c + 1) <= n - 1:
                                            if self.board[j + (c + 1)][i + (c + 1)].color == Color.EMPTY:
                                                return(True)
                                            else:
                                                return(False)
                                if j + c <= n - 1 and i - c >= 0:
                                    if self.board[j + c][i - c].color == Color.BLACK:
                                        if j + (c + 1) <= n - 1 and i - (c + 1) >= 0:
                                            if self.board[j + (c + 1)][i - (c + 1)].color == Color.EMPTY:
                                                return(True)
                                            else:
                                                return(False)
                                if j - c >= 0 and i + c <= n - 1:
                                    if self.board[j - c][i + c].color == Color.BLACK:
                                        if j - (c + 1) >= 0 and i + (c + 1) <= n - 1:
                                            if self.board[j - (c + 1)][i + (c + 1)].color == Color.EMPTY:
                                                return(True)
                                            else:
                                                return(False)
                                if j - c >= 0 and i - c >= 0:
                                    if self.board[j - c][i - c].color == Color.BLACK:
                                        if j - (c + 1) >= 0 and i - (c + 1) >= 0:
                                            if self.board[j - (c + 1)][i - (c + 1)].color == Color.EMPTY:
                                                return(True)
                                            else:
                                                return(False)
                        elif self.board[j][i].color == Color.BLACK:
                            for c in range(n):
                                if j + c <= n - 1 and i + c <= n - 1:
                                    if self.board[j + c][i + c].color == Color.WHITE:
                                        if j + (c + 1) <= n - 1 and i + (c + 1) <= n - 1:
                                            if self.board[j + (c + 1)][i + (c + 1)].color == Color.EMPTY:
                                                return(True)
                                            else:
                                                return(False)
                                if j + c <= n - 1 and i - c >= 0:
                                    if self.board[j + c][i - c].color == Color.WHITE:
                                        if j + (c + 1) <= n - 1 and i - (c + 1) >= 0:
                                            if self.board[j + (c + 1)][i - (c + 1)].color == Color.EMPTY:
                                                return(True)
                                            else:
                                                return(False)
                                if j - c >= 0 and i + c <= n - 1:
                                    if self.board[j - c][i + c].color == Color.WHITE:
                                        if j - (c + 1) >= 0 and i + (c + 1) <= n - 1:
                                            if self.board[j - (c + 1)][i + (c + 1)].color == Color.EMPTY:
                                                return(True)
                                            else:
                                                return(False)
                                if j - c >= 0 and i - c >= 0:
                                    if self.board[j - c][i - c].color == Color.WHITE:
                                        if j - (c + 1) >= 0 and i - (c + 1) >= 0:
                                            if self.board[j - (c + 1)][i - (c + 1)].color == Color.EMPTY:
                                                return(True)
                                            else:
                                                return(False)
        return(False)
type_choice = 0

message = IntVar()
var = IntVar()

message_label = Label(text='Выберите размер', fg='white', bg='#00032F', font='Verdana 20')
message_label.place(relx=.2, rely=.1, anchor='c')
message_entry = Entry(textvariable=message, width=20, font='Verdana 20')
message_entry.delete(0, END); message_entry.insert(0, 8)
message_entry.place(relx=.5, rely=.1, anchor="c")


norm_check = Radiobutton(text='Обычная игра', value=1, variable=var, font='Verdana 20')
norm_check.place(relx=.5, rely=.2, anchor="c")

pod_check = Radiobutton(text='Поддавки', value=2, variable=var, font='Verdana 20')
pod_check.place(relx=.5, rely=.3, anchor="c")

message_button = Button(text="Начать игру", command=get_n, font='Verdana 20')
message_button.place(relx=.5, rely=.5, anchor="c")

canv.tag_bind('rect', '<Button-1>', rect_func)
canv.tag_bind('prev', '<Button-1>', prev_board)
canv.tag_bind('oval', '<Button-1>', oval_func)
canv.tag_bind('button', '<Button-1>', zad_resh)
canv.tag_bind('button1', '<Button-1>', zad_gen)
canv.tag_bind('start_b', '<Button-1>', start_pos)


