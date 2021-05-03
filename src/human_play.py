from game import State
from pv_mcts import pv_mcts_action
from tensorflow.keras.models import load_model
from pathlib import Path
from threading import Thread
import tkinter as tk
from PIL import Image, ImageTk

class GameUI(tk.Frame):
    def __init__(self, master=None, model=None):
        tk.Frame.__init__(self, master)
        self.master.title('簡易将棋')
        self.state = State()
        self.select = -1
        self.dxy = ((0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1))

        self.next_action = pv_mcts_action(model, 0.0)

        self.images = [(None, None, None, None)]
        for i in range(1, 5):
            image = Image.open('piece{}.png'.format(i))
            self.images.append( (\
                ImageTk.PhotoImage(image), \
                ImageTk.PhotoImage(image.rotate(180)),\
                ImageTk.PhotoImage(image.resize((40,40))), \
                ImageTk.PhotoImage(image.resize((40,40)).rotate(180))\
                    ) )
        
        self.c = tk.Canvas(self, width = 240, height = 400, highlightthickness = 0)
        self.c.bind('<Button-1>', self.turn_of_human)
        self.c.pack()

        self.on_draw()

    def turn_of_human(self, event):
        if self.state.is_done():
            self.state = State()
            self.on_draw()
            return
        
        if not self.state.is_first_player():
            return

        captures = []
        for i in range(3):
            if self.state.pieces[12+i] >= 2: captures.append(1+i)
            if self.state.pieces[12+i] >= 1: captures.append(1+i)

        p = int(event.x/80) + int((event.y-40)/80) * 3
        if 40 <= event.y and event.y <= 360:
            select = p
        elif event.x < len(captures) * 40 and event.y > 360:
            select = 12 + int(event.x/40)
        else:
            return

        if self.select < 0:
            self.select = select
            self.on_draw()
            return
        
        action = -1
        if select < 12:
            if self.select < 12:
                action = self.state.position_to_action(p, self.position_to_direction(self.select, p))
            else:
                action = self.state.position_to_action(p, 8-1+captures[self.select-12])
        
        if not (action in self.state.legal_actions()):
            self.select = -1
            self.on_draw()
            return

        self.state = self.state.next(action)
        self.select = -1
        self.on_draw()

        self.master.after(1000, self.turn_of_ai)

    def turn_of_ai(self):
        if self.state.is_done():
            return

        action = self.next_action(self.state)

        self.state = self.state.next(action)
        self.on_draw()

    def position_to_direction(self, position_src, position_dst):
        dx = position_dst%3 - position_src%3
        dy = int(position_dst/3) - int(position_src/3)
        for i in range(8):
            if self.dxy[i][0] == dx and self.dxy[i][1] == dy:
                return i
        return 0
    
    def draw_piece(self, index, first_player, piece_type):
        x = (index%3)*80
        y = int(index/3)*80 + 40
        index = 0 if first_player else 1
        self.c.create_image(x, y, image=self.images[piece_type][index], anchor=tk.NW)

    def draw_capture(self, first_player, pieces):
        index, x, dx, y = (2, 0, 40, 360) if first_player else (3, 200, -40, 0)
        captures = []
        for i in range(3):
            if pieces[12+i] >= 2: captures.append(1+i)
            if pieces[12+i] >= 1: captures.append(1+i)
        for i in range(len(captures)):
            self.c.create_image(x+dx*i, y, image=self.images[captures[i]][index], anchor=tk.NW)

    def draw_cursor(self, x, y, size):
        self.c.create_line(x+1, y+1, x+size-1, y+1, width = 4.0, fill = '#FF0000')
        self.c.create_line(x+1, y+size-1, x+size-1, y+size-1, width = 4.0, fill = '#FF0000')
        self.c.create_line(x+1, y+1, x+1, y+size-1, width = 4.0, fill = '#FF0000')
        self.c.create_line(x+size-1, y+1, x+size-1, y+size-1, width = 4.0, fill = '#FF0000')

    def on_draw(self):
        self.c.delete('all')
        self.c.create_rectangle(0, 0, 240, 400, width = 0.0, fill = '#EDAA56')
        for i in range(1,3):
            self.c.create_line(i*80, 40, i*80, 360, width = 2.0, fill = '#000000')
        for i in range(5):
            self.c.create_line(0, 40+i*80, 240, 40+i*80, width = 2.0, fill = '#000000')

        for p in range(12):
            p0, p1 = (p, 11-p) if self.state.is_first_player() else (11-p, p)
            if self.state.pieces[p0] != 0:
                self.draw_piece(p, self.state.is_first_player(), self.state.pieces[p0])
            if self.state.enemy_pieces[p1] != 0:
                self.draw_piece(p, not self.state.is_first_player(), self.state.enemy_pieces[p1])

        self.draw_capture(self.state.is_first_player(), self.state.pieces)
        self.draw_capture(not self.state.is_first_player(), self.state.enemy_pieces)

        if 0 <= self.select and self.select < 12:
            self.draw_cursor(int(self.select%3)*80, int(self.select/3)*80+40, 80)
        elif 12 <= self.select:
            self.draw_cursor((self.select-12)*40, 360, 40)

model = load_model('./model/best.h5')
f = GameUI(model=model)
f.pack()
f.mainloop()