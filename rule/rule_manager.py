import json
import os

class RuleManager:
    def __init__(self, filepath='rule.json'):
        self.filepath = filepath
        self.rules = self.load_rules()

    def load_rules(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as file:
                return json.load(file).get("rules", [])
        else:
            return []

    def save_rules(self):
        with open(self.filepath, 'w') as file:
            json.dump({"rules": self.rules}, file, indent=4)

    def get_enabled_rules(self):
        return [rule for rule in self.rules if rule["enabled"]]

    def add_rule(self, rule):
        self.rules.append(rule)
        self.save_rules()

    def delete_rule(self, rule_id):
        self.rules = [rule for rule in self.rules if rule["id"] != rule_id]
        self.save_rules()

    def update_rule(self, rule_id, updated_rule):
        for rule in self.rules:
            if rule["id"] == rule_id:
                rule.update(updated_rule)
                break
        self.save_rules()

    def get_all_rules(self):
        return self.rules
