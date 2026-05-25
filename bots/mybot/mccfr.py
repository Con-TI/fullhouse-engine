"""
On preflop: 
-> When we have no raises:
    - fold (Not a choice under BB)
    - check
    - min raise
    - 2x min raise
    - 3x min raise
    - all-in
-> When we have raises (condition on raise, 3 bet, >=4bet):
    - fold
    - call
    - min raise
    - 2x min raise
    - 3x min raise
    - all-in
For preflop, we condition on


On flop/turn/river:
-> When we have no raises:
    - check
    - min raise
    - 2x min raise
    - 3x min raise
    - all-in
-> When we have raises (condition on raise, 3 bet, >=4bet):
    - fold
    - call
    - min raise
    - 2x min raise
    - 3x min raise
    - all-in
"""

ABSTRACT_ACTIONS = [
    "fold", # fold
    "check", # check
    "call", # call
    "raise_1x", # min raise
    "raise_2x", # 2 min raise
    "raise_3x", # 3 min raise
    "all_in", # all in
]

def legal_abstract_actions(state):
    actions = []
    if state["can_check"]:
        actions.append("check")
    else:
        actions += ["fold", "call"]

    if state["your_stack"] > 0:
        actions += [
            "raise_1x",
            "raise_2x",
            "raise_3x",
            "all_in",
        ]
    return actions

def abstract_to_engine(action, state):
    if action == "fold":
        return {"action": "fold"}
    if action == "check":
        return {"action": "check"}
    if action == "call":
        return {"action": "call"}
    if action == "all_in":
        return {"action": "all_in"}
    
    min_raise = state["min_raise_to"]
    if action == "raise_1x":
        amt = min_raise
    elif action == "raise_2x":
        amt = min_raise * 2
    elif action == "raise_3x":
        amt = min_raise * 3
    else:
        return {"action": "fold"}

    amt = min(amt, state["your_stack"])
    return {
        "action": "raise",
        "amount": amt,
    }

def betting_level(state):
    aggressive = 0
    for a in state["action_log"]:
        if a["action"] in ("raise", "all_in"):
            aggressive += 1
    if aggressive == 0:
        return "open"
    if aggressive == 1:
        return "raised"
    if aggressive == 2:
        return "3bet"
    return "4bet+"

def stack_bucket(state):
    bb = max(state["current_bet"], 100)
    eff = min(p["stack"] for p in state["players"] if not p["is_folded"])
    eff_bb = eff / bb
    if eff_bb < 10:
        return "0-10"
    if eff_bb < 20:
        return "10-20"
    if eff_bb < 40:
        return "20-40"
    if eff_bb < 80:
        return "40-80"
    return "80+"

def position_bucket(state):
    seat = state["seat_to_act"]
    n = len(state["players"])
    if seat == 0:
        return "SB"
    if seat == 1:
        return "BB"
    if seat >= n - 2:
        return "UTG"
    return "MP" # everything else

RANKS = "23456789TJQKA"

def bucketing(street, players, cards):
    if street == "preflop":
        r1 = RANKS.index(cards[0][0])
        r2 = RANKS.index(cards[1][0])
        suited = cards[0][1] == cards[1][1]
        hi = max(r1, r2)
        lo = min(r1, r2)
        if hi == lo:
            return f"P{hi}"
        return f"{hi}_{lo}_{int(suited)}"
    elif street == "flop":
        ...
    elif street == "turn":
        ...
    elif street == "river":
        ...

def infoset_key(state):
    return "|".join([
        state["street"],
        bucketing(state[""],state[""],state["your_cards"]),
        stack_bucket(state),
        position_bucket(state),
        betting_level(state),
        str(len(state["players"])),
    ])
    
class Node:
    def __init__(self, actions):
        self.actions = actions
        self.regret_sum = {
            a: 0.0 for a in actions
        }
        self.strategy_sum = {
            a: 0.0 for a in actions
        }

    def strategy(self):
        positive = {a: max(r, 0) for a, r in self.regret_sum.items()}
        s = sum(positive.values())
        
        if s > 0:
            return {a: positive[a] / s for a in self.actions}
        n = len(self.actions)
        return {a: 1.0 / n for a in self.actions}
    
import pickle
pickle.dump(strategy_table)       