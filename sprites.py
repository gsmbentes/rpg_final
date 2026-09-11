"""
sprites.py
----------
Responsabilidade ÚNICA: desenhar e animar um personagem na tela.

`PersonagemSprite` NÃO decide dano, NÃO decide turnos, NÃO conhece as
regras de Heroi/Mago. Ele só guarda uma referência ao objeto de lógica
(`personagem`, vindo de entidades.py) para ler `nome_persona`, `vida`,
`vida_maxima` — e sabe como se desenhar e reagir visualmente quando o
jogo manda `tocar_ataque()` ou `tocar_dano()`.

Preparado para sprites PNG no futuro:
    Se `self.imagem` estiver definido (um `pygame.Surface` carregado com
    `pygame.image.load(...)`), o método `desenhar()` desenha essa imagem
    em vez das formas geométricas. Basta implementar `carregar_imagem()`
    (veja o exemplo comentado no final do arquivo) — nenhum outro código
    do jogo precisa mudar.
"""

import pygame

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (220, 60, 60)
AMARELO = (250, 220, 90)


class PersonagemSprite:
    """
    Sprite genérico. `tipo` define o desenho: "heroi" ou "mago".
    `virado` inverte o desenho horizontalmente (o inimigo fica de frente
    para o jogador).
    """

    LARGURA = 90
    ALTURA = 130

    def __init__(self, personagem, tipo, x, y, cor_primaria, cor_secundaria, virado=False):
        self.personagem = personagem       # objeto de lógica (Heroi/Mago)
        self.tipo = tipo                   # "heroi" ou "mago"
        self.pos_base = pygame.Vector2(x, y)  # posição de "descanso"
        self.pos = pygame.Vector2(x, y)       # posição atual (muda durante animação de ataque)
        self.cor_primaria = cor_primaria
        self.cor_secundaria = cor_secundaria
        self.virado = virado

        self.imagem = None  # no futuro: pygame.image.load("assets/personagens/xxx.png")

        # --- estado de animação de ataque ---
        self._atacando = False
        self._ataque_elapsed = 0
        self._ataque_duracao = 380  # ms
        self._ataque_distancia = 70 if not virado else -70

        # --- estado de "levar dano" ---
        self._piscando = False
        self._pisca_elapsed = 0
        self._pisca_duracao = 400  # ms

        # --- números de dano/cura flutuantes ---
        self._textos_flutuantes = []  # cada item: {"texto","cor","y_off","elapsed","duracao"}

    # ---------------- API chamada pelo game.py ----------------

    def tocar_ataque(self):
        self._atacando = True
        self._ataque_elapsed = 0

    def tocar_dano(self, valor):
        self._piscando = True
        self._pisca_elapsed = 0
        self._adicionar_texto_flutuante(f"-{valor}", VERMELHO)

    def tocar_cura(self, valor):
        self._adicionar_texto_flutuante(f"+{valor}", (90, 220, 120))

    def esta_animando(self):
        return self._atacando

    def _adicionar_texto_flutuante(self, texto, cor):
        self._textos_flutuantes.append({"texto": texto, "cor": cor, "y_off": 0, "elapsed": 0, "duracao": 900})

    # ---------------- atualização por frame ----------------

    def atualizar(self, dt_ms):
        if self._atacando:
            self._ataque_elapsed += dt_ms
            t = min(self._ataque_elapsed / self._ataque_duracao, 1.0)
            # curva "vai e volta": sobe até o meio, desce até o fim (triangular)
            avanco = (1 - abs(2 * t - 1)) * self._ataque_distancia
            self.pos.x = self.pos_base.x + avanco
            if t >= 1.0:
                self._atacando = False
                self.pos.x = self.pos_base.x

        if self._piscando:
            self._pisca_elapsed += dt_ms
            if self._pisca_elapsed >= self._pisca_duracao:
                self._piscando = False

        for texto in self._textos_flutuantes:
            texto["elapsed"] += dt_ms
            texto["y_off"] = -40 * (texto["elapsed"] / texto["duracao"])
        self._textos_flutuantes = [t for t in self._textos_flutuantes if t["elapsed"] < t["duracao"]]

    # ---------------- desenho ----------------

    def desenhar(self, tela, fonte_pequena):
        if self.imagem is not None:
            rect = self.imagem.get_rect(midbottom=(self.pos.x, self.pos.y))
            tela.blit(self.imagem, rect)
        else:
            cor = BRANCO if (self._piscando and (self._pisca_elapsed // 60) % 2 == 0) else None
            if self.tipo == "mago":
                self._desenhar_mago(tela, cor)
            else:
                self._desenhar_heroi(tela, cor)

        self._desenhar_textos_flutuantes(tela, fonte_pequena)

    def _desenhar_textos_flutuantes(self, tela, fonte):
        for texto in self._textos_flutuantes:
            alpha = max(0, 255 - int(255 * (texto["elapsed"] / texto["duracao"])))
            superficie = fonte.render(texto["texto"], True, texto["cor"])
            superficie.set_alpha(alpha)
            rect = superficie.get_rect(center=(self.pos.x, self.pos.y - 150 + texto["y_off"]))
            tela.blit(superficie, rect)

    def _desenhar_heroi(self, tela, cor_flash):
        cx, cy = self.pos.x, self.pos.y
        cor_corpo = cor_flash or self.cor_primaria
        cor_armadura = cor_flash or self.cor_secundaria

        # pernas
        pygame.draw.line(tela, PRETO, (cx - 12, cy - 10), (cx - 14, cy - 55), 10)
        pygame.draw.line(tela, PRETO, (cx + 12, cy - 10), (cx + 14, cy - 55), 10)

        # corpo (armadura)
        torso = pygame.Rect(0, 0, 44, 55)
        torso.center = (cx, cy - 80)
        pygame.draw.rect(tela, cor_armadura, torso, border_radius=8)

        # braços
        sinal = -1 if not self.virado else 1
        pygame.draw.line(tela, cor_corpo, (cx - 22, cy - 95), (cx - 22 + sinal * 18, cy - 60), 9)
        pygame.draw.line(tela, cor_corpo, (cx + 22, cy - 95), (cx + 22 + sinal * -6, cy - 55), 9)

        # cabeça
        pygame.draw.circle(tela, (240, 200, 160), (int(cx), int(cy - 115)), 20)
        # capacete
        pygame.draw.arc(tela, cor_armadura, (cx - 22, cy - 138, 44, 34), 3.4, 6.0, 6)

        # espada (linha da mão até a ponta) — inverte o lado se virado
        base_x = cx + (30 if not self.virado else -30)
        pygame.draw.line(tela, (210, 210, 220), (base_x, cy - 60), (base_x + (sinal * 40), cy - 130), 5)
        pygame.draw.line(tela, (150, 100, 40), (base_x, cy - 60), (base_x, cy - 45), 6)  # cabo

    def _desenhar_mago(self, tela, cor_flash):
        cx, cy = self.pos.x, self.pos.y
        cor_manto = cor_flash or self.cor_primaria
        cor_detalhe = cor_flash or self.cor_secundaria

        # manto (triângulo/polígono até o chão)
        pontos = [(cx, cy - 100), (cx - 38, cy - 5), (cx + 38, cy - 5)]
        pygame.draw.polygon(tela, cor_manto, pontos)

        # braços do manto
        sinal = -1 if not self.virado else 1
        pygame.draw.line(tela, cor_manto, (cx - 18, cy - 80), (cx - 18 + sinal * 20, cy - 45), 10)
        pygame.draw.line(tela, cor_manto, (cx + 18, cy - 80), (cx + 18 + sinal * -6, cy - 45), 10)

        # cabeça
        pygame.draw.circle(tela, (240, 200, 160), (int(cx), int(cy - 118)), 18)

        # chapéu pontudo
        chapeu = [(cx - 22, cy - 130), (cx + 22, cy - 130), (cx, cy - 175)]
        pygame.draw.polygon(tela, cor_detalhe, chapeu)
        pygame.draw.circle(tela, AMARELO, (int(cx), int(cy - 173)), 4)  # estrelinha na ponta

        # cajado
        base_x = cx + (32 if not self.virado else -32)
        pygame.draw.line(tela, (120, 80, 50), (base_x, cy - 20), (base_x, cy - 140), 5)
        pygame.draw.circle(tela, (120, 200, 255), (int(base_x), int(cy - 145)), 8)  # gema mágica

    # ---------------- exemplo de carregamento de PNG (futuro) ----------------
    #
    # def carregar_imagem(self, caminho):
    #     """Substitui o desenho vetorial por uma imagem PNG."""
    #     self.imagem = pygame.image.load(caminho).convert_alpha()
    #
    # Uso: sprite.carregar_imagem("assets/personagens/heroi.png")
