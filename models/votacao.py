class Votacao:
    def __init__(self):
        self.votos = {
            "Candidato A": 0,
            "Candidato B": 0
        }
        self.votantes = set()

    def registrar_voto(self, cpf, candidato_id):
        if cpf in self.votantes:
            return "Você já votou."

        if candidato_id == 1:
            self.votos["Candidato A"] += 1
        elif candidato_id == 2:
            self.votos["Candidato B"] += 1
        else:
            return "Número do candidato inválido."

        self.votantes.add(cpf)
        return "Voto registrado."

    def exportar_resultados(self):
        import json
        return json.dumps(self.votos)
