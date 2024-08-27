# models/votacao.py
class Votacao:
    def __init__(self):
        self.votos = {1: 0, 2: 0}  # Considerando dois candidatos: 1 e 2

    def registrar_voto(self, candidato_id):
        if candidato_id in self.votos:
            self.votos[candidato_id] += 1
        else:
            raise ValueError("Candidato inválido")

    def resultados(self):
        return self.votos
