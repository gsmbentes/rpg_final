
import random

MAX_MENSAGENS = 6


class Combate:
    def __init__(self, jogador, inimigo):
        self.jogador = jogador
        self.inimigo = inimigo
        self.turno_jogador = True
        self.mensagens = []
        self.finalizado = False
        self.vencedor = None

        self._registrar(f"{self.jogador.nome_persona} entra em campo contra {self.inimigo.nome_persona}!")

    # ---------- ações do jogador (chamadas pelos botões) ----------

    def jogador_atacar(self):
        """Executa o ataque do jogador e retorna o dano causado."""
        dano = self.jogador.atacar(self.inimigo)
        self._registrar(f"{self.jogador.nome_persona} atacou {self.inimigo.nome_persona} e causou {dano} de dano!")
        self._verificar_fim()
        return dano

    def jogador_defender(self):
        """Jogador entra em postura de defesa neste turno."""
        self.jogador.ativar_defesa()
        self._registrar(f"{self.jogador.nome_persona} se preparou para defender!")

    def jogador_usar_pocao(self):
        """Jogador usa uma poção. Retorna a cura real aplicada (0 se não houver poções)."""
        cura = self.jogador.usar_pocao()
        if cura > 0:
            self._registrar(f"{self.jogador.nome_persona} usou uma poção e recuperou {cura} de vida!")
        else:
            self._registrar(f"{self.jogador.nome_persona} não tem mais poções!")
        return cura

    # ---------- turno automático do inimigo ----------

    def turno_inimigo(self):
        """
        IA simples do inimigo: na maior parte das vezes ataca; às vezes
        se defende. Retorna um dicionário descrevendo o que aconteceu,
        para a camada visual poder animar o evento certo.
        """
        if self.finalizado:
            return None

        acao = random.choices(["atacar", "defender"], weights=[75, 25])[0]

        if acao == "atacar":
            dano = self.inimigo.atacar(self.jogador)
            self._registrar(f"{self.inimigo.nome_persona} atacou {self.jogador.nome_persona} e causou {dano} de dano!")
            resultado = {"tipo": "atacar", "dano": dano}
        else:
            self.inimigo.ativar_defesa()
            self._registrar(f"{self.inimigo.nome_persona} se preparou para defender!")
            resultado = {"tipo": "defender", "dano": 0}

        self._verificar_fim()
        return resultado

    # ---------- controle de turno / fim de jogo ----------

    def passar_turno(self):
        """Alterna de quem é a vez, se o combate ainda não acabou."""
        if not self.finalizado:
            self.turno_jogador = not self.turno_jogador

    def _verificar_fim(self):
        if not self.jogador.esta_vivo():
            self.finalizado = True
            self.vencedor = self.inimigo
            self._registrar(f"💀 {self.jogador.nome_persona} foi derrotado! {self.inimigo.nome_persona} venceu!")
        elif not self.inimigo.esta_vivo():
            self.finalizado = True
            self.vencedor = self.jogador
            self._registrar(f"🏆 {self.inimigo.nome_persona} foi derrotado! {self.jogador.nome_persona} venceu!")

    def _registrar(self, mensagem):
        self.mensagens.append(mensagem)
        if len(self.mensagens) > MAX_MENSAGENS:
            self.mensagens.pop(0)
