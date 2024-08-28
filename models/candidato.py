class Candidato:
    def __init__(self, id_candidato, nome):
        self.id_candidato = id_candidato
        self.nome = nome
        self.votos = 0

    def adicionar_voto(self):
        self.votos += 1
