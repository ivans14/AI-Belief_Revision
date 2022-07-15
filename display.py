from tkinter import *
import tkinter as tk

from beliefBase import BeliefBase, Belief
from settings import *


class Screen(Tk):
    def __init__(self):
        super().__init__()

        self.title('Belief Revision Agent')
        self.bind("<Key>", self.key_down)

        # Display variables
        self.displayText = StringVar()

        self.init_grid()

        self.temp_prop, self.temp_order = None, None
        self.beliefBase = BeliefBase()

    def init_grid(self):
        """
        Description:
            Initialize the grid corresponding to the display of the game. Here all the buttoms, frames,
            labels, etc. are defined and initialize.
        """
        window = Frame(self, bg=COLOR_PALETTE['background'])
        window.grid()

        displayCell = Frame(window, bg=COLOR_PALETTE['window'])
        displayCell.rowconfigure(0, minsize=300, weight=1)
        displayCell.columnconfigure(0, minsize=100, weight=1)
        displayCell.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky='ew')
        
        self.display = Label(displayCell, bg=COLOR_PALETTE['window'], textvariable=self.displayText, font=SUB_FONT)
        self.display.grid(sticky='n')

        # Input cell for propositions
        self.entryCell = Entry(window, bg=COLOR_PALETTE['window'], font=SUB_FONT, width=65)
        self.entryCell.grid(row=2, column=0, columnspan=2, padx=20, sticky='w')

        # Possible logic operators
        operatorFrame = Frame(window, bg=COLOR_PALETTE['background'])
        operators = ['NEG', 'OR', 'AND', '=>']
        operators_commands = [self.insertNEG, self.insertOR, self.insertAND,
                              self.insertIMPLICATION]
        for i, operator in enumerate(operators):
            button = Button(operatorFrame, bg=COLOR_PALETTE['buttoms'],
                            text=operator, command=operators_commands[i],
                            font=SUB_FONT_BOLD, relief=tk.RAISED)
            button.config(width = 5)
            button.grid(row=0, column=i, padx=5, pady=5)
        operatorFrame.grid(row=3, column=0, padx=15, pady=20, sticky='w')

        # Screen handler buttons
        clear_buttons_frame = Frame(window, bg=COLOR_PALETTE['background'])
        clear_buttons = ['CLEAR ONE', 'CLEAR ALL']
        clear_commands = [self.clear_idx, self.clear_all]
        for i, clear in enumerate(clear_buttons):
            button = Button(clear_buttons_frame, bg=COLOR_PALETTE['sub_buttoms'],
                            text=clear, command=clear_commands[i],
                            font=SUB_FONT_BOLD, relief=tk.RAISED)
            button.config(width = 10)
            button.grid(row=3, column=i, padx=5, pady=5)
        clear_buttons_frame.grid(row=3, column=1, padx=15, pady=20, sticky='e')
    
    # Main method for updating the display
    def run(self):
        self._update()
        self.update_idletasks()
        self.mainloop()

    # Key handler 
    def key_down(self, event):
        key = event.keysym
        if key == KEY_QUIT: exit()
        if key == KEY_ENTER:
            if len(self.entryCell.get()) != 0:
                self.get_entry()

    def _update(self):
        # Display
        self.displayText.set('ENTER PROPOSITION TO REVISE THE BELIEF BASE SYSTEM \n"All beliefs are displayed with its corresponding order"\n--------------------------------------------------------------------------\n'+str(self.beliefBase))
        self.display.grid()

    def insertNEG(self):
        pos = self.entryCell.index(INSERT)
        self.entryCell.insert(pos,'~')
    
    def insertOR(self):
        pos = self.entryCell.index(INSERT)
        self.entryCell.insert(pos,'|')
    
    def insertAND(self):
        pos = self.entryCell.index(INSERT)
        self.entryCell.insert(pos,'&')

    def insertIMPLICATION(self):
        pos = self.entryCell.index(INSERT)
        self.entryCell.insert(pos,'>>')

    def clear_all(self):
        self.temp_prop, self.temp_order = None, None
        self.beliefBase.clear()
        self.run()

    def clear_idx(self):
        SubScreen(self, f'Select the belief to delete (1-{len(self.beliefBase)}) in ascending order: ', 1)
        self.run()

    def get_entry(self):
        self.temp_prop = (self.entryCell.get()).lower()
        SubScreen(self, 'Introduce the order of the proposition (0-1): ', 0)

    def get_sub_win_input(self, _in, type):
        if type == 0: # Order of the proposition will be the input
            self.entryCell.delete(0, END)
            self.temp_order = float(_in)
            temp_belief = Belief(self.temp_prop, self.temp_order)
            self.beliefBase.revise(temp_belief)
            self._update()
        elif type == 1:
            self.beliefBase.delete_belief_idx(int(_in)-1)
            self._update()
       

class SubScreen(Toplevel):
    """
    Sub-display for better understanding and design
    """
    def __init__(self, parent, label, type):
        super().__init__(parent)
        self.label = label
        self.type = type

        self.grid()
        self.bind("<Key>", self.key_down)

        self.init_grid()
        self.run()

    def init_grid(self):
        window = Frame(self, bg=COLOR_PALETTE['sub_background'])
        window.grid()

        self.name = Label(window, bg=COLOR_PALETTE['sub_background'], text=self.label, font=SUB_FONT)
        self.name.grid(padx=20, pady=10, sticky='w')
        self.entryCell = Entry(window, bg=COLOR_PALETTE['sub_window'], font=SUB_FONT, width=30)
        self.entryCell.grid(padx=20, pady=(0,10))

    def run(self):
        self.update_idletasks()
        self.mainloop()

    def key_down(self, event):
        key = event.keysym
        if key == KEY_QUIT: self.destroy()
        if key == KEY_ENTER: self.get_entry()

    def get_entry(self):
        self.content = self.entryCell.get()
        if len(self.content) != 0:
            whole_display.get_sub_win_input(self.content, self.type)
            self.destroy()



if __name__ == '__main__':
    whole_display = Screen()
    whole_display.run()


