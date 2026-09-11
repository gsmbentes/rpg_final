"""
game.py
-------
Controle do jogo (Pygame): janela, loop principal, eventos, estados de
turno e desenho de tudo na tela. É o único arquivo que "junta" as outras
camadas:

    entidades.py -> personagens e regras de combate (POO original)
    combate.py   -> ordem dos turnos
    sprites.py   -> desenho e animação dos personagens
    ui.py        -> botões e barra de vida

Estados do jogo (máquina de estados simples, por tempo em milissegundos):
    AGUARDANDO_JOGADOR -> espera o jogador clicar em um botão
    PROCESSANDO_JOGADOR -> anima a ação do jogador por um tempinho
    PROCESSANDO_INIMIGO -> anima a ação automática do inimigo
    FIM_DE_JOGO -> mostra tela de vitória/derrota
"""

import sys
import pygame

from entidades import Heroi, Mago
from combate import Combate
from sprites import PersonagemSprite
from ui import Botao, desenhar_barra_vida, desenhar_texto_centralizado

LARGURA, ALTURA = 900, 620
FPS = 60

COR_CEU_TOPO = (40, 30, 70)
COR_CEU_BASE = (90, 60, 110)
COR_CHAO = (60, 45, 40)
COR_CHAO_LINHA = (80, 60, 55)
BRANCO = (255, 255, 255)
PRETO = (10, 10, 10)
DOURADO = (240, 200, 90)
CINZA_LOG = (25, 25, 32)

DURACAO_TRANSICAO_MS = 650  # tempo de "pausa" para a animação ser vista antes de trocar o turno


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("RPG de Luta")
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        self.relogio = pygame.time.Clock()

        self.fonte_titulo = pygame.font.SysFont("arialblack", 34)
        self.fonte_grande = pygame.font.SysFont("arial", 26, bold=True)
        self.fonte_media = pygame.font.SysFont("arial", 20, bold=True)
        self.fonte_pequena = pygame.font.SysFont("arial", 16)
        self.fonte_botao = pygame.font.SysFont("arial", 20, bold=True)
        self.fonte_dano = pygame.font.SysFont("arial", 22, bold=True)

        self._novo_jogo()

    # ---------------------------------------------------------------
    # Configuração de uma nova partida (também usado para "jogar de novo")
    # ---------------------------------------------------------------
    def _novo_jogo(self):
        self.jogador = Heroi("Gustavo Guerreiro", poder=15)
        self.inimigo = Mago("Sombra Arcana", magia=40)

        self.combate = Combate(self.jogador, self.inimigo)

        self.sprite_jogador = PersonagemSprite(
            self.jogador, tipo="heroi", x=190, y=430,
            cor_primaria=(195, 60, 60), cor_secundaria=(140, 40, 40), virado=False,
        )
        self.sprite_inimigo = PersonagemSprite(
            self.inimigo, tipo="mago", x=710, y=430,
            cor_primaria=(70, 90, 205), cor_secundaria=(45, 60, 150), virado=True,
        )

        self.estado = "AGUARDANDO_JOGADOR"
        self.temporizador = 0

        self._criar_botoes()

    def _criar_botoes(self):
        largura_botao, altura_botao = 170, 55
        espaco = 30
        total = 3 * largura_botao + 2 * espaco
        x_inicial = (LARGURA - total) // 2
        y = 535

        self.botoes = [
            Botao((x_inicial, y, largura_botao, altura_botao), "ATACAR", self._acao_atacar,
                  cor=(170, 60, 60), cor_hover=(205, 80, 80)),
            Botao((x_inicial + largura_botao + espaco, y, largura_botao, altura_botao), "DEFENDER",
                  self._acao_defender, cor=(60, 110, 170), cor_hover=(80, 135, 205)),
            Botao((x_inicial + 2 * (largura_botao + espaco), y, largura_botao, altura_botao), "POÇÃO",
                  self._acao_pocao, cor=(60, 150, 90), cor_hover=(80, 180, 110)),
        ]

    # ---------------------------------------------------------------
    # Ações dos botões (só funcionam se for o turno do jogador)
    # ---------------------------------------------------------------
    def _pode_agir(self):
        return self.estado == "AGUARDANDO_JOGADOR" and self.combate.turno_jogador and not self.combate.finalizado

    def _acao_atacar(self):
        if not self._pode_agir():
            return
        dano = self.combate.jogador_atacar()
        self.sprite_jogador.tocar_ataque()
        self.sprite_inimigo.tocar_dano(dano)
        self._iniciar_transicao("PROCESSANDO_JOGADOR")

    def _acao_defender(self):
        if not self._pode_agir():
            return
        self.combate.jogador_defender()
        self._iniciar_transicao("PROCESSANDO_JOGADOR")

    def _acao_pocao(self):
        if not self._pode_agir():
            return
        cura = self.combate.jogador_usar_pocao()
        if cura > 0:
            self.sprite_jogador.tocar_cura(cura)
        self._iniciar_transicao("PROCESSANDO_JOGADOR")

    def _iniciar_transicao(self, novo_estado):
        self.estado = novo_estado
        self.temporizador = DURACAO_TRANSICAO_MS
        for botao in self.botoes:
            botao.habilitado = False

    # ---------------------------------------------------------------
    # Loop principal
    # ---------------------------------------------------------------
    def executar(self):
        while True:
            dt = self.relogio.tick(FPS)
            self._processar_eventos()
            self._atualizar(dt)
            self._desenhar()
            pygame.display.flip()

    def _processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r and self.estado == "FIM_DE_JOGO":
                self._novo_jogo()

            for botao in self.botoes:
                botao.lidar_evento(evento)

            if self.estado == "FIM_DE_JOGO" and hasattr(self, "botao_reiniciar"):
                self.botao_reiniciar.lidar_evento(evento)

    def _atualizar(self, dt):
        self.sprite_jogador.atualizar(dt)
        self.sprite_inimigo.atualizar(dt)

        if self.estado in ("PROCESSANDO_JOGADOR", "PROCESSANDO_INIMIGO"):
            self.temporizador -= dt
            if self.temporizador <= 0:
                self._avancar_estado()

    def _avancar_estado(self):
        if self.combate.finalizado:
            self.estado = "FIM_DE_JOGO"
            self._criar_botao_reiniciar()
            return

        if self.estado == "PROCESSANDO_JOGADOR":
            self.combate.passar_turno()
            resultado = self.combate.turno_inimigo()

            if resultado is not None:
                if resultado["tipo"] == "atacar":
                    self.sprite_inimigo.tocar_ataque()
                    self.sprite_jogador.tocar_dano(resultado["dano"])
                self._iniciar_transicao("PROCESSANDO_INIMIGO")
            else:
                self._voltar_para_jogador()

        elif self.estado == "PROCESSANDO_INIMIGO":
            self.combate.passar_turno()
            if self.combate.finalizado:
                self.estado = "FIM_DE_JOGO"
                self._criar_botao_reiniciar()
            else:
                self._voltar_para_jogador()

    def _voltar_para_jogador(self):
        self.estado = "AGUARDANDO_JOGADOR"
        for botao in self.botoes:
            botao.habilitado = True

    def _criar_botao_reiniciar(self):
        largura, altura = 220, 55
        self.botao_reiniciar = Botao(
            ((LARGURA - largura) // 2, 430, largura, altura),
            "JOGAR NOVAMENTE", self._novo_jogo, cor=(90, 90, 200), cor_hover=(115, 115, 230),
        )

    # ---------------------------------------------------------------
    # Desenho
    # ---------------------------------------------------------------
    def _desenhar(self):
        self._desenhar_arena()
        self._desenhar_titulo()

        self._desenhar_info_personagem(self.jogador, x=190, alinhamento="left")
        self._desenhar_info_personagem(self.inimigo, x=710, alinhamento="right")

        self.sprite_jogador.desenhar(self.tela, self.fonte_dano)
        self.sprite_inimigo.desenhar(self.tela, self.fonte_dano)

        self._desenhar_indicador_turno()
        self._desenhar_log()

        for botao in self.botoes:
            botao.desenhar(self.tela, self.fonte_botao)

        if self.estado == "FIM_DE_JOGO":
            self._desenhar_fim_de_jogo()

    def _desenhar_arena(self):
        # céu em degradê simples
        for i in range(300):
            t = i / 300
            cor = [int(COR_CEU_TOPO[c] + (COR_CEU_BASE[c] - COR_CEU_TOPO[c]) * t) for c in range(3)]
            pygame.draw.line(self.tela, cor, (0, i), (LARGURA, i))

        # chão
        pygame.draw.rect(self.tela, COR_CHAO, (0, 300, LARGURA, ALTURA - 300))
        for x in range(0, LARGURA, 60):
            pygame.draw.line(self.tela, COR_CHAO_LINHA, (x, 300), (x - 40, ALTURA - 80), 1)

        # sombras dos personagens
        pygame.draw.ellipse(self.tela, (0, 0, 0, 80), (self.sprite_jogador.pos_base.x - 35, 435, 70, 18))
        pygame.draw.ellipse(self.tela, (0, 0, 0, 80), (self.sprite_inimigo.pos_base.x - 35, 435, 70, 18))

    def _desenhar_titulo(self):
        desenhar_texto_centralizado(self.tela, "RPG DE LUTA", self.fonte_titulo, DOURADO, (LARGURA // 2, 35))

    def _desenhar_info_personagem(self, personagem, x, alinhamento):
        largura_barra = 260
        y_nome = 75
        y_barra = 105

        nome_surf = self.fonte_grande.render(personagem.nome_persona, True, BRANCO)
        if alinhamento == "left":
            rect_nome = nome_surf.get_rect(midleft=(x - largura_barra // 2, y_nome))
            x_barra = x - largura_barra // 2
        else:
            rect_nome = nome_surf.get_rect(midright=(x + largura_barra // 2, y_nome))
            x_barra = x - largura_barra // 2
        self.tela.blit(nome_surf, rect_nome)

        desenhar_barra_vida(self.tela, x_barra, y_barra, largura_barra, 28,
                             personagem.vida, personagem.vida_maxima, self.fonte_pequena)

        pocoes_txt = self.fonte_pequena.render(f"🧪 x{personagem.pocoes}", True, (200, 230, 200))
        self.tela.blit(pocoes_txt, (x_barra, y_barra + 32))

    def _desenhar_indicador_turno(self):
        if self.combate.finalizado:
            return
        if self.combate.turno_jogador:
            texto, cor = f"Turno de {self.jogador.nome_persona}", (120, 220, 140)
        else:
            texto, cor = f"Turno de {self.inimigo.nome_persona}", (220, 120, 120)
        desenhar_texto_centralizado(self.tela, texto, self.fonte_media, cor, (LARGURA // 2, 175))

    def _desenhar_log(self):
        rect_log = pygame.Rect(60, 380, LARGURA - 120, 40)
        pygame.draw.rect(self.tela, CINZA_LOG, rect_log, border_radius=8)
        pygame.draw.rect(self.tela, (90, 90, 100), rect_log, width=1, border_radius=8)

        if self.combate.mensagens:
            ultima = self.combate.mensagens[-1]
            desenhar_texto_centralizado(self.tela, ultima, self.fonte_pequena, BRANCO, rect_log.center)

    def _desenhar_fim_de_jogo(self):
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.tela.blit(overlay, (0, 0))

        venceu_jogador = self.combate.vencedor is self.jogador
        texto = "VITÓRIA!" if venceu_jogador else "DERROTA!"
        cor = (120, 230, 140) if venceu_jogador else (230, 90, 90)

        desenhar_texto_centralizado(self.tela, texto, self.fonte_titulo, cor, (LARGURA // 2, 320))
        desenhar_texto_centralizado(
            self.tela, f"{self.combate.vencedor.nome_persona} venceu o combate!",
            self.fonte_media, BRANCO, (LARGURA // 2, 370),
        )

        if hasattr(self, "botao_reiniciar"):
            self.botao_reiniciar.desenhar(self.tela, self.fonte_botao)
