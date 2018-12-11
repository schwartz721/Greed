# A program for playing the dice game "Greed" with human and computer players

from random import randint
from draw_dice import show_dice, spin_dice
from time import sleep
import tkinter as tk
from classes import Player


class Window:

    # ---------------------------------  FRAME 1  ---------------------------------

    def __init__(self, master):
        self.master = master
        self.master.title("Setup")
        self.frame1 = tk.Frame(self.master)
        self.frame1.pack()

        self.comment_text = tk.StringVar()
        self.comment_label = tk.Label(self.frame1, textvariable=self.comment_text)
        self.comment_text.set("How many points will be required to win?")
        self.player_label = tk.Label(self.frame1, text="Players:")

        self.str_entry_text = tk.StringVar()
        self.str_entry = tk.Entry(self.frame1, textvariable=self.str_entry_text)

        self.entered_number = 0
        vcmd = self.frame1.register(self.validate)

        self.int_entry = tk.Entry(self.frame1, validate="key", validatecommand=(vcmd, "%P"))

        self.roster_text = tk.StringVar()
        self.roster_label = tk.Label(self.frame1, textvariable=self.roster_text)
        self.roster_text.set('')
        self.roster_str = ''

        self.b_submit_text = tk.StringVar()
        self.b_submit = tk.Button(self.frame1, textvariable=self.b_submit_text,
                                  command=lambda: self.submit())
        self.b_submit_text.set("Submit")

        self.player_list = []
        self.b_add_human = tk.Button(self.frame1, text="Add as Human player",
                                     command=lambda:
                                     self.add_player("human", self.str_entry_text.get()))
        self.b_add_comp = tk.Button(self.frame1, text="Add as Computer player",
                                    command=lambda:
                                    self.add_player("comp", self.str_entry_text.get()))

        # layout
        self.comment_label.grid(row=0, column=0, columnspan=3)
        self.int_entry.grid(row=2, column=0, columnspan=2)
        self.roster_label.grid(row=2, column=2)
        self.b_submit.grid(row=3, column=2)

    def add_player(self, human_comp, inp):
        name = inp.strip()
        if name == '':
            self.comment_text.set("Please give the player a name.")
            self.str_entry_text.set('')
            return
        elif name in self.roster_str:
            self.comment_text.set("Another player already has that name.")
            self.str_entry_text.set('')
            return
        else:
            if human_comp == "human":
                self.player_list.append(Player(name, "human"))
            else:
                self.player_list.append(Player(name, "comp"))
            self.comment_text.set("Enter a name and choose if the player is a Human or Computer.")
        self.roster_str += name + "\n"
        self.roster_text.set(self.roster_str)
        self.str_entry_text.set('')

    def validate(self, new_text):
        if not new_text:
            self.entered_number = 0
            return True
        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False

    def submit(self):
        if self.b_submit_text.get() == "Submit":
            self.win_condition = self.entered_number

            self.comment_text.set("Enter a name and choose if the player is a Human or Computer.")
            self.b_submit_text.set("Finish")

            self.int_entry.destroy()
            self.b_add_human.grid(row=3, column=0)
            self.b_add_comp.grid(row=3, column=1)
            self.player_label.grid(row=1, column=2)
            self.str_entry.grid(row=1, column=0, rowspan=2, columnspan=2)
        else:
            self.standings = [0] * len(self.player_list)
            self.frame1.destroy()
            self.master.title("Greed")
            self.frame2 = tk.Frame(self.master, height="200", width="700")
            [self.frame2.columnconfigure(i, minsize="90") for i in range(8)]
            self.frame2.pack()
            self.start_frame2()

    # ---------------------------------  FRAME 2  ---------------------------------

    def start_frame2(self):

        self.player_up_text = tk.StringVar()
        self.player_up_text.set("%s's" % (self.player_list[0].name))
        self.player_up_label = tk.Label(self.frame2, textvariable=self.player_up_text)
        self.player_up = tk.Label(self.frame2, text="Turn")

        self.current_score_text = tk.IntVar()
        self.current_score_label = tk.Label(self.frame2, textvariable=self.current_score_text)
        self.current_score = tk.Label(self.frame2, text="Round Score:")

        self.total_score_text = tk.IntVar()
        self.total_score_label = tk.Label(self.frame2, textvariable=self.total_score_text)
        self.total_score = tk.Label(self.frame2, text="Total Score:")

        self.standings_text = tk.StringVar()
        self.standings_text.set("Standings:")
        self.standings_label = tk.Label(self.frame2, textvariable=self.standings_text)
        self.standings_players_label = tk.Label(self.frame2, text=":\n".join(i.name for i
                                                in self.player_list) + ":", justify="right")
        self.standings_scores_text = tk.StringVar()
        self.standings_scores_text.set("\n".join(["0"] * len(self.player_list)))
        self.standings_scores_label = tk.Label(self.frame2, textvariable=self.standings_scores_text,
                                               justify="left")

        self.dice = tk.StringVar()
        self.dice.set(show_dice([0] * 5))
        self.dice_label = tk.Label(self.frame2, textvariable=self.dice, font="Consolas")

        self.cb0_var = tk.IntVar()
        self.cb0 = tk.Checkbutton(self.frame2, state="disabled", variable=self.cb0_var)
        self.cb1_var = tk.IntVar()
        self.cb1 = tk.Checkbutton(self.frame2, state="disabled", variable=self.cb1_var)
        self.cb2_var = tk.IntVar()
        self.cb2 = tk.Checkbutton(self.frame2, state="disabled", variable=self.cb2_var)
        self.cb3_var = tk.IntVar()
        self.cb3 = tk.Checkbutton(self.frame2, state="disabled", variable=self.cb3_var)
        self.cb4_var = tk.IntVar()
        self.cb4 = tk.Checkbutton(self.frame2, state="disabled", variable=self.cb4_var)
        self.cb_var_list = (self.cb0_var, self.cb1_var, self.cb2_var, self.cb3_var, self.cb4_var)
        self.cb_list = (self.cb0, self.cb1, self.cb2, self.cb3, self.cb4)

        self.comment_text = tk.StringVar()
        self.comment_label = tk.Label(self.frame2, textvariable=self.comment_text)

        self.start = tk.Button(self.frame2, text="Start Game", command=lambda: self.start_game())

        self.take = tk.Button(self.frame2, text="Take Dice", state="disabled",
                              command=lambda: self.take_dice(self.player_list[self.up]))
        self.b_roll = tk.Button(self.frame2, text="Roll", state="disabled",
                              command=lambda: self.roll_dice(self.player_list[self.up]))
        self.c_s_n_text = tk.StringVar()
        self.c_s_n = tk.Button(self.frame2, textvariable=self.c_s_n_text, state="disabled",
                               command=lambda: self.c_s_n_func(self.player_list[self.up],
                                                               self.player_list[(self.up + 1)
                                                               % len(self.player_list)]))
        self.c_s_n_text.set("Collect")

        # layout
        self.player_up_label.grid(row=0, column=0, sticky=tk.E)
        self.player_up.grid(row=0, column=1, sticky=tk.W)

        self.current_score.grid(row=0, column=2, sticky=tk.E)
        self.current_score_label.grid(row=0, column=3, sticky=tk.W)

        self.total_score.grid(row=0, column=4, sticky=tk.E)
        self.total_score_label.grid(row=0, column=5, sticky=tk.W)

        self.standings_label.grid(row=0, column=6, columnspan=2)
        self.standings_players_label.grid(row=1, column=6, rowspan=4, sticky=tk.NE)
        self.standings_scores_label.grid(row=1, column=7, rowspan=4, sticky=tk.NW)

        self.start.grid(row=1, column=0, columnspan=5)
        self.take.grid(row=1, column=5)

        self.cb0.grid(row=2, column=0)
        self.cb1.grid(row=2, column=1)
        self.cb2.grid(row=2, column=2)
        self.cb3.grid(row=2, column=3)
        self.cb4.grid(row=2, column=4)

        self.comment_label.grid(row=3, column=0, columnspan=6)

        self.b_roll.grid(row=4, column=0, columnspan=2)
        self.c_s_n.grid(row=4, column=2, columnspan=2)

    up = 0
    steal_score = 0
    dice_left = 5
    last_round = 0
    endgame = False
    sleep_time = 1

    def start_game(self):
        self.start.destroy()
        self.dice_label.grid(row=1, column=0, columnspan=5, sticky=tk.W)
        while self.player_list[self.up].p_type == "comp":
            self.comp_turn(self.player_list[self.up], self.steal_score, self.dice_left)
        self.setup_human_turn()

    def roll(self, num_dice):
        # roll is passed integer with number of dice
        # dice_count stores occurrences of each number in dice_list
        # if dice_list = [1, 1, 2, 4, 6] then dice_count = [2, 1, 0, 1, 0, 1]
        self.comment_text.set('')
        dice_list = sorted([randint(1, 6) for _ in range(num_dice)])
        dice_count = [dice_list.count(i) for i in range(1, 7)]
        for tick in range(12):
            self.dice.set(spin_dice(num_dice, tick))
            root.update()
        self.dice.set(show_dice(dice_list))
        root.update()
        return (dice_list, dice_count)

    def roll_dice(self, player):
        [i.deselect() for i in self.cb_list]
        self.c_s_n_text.set("Collect")
        self.c_s_n.config(state="disabled")
        self.b_roll.config(state="disabled")
        (player.dice_list, player.dice_count) = self.roll(player.dice_left)
        self.take.config(state="normal")
        cond1 = player.dice_list.count(1) == 0
        cond2 = player.dice_list.count(5) == 0
        cond3 = max(player.dice_count) < 3
        if cond1 and cond2 and cond3:
            self.comment_text.set("There are no scoreable dice. "
                                  "You score 0 points and your turn is over.")
            player.current_score = 0
            self.take.config(state="disabled")
            self.c_s_n_text.set("Next Player")
            self.c_s_n.config(state="normal")
            self.steal_score = 0
            self.dice_left = 5

    def score_take(self, take_list, take_count):
        # accepts a list, returns the point value sum of all dice taken
        if ''.join(str(i) for i in take_list) in ("12345", "23456"):
            return 750
        score = 0
        for i in range(6):
            if take_count[i] > 0:
                if i == 0:
                    if take_count[i] < 3:
                        score += take_count[i] * 100
                    else:
                        score += 1000 * 2 ** (take_count[i] - 3)
                elif i == 4 and take_count[i] < 3:
                    score += take_count[i] * 50
                else:
                    score += 100 * (i + 1) * 2 ** (take_count[i] - 3)
        return score

    def take_dice(self, player):
        self.take.config(state="disabled")
        take_list = [player.dice_list[i] for i in range(5) if self.cb_var_list[i].get() == 1]
        [i.deselect() for i in self.cb_list]
        take_count = [take_list.count(i) for i in range(1, 7)]

        if ''.join(str(i) for i in take_list) not in ["12345", "23456"]:
            for i in [1, 2, 3, 5]:
                if 0 < take_count[i] < 3:
                    self.comment_text.set("You can't take only (%d) %d's."
                                          % (take_count[i], i + 1))
                    self.take.config(state="normal")
                    return
                elif take_count == [0] * 6:
                    self.comment_text.set("You must take dice to continue.")
                    self.take.config(state="normal")
                    return

        player.dice_left -= len(take_list)
        if player.dice_left == 0:
            player.dice_left = 5
            [i.config(state="normal") for i in self.cb_list]
        else:
            [i.config(state="disabled") for i in self.cb_list[player.dice_left - 5:]]

        self.dice.set(show_dice([0] * player.dice_left))
        player.current_score += self.score_take(take_list, take_count)
        self.current_score_text.set(player.current_score)
        self.b_roll.config(state="normal")
        if player.current_score >= player.collect_min:
            self.comment_text.set("You can now choose to stop rolling and collect your points.")
            self.c_s_n.config(state="normal")
        else:
            self.comment_text.set("You must score a minimum of %d to collect your points."
                                  % player.collect_min)

    def end_turn(self, player, current_score, dice_left):
        self.b_roll.config(state="disabled")
        self.c_s_n.config(state="disabled")
        self.take.config(state="disabled")
        [i.config(state="disabled") for i in self.cb_list]
        player.score += current_score
        if current_score > 0:
            player.collect_min = 250
            self.comment_text.set("%s passes %d dice with %d points."
                                  % (player.name, dice_left, current_score))
            self.current_score_text.set(current_score)
            root.update()
            sleep(self.sleep_time)

        self.standings_scores_text.set("\n".join(str(i.score) for i in self.player_list))
        if player.score >= self.win_condition:
            self.endgame = True
            self.standings_text.set("Last Turn!")
        if self.endgame is True:
            self.last_round += 1
            if self.last_round == len(self.player_list):
                self.finish_game()
        self.steal_score = current_score
        self.dice_left = dice_left
        self.up = (self.up + 1) % len(self.player_list)
        self.player_up_text.set("%s's" % (self.player_list[self.up].name))
        self.current_score_text.set(0)
        self.total_score_text.set(self.player_list[self.up].score)
        self.c_s_n_text.set("Collect")
        root.update()

    def comp_turn(self, player, steal_score, dice_left):
        self.b_roll.config(state="disabled")
        self.take.config(state="disabled")
        self.c_s_n.config(state="disabled")
        [i.config(state="disabled") for i in self.cb_list]

        (current_score, dice_left) = player.steal(steal_score, dice_left)
        if current_score > 0:
            self.comment_text.set("%s has stolen the dice." % player.name)
        self.current_score_text.set(current_score)
        root.update()
        sleep(self.sleep_time)
        self.comment_text.set('')

        max_score = max([i.score for i in self.player_list])
        while True:
            (dice_list, dice_count) = self.roll(dice_left)
            sleep(self.sleep_time)
            (current_score, dice_left, end, message) = player.analyze(dice_list, dice_count,
                                                                      current_score, dice_left,
                                                                      max_score, self.endgame)
            self.comment_text.set(message)
            if end is True:
                root.update()
                sleep(self.sleep_time)
                break
            self.current_score_text.set(current_score)
            root.update()
            sleep(self.sleep_time)
        self.end_turn(player, current_score, dice_left)

    def setup_human_turn(self):
        self.b_roll.config(state="normal")
        self.c_s_n.config(state="disabled")
        self.take.config(state="disabled")
        [i.config(state="normal") for i in self.cb_list]
        player = self.player_list[self.up]
        player.dice_left = 5
        player.current_score = 0
        if self.steal_score > 0:
            if player.collect_min == 250:
                self.c_s_n_text.set("Steal")
                self.c_s_n.config(state="normal")
                self.comment_text.set("%s, do you want to steal %d dice with %d points?"
                                      % (player.name, self.dice_left, self.steal_score))
                self.dice.set(show_dice([0] * self.dice_left))
                self.c_s_n.config(state="normal")
            else:
                self.dice.set(show_dice([0] * 5))
                self.comment_text.set("%s, you can't steal dice until you have scored points."
                                      % player.name)
        else:
            self.dice.set(show_dice([0] * 5))

    def c_s_n_func(self, player, next_player):
        [i.deselect() for i in self.cb_list]
        self.comment_text.set('')

        # STEAL
        if self.c_s_n_text.get() == "Steal":
            player.dice_left = self.dice_left
            player.current_score = self.steal_score
            self.current_score_text.set(player.current_score)
            self.c_s_n_text.set("Collect")
            self.c_s_n.configure(state="disabled")
            if player.dice_left == 5:
                [i.config(state="normal") for i in self.cb_list]
            else:
                [i.config(state="disabled") for i in self.cb_list[player.dice_left - 5:]]

        # COLLECT / NEXT PLAYER
        else:
            self.end_turn(player, player.current_score, player.dice_left)
            while self.player_list[self.up].p_type == "comp":
                self.comp_turn(self.player_list[self.up], self.steal_score, self.dice_left)
            else:
                self.setup_human_turn()

    def finish_game(self):
        self.frame2.destroy()
        self.master.title("Results")
        self.frame3 = tk.Frame(self.master)
        self.frame3.pack()
        self.start_frame3()

    # ---------------------------------  FRAME 3  ---------------------------------

    def start_frame3(self):
        self.win_tie_text = tk.StringVar()
        self.win_tie_label = tk.Label(self.frame3, textvariable=self.win_tie_text)

        self.winner_text = tk.StringVar()
        self.winner_label = tk.Label(self.frame3, textvariable=self.winner_text)

        max_score = max([i.score for i in self.player_list])
        if [i.score for i in self.player_list].count(max_score) > 1:
            self.win_tie_text.set("There is a tie!\nThe winners are:")
        else:
            self.win_tie_text.set("The winner is:")

        self.winner_text.set(' & '.join([i.name for i in self.player_list if i.score == max_score]) + "!")

        standings = []
        players = []
        scores = []
        for _ in range(len(self.player_list)):
            ind = [i.score for i in self.player_list].index(max([i.score for i in self.player_list]))
            players.append(self.player_list[ind].name + ":")
            scores.append(str(self.player_list[ind].score))
            if scores.count(scores[-1]) > 1:
                standings.append('')
            else:
                standings.append(str(len(scores)) + ".")
            del self.player_list[ind]

        self.standings = tk.Label(self.frame3, text='\n'.join(standings), justify="right")
        self.standings_players = tk.Label(self.frame3, text="\n".join(players), justify="left")
        self.standings_scores = tk.Label(self.frame3, text="\n".join(scores), justify="left")
        self.standings_label = tk.Label(self.frame3, text="Standings:")

        self.die1 = tk.Label(self.frame3, text=show_dice([5]), font="Consolas")
        self.die2 = tk.Label(self.frame3, text=show_dice([2]), font="Consolas")
        self.die3 = tk.Label(self.frame3, text=show_dice([1]), font="Consolas")
        self.die4 = tk.Label(self.frame3, text=show_dice([4]), font="Consolas")
        self.die5 = tk.Label(self.frame3, text=show_dice([6]), font="Consolas")
        self.die6 = tk.Label(self.frame3, text=show_dice([3]), font="Consolas")

        # layout
        self.die1.grid(row=0, column=0)
        self.die2.grid(row=0, column=4)
        self.die3.grid(row=3, column=0)
        self.die4.grid(row=3, column=4)
        self.die5.grid(row=6, column=0)
        self.die6.grid(row=6, column=4)

        self.win_tie_label.grid(row=1, column=1, columnspan=3)
        self.winner_label.grid(row=2, column=1, columnspan=3)
        self.standings_label.grid(row=4, column=1, columnspan=3)
        self.standings.grid(row=5, column=1, sticky=tk.E)
        self.standings_players.grid(row=5, column=2, sticky=tk.W)
        self.standings_scores.grid(row=5, column=3, sticky=tk.W)


root = tk.Tk()
window = Window(root)
root.mainloop()
