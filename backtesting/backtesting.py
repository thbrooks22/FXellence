import sys
sys.path.append('../helpers')
import finance_helpers as fin
from datetime import date, timedelta


class Ruleset:
    def __init__(self, rules_dict):
        if not isinstance(rules_dict, dict):
            raise TypeError("Argument must be of type 'dict.'")
        self.rules = rules_dict


    def add_rule(self, rule_id, rule, overwrite=False):
        if rule_id in self.rules and not overwrite:
            print("Overwrite detected. Switch overwrite on to replace rule.")
        else:
            self.rules[rule_id] = rule


    def del_rule(self, rule_id):
        if rule_id not in self.rules:
            raise KeyError("Rule " + str(rule_id) + " does not exist.")
        del(self.rules[rule_id])


    def execute(self, portfolio, day, memo):
        for rule in self.rules:
            memo, portfolio = self.rules[rule](portfolio, day, memo)
        return memo, portfolio




class Backtester:
    def __init__(self, ruleset):
        if not isinstance(ruleset, Ruleset):
            raise TypeError("Argument must be of type 'Ruleset.'")
        self.ruleset = ruleset


    def execute(self, portfolio, start, end=date.today()):
        memo = None
        for day in [start + timedelta(i) for i in \
            range((end - start + timedelta(1)).days)]:
            memo, portfolio = self.ruleset.execute(portfolio, day, memo)
        return portfolio



class Portfolio:
    def __init__(self, portfolio_dict):
        self.sheet = portfolio_dict


    def __repr__(self):
        return str(self.sheet)


    def open_position(self, key, val):
        if key in self.sheet:
            raise KeyError("Unable to open position for existing key " + key + ".")
        self.sheet[str(key)] = val


    def update(self, key, val):
        if key not in self.sheet:
            raise KeyError(key + " is missing from the portfolio.")
        self.sheet[str(key)] = val


    def transfer(self, frm, to, amount, rate):
        if frm not in self.sheet:
            raise KeyError(str(frm) + " is missing from the portfolio.")
        if to not in self.sheet:
            raise KeyError(str(to) + " is missing from the portfolio.")
        if self.sheet[frm] < amount:
            raise ValueError(str(frm) + " cannot transfer sufficient funds.")
        self.update(to, self.sheet[to] + amount * rate)
        self.update(frm, self.sheet[frm] - amount)
