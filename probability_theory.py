"""概率论"""


class Node:
    """节点"""

    def __init__(self, special_attribute=None):
        """初始化属性children和parents"""
        self.special_attribute = special_attribute
        if special_attribute == "start":
            self.children = []
        elif special_attribute == "end":
            self.parents = []
        else:
            self.parents = []
            self.children = []

    def add_child(self, child, to_probability):
        """添加子节点"""
        self.children.append({"child": child, "to_probability": to_probability})
        child.parents.append({"parent": self, "event_probability": self.event_probability(), "to_probability": to_probability})
    
    def event_probability(self):
        """计算节点的概率"""
        if self.special_attribute == "start":
            return 1
        probability = 0
        for parent in self.parents:
            probability += parent["event_probability"] * parent["to_probability"]
        return probability

    def __repr__(self):
        return self.__class__.__name__
