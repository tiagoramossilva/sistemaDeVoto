class Candidato:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome
        self.votos = 0

    def adicionar_voto(self):
        self.votos += 1

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'votos': self.votos
        }

    @staticmethod
    def from_dict(data):
        candidato = Candidato(data['id'], data['nome'])
        candidato.votos = data['votos']
        return candidato
