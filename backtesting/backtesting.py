import sys
sys.path.append('../helpers')
import finance_helpers as fin
from datetime import date, timedelta


class Ruleset:
    def __init__(self, rules_dict):
        self.rules = rules_dict


    def add_rule(self, rule_id, rule, overwrite=False):
        if rule_id in self.rules and not overwrite:
            print("Overwrite detected. Switch overwrite on to replace rule.")
        else:
            self.rules[rule_id] = rule


    def del_rule(self, rule_id):
        try:
            del(self.rules[rule_id])
        except KeyError:
            print("Rule " + rule_id + " does not exist.")


    def execute(self, portfolio, day):
        new_port = portfolio
        for rule in self.rules:
            new_port = self.rules[rule](new_port, day)
        return new_port


class Backtester:
    def __init__(self, ruleset):
        self.ruleset = ruleset


    def execute(self, portfolio, start, end=date.today()):
        new_port = portfolio
        for day in [start + timedelta(i) for i in \
            range((end - start + timedelta(1)).days)]:
            new_port = self.ruleset.execute(new_port, day)
        return new_port


class Portfolio:
    def __init__(self, portfolio_dict):
        self.sheet = portfolio_dict


    def update(self, key, val):
        if key not in self.sheet:
            raise KeyError(key + " is missing from the portfolio.")
        self.sheet[key] = val


    def transfer(self, frm, to, amount, rate):
        if frm not in self.sheet:
            raise KeyError(frm + " is missing from the portfolio.")
        if to not in self.sheet:
            raise KeyError(to + " is missing from the portfolio.")
        if self.sheet[frm] < amount:
            raise ValueError(frm + " cannot transfer sufficient funds.")
        self.update(to, self.sheet[to] + amount * rate)
        self.update(frm, self.sheet[frm] - amount)
