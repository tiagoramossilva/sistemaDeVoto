class Usuario:
    def __init__(self, cpf):
        self.cpf = cpf
        self.votou = False

    def votar(self):
        if not self.votou:
            self.votou = True
            return True
        return False
