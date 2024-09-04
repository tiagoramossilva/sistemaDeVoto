class Candidato:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome
        self.votos = 0

    def adicionar_voto(self):
        self.votos += 1

    def to_dict(self):
        return {'id': self.id, 'nome': self.nome, 'votos': self.votos}

    @staticmethod
    def from_dict(dados):
        candidato = Candidato(dados['id'], dados['nome'])
        candidato.votos = dados['votos']
        return candidato

    def __str__(self):
        return f"{self.nome} - Votos: {self.votos}"
