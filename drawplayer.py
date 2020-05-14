class DrawPlayer:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'Player {self.name}'

    def __hash__(self):
        return hash(self.name)


SingletonDrawPlayer = DrawPlayer('Draw')
