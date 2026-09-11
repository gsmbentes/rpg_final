"""
ui.py
-----
Elementos de interface reutilizáveis: botões e barra de vida.
Não conhece regras de combate — só desenha e informa cliques.
"""

import pygame

BRANCO = (255, 255, 255)
PRETO = (20, 20, 20)
CINZA = (70, 70, 80)
CINZA_CLARO = (110, 110, 125)
VERDE_VIDA = (90, 200, 100)
AMARELO_VIDA = (230, 200, 60)
VERMELHO_VIDA = (210, 60, 60)
FUNDO_VIDA = (40, 40, 45)


class Botao:
    """Botão retangular clicável, com estado de hover e habilitado/desabilitado."""

    def __init__(self, rect, texto, callback, cor=(80, 90, 160), cor_hover=(105, 118, 200)):
        self.rect = pygame.Rect(rect)
        self.texto = texto
        self.callback = callback
        self.cor = cor
        self.cor_hover = cor_hover
        self.habilitado = True

    def lidar_evento(self, evento):
        if not self.habilitado:
            return
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(evento.pos):
                self.callback()

    def desenhar(self, tela, fonte):
        mouse_pos = pygame.mouse.get_pos()
        hover = self.habilitado and self.rect.collidepoint(mouse_pos)

        if not self.habilitado:
            cor = CINZA
        elif hover:
            cor = self.cor_hover
        else:
            cor = self.cor

        pygame.draw.rect(tela, cor, self.rect, border_radius=10)
        pygame.draw.rect(tela, BRANCO if self.habilitado else CINZA_CLARO, self.rect, width=2, border_radius=10)

        cor_texto = BRANCO if self.habilitado else CINZA_CLARO
        superficie = fonte.render(self.texto, True, cor_texto)
        rect_texto = superficie.get_rect(center=self.rect.center)
        tela.blit(superficie, rect_texto)


def desenhar_barra_vida(tela, x, y, largura, altura, vida, vida_maxima, fonte):
    """Desenha uma barra de vida com fundo, preenchimento colorido por porcentagem e texto."""
    proporcao = max(0, vida) / vida_maxima if vida_maxima else 0

    fundo = pygame.Rect(x, y, largura, altura)
    pygame.draw.rect(tela, FUNDO_VIDA, fundo, border_radius=6)

    if proporcao > 0.5:
        cor = VERDE_VIDA
    elif proporcao > 0.2:
        cor = AMARELO_VIDA
    else:
        cor = VERMELHO_VIDA

    preenchimento = pygame.Rect(x, y, int(largura * proporcao), altura)
    if preenchimento.width > 0:
        pygame.draw.rect(tela, cor, preenchimento, border_radius=6)

    pygame.draw.rect(tela, BRANCO, fundo, width=2, border_radius=6)

    texto = fonte.render(f"{max(0, vida)} / {vida_maxima} HP", True, BRANCO)
    rect_texto = texto.get_rect(center=fundo.center)
    tela.blit(texto, rect_texto)


def desenhar_texto_centralizado(tela, texto, fonte, cor, centro):
    superficie = fonte.render(texto, True, cor)
    rect = superficie.get_rect(center=centro)
    tela.blit(superficie, rect)
