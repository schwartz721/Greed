# Uses Unicode Box Drawing Light characters
# U+2500 - U+2518
# Uses Unicode Black Circle
# U+25cf

# show_dice function must be passed a list of integers between 1 and 6

one_thru_six = {
    0: ["┌───────┐",
        "│       │",
        "│ GREED │",
        "│       │",
        "└───────┘"],
    1: ["┌───────┐",
        "│       │",
        "│   ●   │",
        "│       │",
        "└───────┘"],

    2: ["┌───────┐",
        "│ ●     │",
        "│       │",
        "│     ● │",
        "└───────┘"],

    3: ["┌───────┐",
        "│ ●     │",
        "│   ●   │",
        "│     ● │",
        "└───────┘"],

    4: ["┌───────┐",
        "│ ●   ● │",
        "│       │",
        "│ ●   ● │",
        "└───────┘"],

    5: ["┌───────┐",
        "│ ●   ● │",
        "│   ●   │",
        "│ ●   ● │",
        "└───────┘"],

    6: ["┌───────┐",
        "│ ●   ● │",
        "│ ●   ● │",
        "│ ●   ● │",
        "└───────┘"]
}


def show_dice(dice_list):
    return ' ' + ''.join([('    '.join([one_thru_six[j][i] for j in dice_list]) + "\n ") for i in range(5)])


"""
def expanded_draw_dice(dice_list):
    output = ' '
    for i in range(5):
        for j in dice_list:
            output += one_thru_six[j][i] + '    '
        output += "\n "
    return output
"""


"""
# DEMO FUNCTION CALL
from random import randint
again = ''
while again == '':
    dice_list = []
    for i in range(int(input("How many dice? "))):
        dice_list.append(randint(1, 6))
    dice_list = sorted(dice_list)
    print(draw_dice(dice_list))
    again = input("To roll again, hit enter.\n"
                  "To exit, type anything and hit enter: ")
"""

# spin_dice function must be passed an integer
# nest function in loop with turn variable incrementing by 1

spinning = {
    0: ["┌───────┐",
        "│ ●   ● │",
        "│   ●   │",
        "│ ●   ● │",
        "└───────┘"],
    1: ["┌─┬─────┐",
        "│ │●   ●│",
        "│ │  ●  │",
        "│ │●   ●│",
        "└─┴─────┘"],
    2: ["┌───┬───┐",
        "│●  │● ●│",
        "│ ● │ ● │",
        "│  ●│● ●│",
        "└───┴───┘"],
    3: ["┌─────┬─┐",
        "│●    │ │",
        "│  ●  │ │",
        "│    ●│ │",
        "└─────┴─┘"],
    4: ["┌───────┐",
        "│ ●     │",
        "│   ●   │",
        "│     ● │",
        "└───────┘"],
    5: ["┌─┬─────┐",
        "│ │●    │",
        "│ │  ●  │",
        "│ │    ●│",
        "└─┴─────┘"],
    6: ["┌───┬───┐",
        "│●  │●  │",
        "│   │ ● │",
        "│  ●│  ●│",
        "└───┴───┘"],
    7: ["┌─────┬─┐",
        "│●    │ │",
        "│     │ │",
        "│    ●│ │",
        "└─────┴─┘"],
    8: ["┌───────┐",
        "│ ●     │",
        "│       │",
        "│     ● │",
        "└───────┘"],
    9: ["┌─┬─────┐",
        "│ │●    │",
        "│ │     │",
        "│ │    ●│",
        "└─┴─────┘"],
    10: ["┌───┬───┐",
         "│● ●│●  │",
         "│   │   │",
         "│● ●│  ●│",
         "└───┴───┘"],
    11: ["┌─────┬─┐",
         "│●   ●│ │",
         "│     │ │",
         "│●   ●│ │",
         "└─────┴─┘"],
    12: ["┌───────┐",
         "│ ●   ● │",
         "│       │",
         "│ ●   ● │",
         "└───────┘"],
    13: ["┌─┬─────┐",
         "│ │●   ●│",
         "│ │     │",
         "│ │●   ●│",
         "└─┴─────┘"],
    14: ["┌───┬───┐",
         "│● ●│● ●│",
         "│ ● │   │",
         "│● ●│● ●│",
         "└───┴───┘"],
    15: ["┌─────┬─┐",
         "│●   ●│ │",
         "│  ●  │ │",
         "│●   ●│ │",
         "└─────┴─┘"]
}


from time import sleep


def spin_dice(num_dice, tick):
    output = ' '
    for row in range(5):
        for sep in [i * 4 for i in range(num_dice)]:
            output += spinning[(tick + sep) % 16][row] + '    '
        output = output[:-4] + "\n "
    sleep(.1)
    return(output)


"""
# DEMO FUNCTION CALL
from tkinter import *
from time import sleep

class Window:
    def __init__(self, master):
        self.master = master
        master.title("Spinning Dice")
        master.geometry("500x100")

        self.text = StringVar()
        self.text_label = Label(master, textvariable=self.text, font="Consolas")
        self.text_label.pack()


root = Tk()
window = Window(root)
turn = 0
while 1:
    window.text.set(spin_dice(5))
    turn += 1
    root.update()
"""
