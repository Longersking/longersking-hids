from ahocorasick import Automaton

class StringMatcher:
    def __init__(self, rules):
        self.automaton = Automaton()
        for rule in rules:
            self.automaton.add_word(rule["pattern"], (rule["id"], rule["pattern"], rule["description"], rule["severity"]))
        self.automaton.make_automaton()

    def match(self, text):
        matches = []
        for end_index, (rule_id, pattern, description, severity) in self.automaton.iter(text):
            matches.append({"id": rule_id, "pattern": pattern, "description": description, "severity": severity})
        return matches
