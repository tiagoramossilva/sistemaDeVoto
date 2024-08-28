from models.usuario import Usuario
from models.candidato import Candidato

class Votacao:
    def __init__(self):
        self.usuarios = {}  
        self.candidatos = {
            1: Candidato(1, "Candidato A: Biscoito"),
            2: Candidato(2, "Candidato B: Bolacha")
        }  

    def registrar_voto(self, cpf, candidato_id):
        if cpf in self.usuarios:
            usuario = self.usuarios[cpf]
            if usuario.votar():
                if candidato_id in self.candidatos:
                    self.candidatos[candidato_id].adicionar_voto()
                    return "Voto registrado com sucesso!"
                else:
                    return "Candidato inválido"
            else:
                return "Você já votou!"
        else:
            return "Usuário não registrado"

    def resultados(self):
        return {candidato.nome: candidato.votos for candidato in self.candidatos.values()}
