# ⚔️ RPG de Combate em Python

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green?logo=python)
![Git](https://img.shields.io/badge/Git-Version%20Control-orange?logo=git)
![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)

Um pequeno RPG de combate desenvolvido em **Python** e **Pygame**, criado como projeto de estudo para praticar **Programação Orientada a Objetos (POO)**, lógica de programação, organização de código, desenvolvimento de jogos e utilização do Git/GitHub.

---

# 🎮 Sobre o projeto

Este projeto começou como um pequeno sistema de combate desenvolvido no **terminal**, com o objetivo principal de praticar conceitos de **Programação Orientada a Objetos em Python**.

A primeira versão possuía personagens capazes de atacar e defender, utilizando conceitos como classes, herança, métodos, atributos e polimorfismo.

Posteriormente, o projeto evoluiu para uma versão gráfica utilizando **Pygame**.

A lógica principal do jogo foi mantida e novas funcionalidades foram adicionadas para transformar o sistema inicial em um pequeno RPG de combate interativo.

O projeto atualmente possui:

- Sistema de personagens;
- Sistema de ataque;
- Sistema de dano;
- Dano aleatório;
- Sistema de defesa;
- Escudo do Herói;
- Barreira mágica do Mago;
- Sistema de vida;
- Sistema de poções;
- Sistema de turnos;
- Comportamento do inimigo;
- Sistema de vitória e derrota;
- Interface gráfica utilizando Pygame;
- Organização do projeto em diferentes módulos.

---

# 🧠 Minha participação no projeto

O principal objetivo deste projeto foi desenvolver e compreender a **lógica por trás do jogo**.

A parte visual foi utilizada como uma camada gráfica para apresentar essa lógica de forma interativa.

**As imagens, sprites e elementos gráficos utilizados no jogo não foram criados por mim.**
**Eu desenvolvi a lógica e utilizei IA como ferramenta de apoio para a parte visual.**

Meu foco foi principalmente na programação responsável pelo funcionamento do RPG, incluindo:

- Regras do combate;
- Classes dos personagens;
- Ataques;
- Defesa;
- Cálculo de dano;
- Sistema de vida;
- Sistema de poções;
- Turnos;
- Comportamento do inimigo;
- Condições de vitória e derrota;
- Organização da lógica em diferentes arquivos.

A interface gráfica foi integrada ao projeto para permitir que toda essa lógica pudesse ser utilizada de maneira visual.

Portanto, o foco deste projeto está muito mais na **programação e na lógica de funcionamento** do que na criação dos elementos artísticos.

---

# 🖥️ Parte visual

O projeto utiliza **Pygame** para criar a interface gráfica.

A parte visual permite representar as ações que acontecem na lógica do jogo, como:

- Ataques;
- Defesa;
- Vida dos personagens;
- Ações do jogador;
- Turnos;
- Resultado do combate;
- Elementos da interface.

É importante destacar que **não fui responsável pela criação das imagens e sprites utilizados na interface**.

O Pygame foi utilizado principalmente como uma forma de transformar a lógica que estava inicialmente no terminal em uma experiência gráfica e interativa.

---

# ⚔️ Sistema de combate

O sistema de combate é baseado em turnos.

Durante o combate, o jogador pode realizar ações com seu personagem enquanto o inimigo possui sua própria lógica de decisão.

As principais ações envolvem:

- Atacar;
- Defender;
- Utilizar poção.

O combate continua enquanto os personagens estiverem vivos.

Quando a vida de um personagem chega a `0`, ele é considerado derrotado.

---

# 🎲 Sistema de dano

O dano dos ataques não possui sempre o mesmo valor.

Foi utilizado o módulo `random` do Python para gerar valores aleatórios.

A fórmula utilizada pelo Herói é:

```python
dano_base = random.randint(40, 60)
bonus = random.randint(10, 30)
dano_total = dano_base + bonus + (self.poder // 5)
