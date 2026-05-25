from collections import namedtuple

InfoSet = namedtuple("InfoSet", ["street", "position", "players", "eff_stack_bucket", "bet_level", 
        "hand_bucket", # done
        "board_bucket", 
        "legal_mask", # done
    ]
)

ACTION_FOLD      = 0
ACTION_CHECK     = 1
ACTION_CALL      = 2
ACTION_MIN_RAISE = 3
ACTION_2X_RAISE  = 4
ACTION_3X_RAISE  = 5
ACTION_ALLIN     = 6

ALL_ACTIONS = [ACTION_FOLD, ACTION_CHECK, ACTION_CALL, ACTION_MIN_RAISE, ACTION_2X_RAISE, ACTION_3X_RAISE, ACTION_ALLIN,]

def bucket_stack(eff_stack_bb):
    if eff_stack_bb <= 10:
        return "0_10"
    if eff_stack_bb <= 20:
        return "10_20"
    if eff_stack_bb <= 40:
        return "20_40"
    if eff_stack_bb <= 60:
        return "40_60"
    if eff_stack_bb <= 80:
        return "60_80"
    return "80_plus"

def betting_level(action_log):
    aggressive = 0
    for a in action_log:
        if a["action"] in ("raise", "all_in"):
            aggressive += 1
    if aggressive == 0:
        return "open"
    if aggressive == 1:
        return "raised"
    if aggressive == 2:
        return "3bet"
    return "4bet_plus"

def position_bucket(seat, dealer, players):
    rel = (seat - dealer) % players
    if players == 2:
        return ["sb", "bb"][rel]
    names = ["btn", "sb", "bb", "utg", "mp", "co"]
    return names[rel % len(names)]

infoset