class cell:
    def __init__(self) -> None:
        self.status = False

    def is_alive(self):
        return self.status

    def set_death(self):
        self.status = False
        return self.status
        
    def set_alive(self):
        self.status = True
        return self.status