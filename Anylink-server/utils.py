import os
class PathBuilder():
    def __init__(self,initial_path):
        self.initial_path = initial_path
        self.current_path = self.initial_path

    def __add__(self, other):
        self.current_path = os.path.join(self.current_path,other)
    def __isub__(self, other):
        self.current_path = os.path.dirname(self.current_path)

    def __str__(self):
        return self.current_path
    def __repr__(self):
        return self.current_path