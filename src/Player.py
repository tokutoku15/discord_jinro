class Player():
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.is_alive = True
    def get_name(self):
        return self.name
    def get_id(self):
        return self.id
    def get_is_alive(self):
        return self.is_alive