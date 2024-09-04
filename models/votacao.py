from models.usuario import Usuario
from models.candidato import Candidato
import json

class Votacao:
    def __init__(self):
        self.resultados = {
            'Candidato A': 0,
            'Candidato B': 0
        }
        self.usuarios = {}  # Usado para rastrear usuários que já votaram

    def registrar_voto(self, cpf, candidato_id):
        if cpf in self.usuarios:
            return "Você já votou."
        
        if candidato_id == 1:
            candidato = 'Candidato A'
        elif candidato_id == 2:
            candidato = 'Candidato B'
        else:
            return "Candidato inválido."

        self.resultados[candidato] += 1
        self.usuarios[cpf] = True
        return f"Voto registrado: {candidato} agora tem {self.resultados[candidato]} votos."

    def exportar_resultados(self):
        """Exporta os resultados como uma string JSON."""
        return json.dumps(self.resultados)

    def importar_resultados(self, resultados_json):
        """Importa resultados a partir de uma string JSON."""
        self.resultados = json.loads(resultados_json)
