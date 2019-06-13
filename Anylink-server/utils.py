import os


class PathBuilder():
    """Util class for intuitivly join and walk through paths using operators overload"""

    def __init__(self, initial_path: str):
        """C'tor PathBuilder"""
        self.initial_path = initial_path
        self.current_path = self.initial_path

    def __add__(self, other: str) -> str:
        self.current_path = os.path.join(self.current_path, other)
        return self.current_path

    def __sub__(self, other: str) -> str:
        self.current_path = os.path.dirname(self.current_path)
        return self.current_path

    def __str__(self):
        return self.current_path

    def __repr__(self):
        return self.current_path
