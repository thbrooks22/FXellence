import finance_helpers as fin
from forex_helpers import rates_in_range
from datetime import date, timedelta


class Ruleset:
    def __init__(self, rules):
        self.rules = rules


    def add_rule(self, rule_id, rule, overwrite=False):
        if rule_id in self.rules and not overwrite:
            print("Overwrite detected. Switch overwrite on to proceed.")
        else:
            self.rules[rule_id] = rule


    def del_rule(self, rule_id):
        try:
            del(self.rules[rule_id])
        except KeyError:
            print("Rule " + rule_id + " does not exist.")


    def execute(self, portfolio, rate_sheet):
        new_port = portfolio
        for rule in self.rules:
            new_port = self.rules[rule](new_port, rate_sheet)
        return new_port


class Backtester:
    def __init__(self, ruleset):
        self.ruleset = ruleset

    def execute(self, portfolio, start, end=date.today()):
        new_port = portfolio
        for day in [start + timedelta(i) for i in \
            range((end - start + timedelta(1)).days)]:
            rate_sheet = #COMPLETE RATE SHEET CONSTRUCTION, should be efficient
            new_port = self.ruleset.execute(new_port, rate_sheet)
        return new_port
