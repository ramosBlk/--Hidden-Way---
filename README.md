# 🎮 Hidden Way

**Hidden Way** é um jogo 2D de plataforma e aventura desenvolvido como projeto da disciplina **Programação para Jogos**, do curso de Ciência da Computação da UNIPAC.

O jogo foi inspirado em clássicos como **Fireboy and Watergirl (Fogo e Água)**, porém adaptado para uma experiência **single-player**, onde todos os desafios podem ser resolvidos utilizando apenas um personagem. 
---

## 📖 Sobre o jogo:

Em **Hidden Way**, o jogador deverá explorar diferentes fases, atravessar plataformas, evitar armadilhas e resolver desafios para encontrar o caminho até a saída de cada nível.

A dificuldade aumenta gradualmente conforme novas mecânicas e obstáculos são introduzidos, incentivando a exploração e o raciocínio do jogador.

---

## 🎯 Objetivo e mecânicas

Explore os cenários, pule entre plataformas, colete as chaves e alcance a saída. O jogo inclui:

- Movimentação lateral e pulo
- Plataformas e obstáculos
- Coleta de itens e interação com elementos do cenário
- Inimigos terrestres e voadores
- Progressão por três fases

### Fases

1. **Mapa 1:** tutorial, chave, baú e saída pela caverna.
2. **A Caverna:** colete as chaves, evite os perigos e encontre a saída.
3. **A Floresta Sombria:** atravesse as plataformas, enfrente inimigos e alcance o portal final.

---

## ✨ Diferencial

O grande diferencial do projeto é trazer a proposta de jogos como **Fireboy and Watergirl** para um modo **single-player**, mantendo a essência da exploração e da resolução de desafios, mas utilizando apenas um personagem. 
---

## 🛠️ Tecnologias

- Python
- Pygame-CE
- Git
- GitHub

## 🎮 Controles

- **A / D** ou **setas esquerda / direita:** mover
- **Espaço:** pular
- **W / S** ou **setas cima / baixo:** movimento vertical no menu inicial
- **E:** interagir com elementos, como o baú
- **F3:** exibir/ocultar as paredes de colisão nas fases compatíveis
- **ESC:** voltar ao seletor de fases (quando iniciado pelo teste direto)

---

## 📂 Estrutura do projeto

```
Hidden Way/
├── assets/          # Cenários, sprites, efeitos e itens
├── classes/         # Estados, entidades e sistemas do jogo
├── teste/           # Seletor de fases e editores de plataformas/paredes
├── main.py          # Inicialização normal do jogo
└── README.md
```

---

## 🚀 Como executar

1. Clone o repositório

```bash
git clone https://github.com/ramosBlk/--Hidden-Way---.git
```

2. Entre na pasta

```bash
cd --Hidden-Way---
```

3. Instale a dependência

```bash
pip install pygame-ce
```

4. Inicie o jogo pelo menu

```bash
python main.py
```

## 🧪 Testar fases e editar o mapa

Os arquivos em `teste/` são ferramentas gráficas independentes do menu principal.

### Abrir uma fase diretamente

```bash
python teste/test_fases.py
```

Pressione **1**, **2** ou **3** para iniciar a fase desejada sem percorrer as anteriores. Durante a fase, **ESC** retorna ao seletor; no seletor, **ESC** fecha a ferramenta.

### Editores de plataformas e paredes

Execute o editor correspondente:

```bash
python teste/test_plataforma_fase2.py
python teste/test_paredes_fase2.py
python teste/test_plataforma_fase3.py
python teste/test_paredes_fase3.py
```

Nos editores, use **TAB** para trocar de elemento, **N** para adicionar, **DELETE** para excluir, as **setas** para mover, **Q/E** para ajustar a largura e **A/D** para ajustar a altura. **ENTER** imprime as coordenadas no terminal.

Os editores não salvam as coordenadas automaticamente. Depois de exportá-las, copie a lista impressa para a configuração correspondente em `classes/systems/fases.py`.

---

## 👨‍💻 Equipe

- Pedro Henrique Faria Silva
- Pedro Henrique Ramos de Carvalho
- Raphael Antonio Ferreira
- Victor Hugo Silva de Assis 

---

## 📚 Projeto Acadêmico

___Desenvolvido para a disciplina **Programação para Jogos** do curso de **Ciência da Computação** do Centro Universitário Presidente Antônio Carlos (UNIPAC), sob orientação do professor **Rodrigo Fernandes dos Santos**.
