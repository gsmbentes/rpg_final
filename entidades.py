"""
entidades.py
------------
Lógica pura do RPG (sem nenhuma dependência de Pygame).

Este arquivo preserva 100% das regras originais do seu `jogo.py`:
- Jogo (classe base): vida, ataque básico, defesa básica.
- Heroi: dano extra baseado em "poder", defesa com escudo (reduz dano fixo).
- Mago: dano baseado em "magia", defesa com barreira (reduz dano fixo).
"""


import random

class Jogo:
    """Classe base: atributos e regras comuns a qualquer personagem."""

    def __init__(self, nome_persona, vida_maxima=100, pocoes=3):
        self.vida_maxima = vida_maxima
        self.vida = vida_maxima
        self.nome_persona = nome_persona
        self.pocoes = pocoes
        self.defendendo = False  # True quando o personagem escolheu se defender neste turno

    def atacar(self, inimigo):
        """Ataque básico padrão para qualquer personagem."""
        dano = 10
        print(f"⚔️ {self.nome_persona} realiza um ataque básico!")
        return inimigo.defender(dano)

    def defender(self, dano):
        """
        Lógica central de dano: garante que a vida não fique negativa.

        Se o personagem ativou a postura de defesa neste turno
        (`ativar_defesa`), o dano recebido é reduzido pela metade.
        """
        if self.defendendo:
            dano = dano // 2
            print(f"🛡️ {self.nome_persona} estava se defendendo e reduziu o dano pela metade!")
            self.defendendo = False

        self.vida -= dano
        if self.vida < 0:
            self.vida = 0

        print(f"💥 {self.nome_persona} recebeu {dano} de dano! Vida restante: {self.vida}")
        return dano

    def ativar_defesa(self):
        """Ação de combate: entrar em postura de defesa neste turno."""
        self.defendendo = True
        print(f"🛡️ {self.nome_persona} entrou em posição de defesa!")

    def usar_pocao(self, cura=20):
        """Ação de combate: usa uma poção de cura, se ainda houver alguma disponível."""
        if self.pocoes <= 0:
            print(f"🚫 {self.nome_persona} não tem mais poções!")
            return 0

        self.pocoes -= 1
        vida_antes = self.vida
        self.vida = min(self.vida + cura, self.vida_maxima)
        cura_real = self.vida - vida_antes
        print(f"🧪 {self.nome_persona} usou uma poção e recuperou {cura_real} de vida!")
        return cura_real

    def esta_vivo(self):
        return self.vida > 0


class Heroi(Jogo):
    """Especialista em força física: dano extra por 'poder', defesa com escudo."""

    def __init__(self, nome_persona, poder, vida_maxima=100, pocoes=3):
        super().__init__(nome_persona, vida_maxima=vida_maxima, pocoes=pocoes)
        self.poder = poder

    def atacar(self, inimigo):
        """Ataque especial do Herói baseado em poder físico."""
        dano_base = random.randint(40, 60)
        bonus = random.randint(10, 30)
        dano_total = dano_base + bonus + (self.poder // 5)
        print(f"\n🔥 {self.nome_persona} usou FORÇA BRUTA!")
        return inimigo.defender(dano_total)

    def defender(self, dano):
        """Defesa com escudo: reduz o dano antes de aplicar à vida."""
        escudo = 20
        dano_final = dano - escudo
        if dano_final < 0:
            dano_final = 0

        print(f"🛡️ {self.nome_persona} usou o Escudo!")
        return super().defender(dano_final)


class Mago(Jogo):
    """Especialista em magia: dano baseado em 'magia', defesa com barreira."""

    def __init__(self, nome_persona, magia, vida_maxima=100, pocoes=3):
        super().__init__(nome_persona, vida_maxima=vida_maxima, pocoes=pocoes)
        self.magia = magia

    def atacar(self, inimigo):
        """Ataque especial do Mago baseado em poder mágico."""
        dano_base = random.randint(40, 60)
        bonus = random.randint(10, 30)
        dano_total = dano_base + bonus + (self.magia // 5)
        print(f"\n✨ {self.nome_persona} lançou uma MAGIA poderosa!")
        return inimigo.defender(dano_total)

    def defender(self, dano):
        """Defesa com barreira: absorção mágica de dano."""
        barreira = 30
        dano_final = dano - barreira
        if dano_final < 0:
            dano_final = 0

        print(f"🔮 {self.nome_persona} criou uma Barreira Mágica!")
        return super().defender(dano_final)
