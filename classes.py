from itertools import combinations


class Player(object):
    def __init__(self, name, p_type):
        self.name = name
        self.p_type = p_type

    score = 0
    collect_min = 750  # collect_min is changed to 250 after scoring once

    # below is only used by computer players (self.p_type == "comp")

    roll_value = (341, 25, 50, 111, 230, 341)
    # roll_value assigns theoretical value of rolling x dice, where x is list index
    # index 0 and index 5 are both 341 because using all dice (0 remaining) restores all 5 dice
    success_rate = (0, 0.333, 0.556, 0.722, 0.843, 0.923)
    # percent success rate when rolling x dice, where x is list index

    def steal(self, steal_score, dice_left):
        cond1 = steal_score > 0
        cond2 = self.collect_min == 250
        cond3 = steal_score * self.success_rate[dice_left] > self.roll_value[5]
        if cond1 and cond2 and cond3:
            return(steal_score, dice_left)
        else:
            return(0, 5)

    def analyze(self, dice_list, dice_count, current_score, dice_left, max_score, endgame):
        cond1 = dice_list.count(1) == 0
        cond2 = dice_list.count(5) == 0
        cond3 = max(dice_count) < 3
        if cond1 and cond2 and cond3:
            return(0, 5, True, "There are no scoreable dice. "
                               "%s scores 0 points and ends their turn." % self.name)

        if ''.join(str(i) for i in dice_list) in ("12345", "23456"):
            options = [(''.join(str(i) for i in dice_list), 750)]
        else:
            options = []
            # options is a list of all individual scoreable dice sets
            # tuples in options are (dice string, point value integer)
            for i in range(6):
                if dice_count[i] > 0:
                    if i == 0:
                        if dice_count[i] < 3:
                            options += [("1", 100) for _ in range(dice_count[i])]
                        else:
                            options += ("1" * dice_count[i],
                                        1000 * 2 ** (dice_count[i] - 3)),
                    elif i == 4 and dice_count[i] < 3:
                        options += [("5", 50) for _ in range(dice_count[i])]
                    elif dice_count[i] >= 3:
                        options += (str(i + 1) * dice_count[i],
                                    100 * (i + 1) * 2 ** (dice_count[i] - 3)),

        # makes take_all option, for use if comp decides to pass dice
        take_all_score = sum([i[1] for i in options])
        take_all_str = ''.join([i[0] for i in options])
        print_take_all_str = ', '.join([i for i in take_all_str])

        # compares options and chooses best (single option bypasses)
        if len(options) > 1:
            top_score = 0
            for i in range(1, len(options) + 1):
                for combo in combinations(options, i):
                    score = 0
                    dice_str = ''
                    for each in combo:
                        score += each[1]
                        dice_str += each[0]
                    weighted_score = score + self.roll_value[-len(dice_str) - 1 -
                                                             (5 - len(dice_list))]
                    if weighted_score > top_score:
                        top_score = weighted_score
                        take_score = score
                        take_str = dice_str
        else:
            take_score = options[0][1]
            take_str = options[0][0]

        current_score += take_score
        dice_left -= len(take_str)
        if dice_left == 0:
            dice_left = 5
        print_take_str = ', '.join([i for i in take_str])

        # decision on whether to roll again or collect
        cond1 = endgame is True
        cond2 = current_score + self.score < max_score
        cond3 = current_score >= self.collect_min
        cond4 = current_score * (1 - self.success_rate[dice_left]) > self.roll_value[dice_left]
        if cond1 and cond2:
            end = False
            message = "%s takes %s." % (self.name, print_take_str)
        elif cond3 and cond4:
            current_score += take_all_score - take_score
            dice_left = (dice_left - len(take_all_str) + len(take_str))
            end = True
            message = "%s takes %s." % (self.name, print_take_all_str)
        else:
            end = False
            message = "%s takes %s." % (self.name, print_take_str)
        return(current_score, dice_left, end, message)
