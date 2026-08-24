# Plano de Projeto Colaborativo: A-Maze-ing (42) — Thamily & Guilherme

Este documento serve como guia estratégico e plano de ação para o desenvolvimento em dupla do projeto **A-Maze-ing**. Ele define a divisão de responsabilidades entre **Thamily** (focada em Design, Interface, Parser e I/O) e **Guilherme** (focado no Core, Algoritmos e Empacotamento), estabelece os contratos de comunicação do código e define um cronograma ágil para que ambos possam trabalhar de forma independente e sem bloqueios.

---

## 👥 Papéis e Responsabilidades

Para aproveitar ao máximo o potencial de cada um e garantir uma entrega rápida e robusta, as tarefas foram distribuídas de forma que **Thamily** domine a interação do usuário e a parte visual, enquanto **Guilherme** foca na engenharia de algoritmos e estrutura do pacote.

### 🎨 Thamily (UI/UX, Fluxo e I/O)
*   **Perfil**: Iniciante em Python, com grande interesse em design e experiência do usuário.
*   **Foco principal**: Construir a ponte entre o usuário e o código do Guilherme. É a oportunidade perfeita para consolidar lógica de programação essencial (estruturas de repetição `for`, condicionais `if/else`, leitura de arquivos e tratamento de erros).
*   **Suas Tarefas**:
    1.  **Parser do `config.txt`**: Escrever a lógica que lê o arquivo de configuração, ignorando comentários (`#`), extraindo as variáveis e tratando erros de forma robusta para evitar fechamentos inesperados (*crashes*).
    2.  **Renderizador ASCII Colorido**: Projetar a exibição visual do labirinto no terminal usando caracteres de bloco (como `█`) e cores ANSI, garantindo que o design fique limpo e agradável.
    3.  **Menu Interativo**: Implementar o loop de comandos do terminal (`[R]`, `[P]`, `[C]`, `[Q]`) para interagir com o labirinto em tempo real.
    4.  **Exportador Hexadecimal (`maze.txt`)**: Salvar a matriz resolvida no arquivo de saída final no formato hexadecimal exato exigido pelo projeto.

### 🧠 Guilherme (Core Algorítmico e DevOps)
*   **Perfil**: Alguma experiência prévia em Python.
*   **Foco principal**: Estruturação lógica, matemática dos grafos e conformidade do código com os padrões de avaliação da 42.
*   **Suas Tarefas**:
    1.  **Gerador Perfeito (DFS)**: Implementar o algoritmo *Recursive Backtracking* (DFS) para cavar o labirinto perfeito sem ciclos.
    2.  **Gerador Imperfeito (Pac-Man)**: Desenvolver a lógica para abrir o centro, os quatro cantos e derrubar paredes aleatórias para criar caminhos múltiplos.
    3.  **Solucionador BFS**: Implementar o algoritmo de busca em largura (*Breadth-First Search*) para encontrar e listar as coordenadas do caminho mais curto.
    4.  **Padrão "42"**: Criar a inserção lógica do padrão numérico "42" feito de células fechadas no centro do labirinto.
    5.  **Empacotamento (`pyproject.toml`)**: Configurar o módulo reutilizável `mazegen` para que seja instalável via `pip install .`.

---

## 🤝 O Contrato de Integração (API)

Este é o acordo de comunicação que permite que **Thamily** e **Guilherme** programem de forma 100% paralela. Uma vez definido esse contrato, nenhum dos dois precisa esperar o outro terminar para avançar no próprio código.

### 1. Como Guilherme entregará o Labirinto para Thamily
O gerador do Guilherme sempre entregará o labirinto como uma **lista de listas (matriz) de inteiros**.
*   Cada inteiro de `0` a `15` representa quais paredes de uma célula estão de pé, baseado em uma **máscara de bits (bitmask)**:
    *   `Norte`: +1 (Bit 0)
    *   `Leste`: +2 (Bit 1)
    *   `Sul`: +4 (Bit 2)
    *   `Oeste`: +8 (Bit 3)
*   **Para Thamily testar**: Você não precisa esperar os algoritmos do Guilherme! Crie uma matriz fictícia em seu arquivo `a_maze_ing.py` para programar seu renderizador ASCII:
    ```python
    # Matriz fictícia para Thamily testar a lógica de desenho:
    grid_teste = [
        [9,  5,  12],  # Linha 0 (Célula 0,0 tem paredes ao Norte e Oeste [1+8=9])
        [10, 15, 10],  # Linha 1 (Célula central 1,1 está totalmente fechada [15])
        [3,  5,  6 ]   # Linha 2
    ]
    ```

### 2. Como Guilherme entregará a Solução para Thamily
Para destacar o menor caminho na tela, o algoritmo de solução do Guilherme entregará uma **lista de coordenadas** (tuplas `(linha, coluna)`):
*   **Para Thamily testar**: Use uma lista de coordenadas de exemplo para programar o realce de cor do caminho:
    ```python
    caminho_teste = [(0,0), (0,1), (0,2), (1,2), (2,2)]
    ```
    Em sua função de renderização, basta verificar: `if (linha, coluna) in caminho_teste:` para pintar aquela célula com a cor de destaque (ex: verde).

---

## 🎯 Orientações de Desenvolvimento e Aprendizado

### 💡 Dicas Especiais para Thamily (Acelerando no Python)
Como você está iniciando agora, aqui estão práticas excelentes para treinar e acelerar sem medo:
1.  **Foco em Lógica Básica**: A sua parte é excelente porque usa as estruturas mais importantes de qualquer linguagem de programação: laços `for` (para percorrer a matriz e desenhar as linhas no terminal), condicionais `if/elif/else` (para decidir qual caractere ou cor imprimir dependendo das paredes da célula) e manipulação simples de arquivos com `with open()`.
2.  **Cores ANSI Nativas (Sem Instalações)**: Para pintar seu terminal do seu jeito, utilize sequências de escape ANSI. Veja como é simples em Python:
    ```python
    PAREDE_AZUL = "\033[1;34m"
    CAMINHO_VERDE = "\033[1;32m"
    RESET = "\033[0m"

    print(f"{PAREDE_AZUL}██████{RESET}")  # Desenha uma parede azul
    print(f"{CAMINHO_VERDE}  ••  {RESET}")  # Desenha o caminho verde
    ```
3.  **Prevenção de Bugs**: Ao ler o `config.txt`, use blocos `try/except` para lidar com arquivos que não existem ou valores quebrados. Isso garantirá uma nota excelente na avaliação por estabilidade do software.

### ⚙️ Dicas Especiais para Guilherme (Garantindo a Qualidade de Engenharia)
Sendo o desenvolvedor com alguma experiência e responsável pelo core, seu foco deve ser a precisão matemática e os requisitos estritos da 42:
1.  **Tipagem Estrita (mypy)**: Escreva todas as assinaturas de funções com *type hints* claros. O `mypy` não deve apontar nenhum erro de tipo. Exemplo:
    ```python
    def generate_maze(self, width: int, height: int) -> list[list[int]]:
    ```
2.  **Controle de Estilo (flake8)**: Garanta que todo o seu código siga estritamente a PEP 8. Evite linhas com mais de 79 caracteres e use docstrings coerentes (PEP 257) em todas as classes e funções.
3.  **Lógica Recursiva Sem Estouro de Pilha**: No DFS, use uma abordagem iterativa com uma pilha (`list` do Python) se o labirinto puder ser muito grande, evitando erros de *RecursionError*.
4.  **Isolamento no Pacote**: A lógica matemática do labirinto não deve fazer chamadas de `input()` ou `print()` no terminal. Ela deve apenas processar dados e retornar os objetos para que a Thamily decida como exibi-los.

---

## 📂 Esqueleto de Pastas do Repositório Git

Mantenham a estrutura de arquivos organizada da seguinte forma:

```text
a-maze-ing/
├── .gitignore               # Ignorar caches do Python, virtualenvs e builds
├── Makefile                 # Automação das tarefas (install, run, lint, debug)
├── README.md                # Documentação do projeto (requisitos e uso)
├── a_maze_ing.py            # Ponto de entrada do programa (Thamily trabalha aqui)
├── config.txt               # Configuração padrão de teste
├── pyproject.toml           # Metadados de empacotamento do módulo mazegen
│
├── mazegen/                 # Pacote reutilizável (Guilherme trabalha aqui)
│   ├── __init__.py          # Expõe a classe principal (ex: MazeGenerator)
│   ├── generator.py         # Lógica de geração (DFS, imperfeito, padrão 42)
│   ├── solver.py            # Solucionador BFS do menor caminho
│   └── utils.py             # Validações matemáticas de parede e coerência
│
└── tests/                   # Testes unitários do core algorítmico
```

---

## 📅 Cronograma de Trabalho em 4 Passos

Para que vocês consigam visualizar o progresso de forma simples e direta (sem depender de leitores de gráficos especiais que às vezes falham ou quebram o visual no GitHub), aqui está a linha do tempo do projeto representada de forma visual e em tabela:

| Passo | Atividade | Responsável | Duração | Visualização do Cronograma |
| :--- | :--- | :--- | :---: | :--- |
| **Passo 1** | Setup do Repositório e Alinhamento do Contrato | 👥 Dupla | 1 Dia | `█░░░░░░` (Dia 1) |
| **Passo 2** | Desenvolvimento do Visualizador e Parser | 🎨 Thamily | 3 Dias | `.███░░░` (Dias 2 a 4) |
| **Passo 2** | Desenvolvimento dos Algoritmos DFS e BFS | 🧠 Guilherme | 3 Dias | `.███░░░` (Dias 2 a 4) |
| **Passo 3** | Integração dos Sistemas (Fim do teste fictício) | 👥 Dupla | 1 Dia | `....█░░` (Dia 5) |
| **Passo 4** | Exportação Hexadecimal, Padrão 42 e Polimento | 👥 Dupla | 2 Dias | `.....██` (Dias 6 e 7) |

*Legenda: `█` representa dias ativos de trabalho; `.` representa dias anteriores ou posteriores.*

### 📌 Passo 1: Setup e Alinhamento (Dia 1)
*   **Juntos**: Criar o repositório Git, configurar o `.gitignore` e confirmar as variáveis do Contrato de API descritas acima.
*   **Thamily**: Criar a estrutura básica de arquivos na raiz e o `config.txt` inicial.
*   **Guilherme**: Configurar o ambiente local garantindo que o `mypy` e o `flake8` estejam instalados e configurados para rodar de forma simples.

### 📌 Passo 2: Desenvolvimento Isolado (Dias 2 a 4)
*   **Thamily**:
    *   Escrever a função de leitura (`parser`) para o arquivo `config.txt`.
    *   Criar o visualizador ASCII colorido rodando sobre a matriz fictícia (`grid_teste`).
    *   Criar a interface do menu interativo (`[R]`, `[P]`, `[C]`, `[Q]`).
*   **Guilherme**:
    *   Escrever a estrutura da classe `MazeGenerator`.
    *   Desenvolver a geração perfeita utilizando o DFS (Recursive Backtracking).
    *   Desenvolver o resolvedor de caminhos utilizando o BFS.

### 📌 Passo 3: Integração dos Sistemas (Dia 5)
*   **Juntos**: Conectar o script principal da **Thamily** ao pacote `mazegen` do **Guilherme**.
*   Substituir as matrizes fictícias de testes da Thamily pelo gerador dinâmico do Guilherme. Corrigir eventuais desalinhamentos de coordenadas (linha vs coluna).

### 📌 Passo 4: Polimento, Exportação e Entrega (Dias 6 e 7)
*   **Thamily**: Implementar a função de escrita e conversão para o arquivo hexadecimal final (`maze.txt`).
*   **Guilherme**: Finalizar a lógica do número "42" no centro e o comportamento para mapas imperfeitos. Configurar o arquivo `pyproject.toml` para empacotamento oficial.
*   **Juntos**: Escrever a documentação final no `README.md`, rodar o analisador estático para certificar que não há erros de tipos ou PEP8 e rodar testes para garantir nota máxima.
