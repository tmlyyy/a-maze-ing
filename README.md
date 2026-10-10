*This project has been created as part of the 42 curriculum by thamoliv, gproenca.*


## Description

A-Maze-ing gera labirintos aleatórios reproduzíveis, resolve o menor caminho e exporta cada célula como um dígito hexadecimal. O modo perfeito forma uma árvore; o modo padrão abre vários ciclos para um tabuleiro tipo Pac-Man. A tela ASCII mostra as paredes, entrada, saída, caminho e um “42” de células fechadas quando há espaço.

## Instructions

Requer Python 3.10 ou posterior. Na raiz:

```sh
python3 a_maze_ing.py config.txt
make run
make lint
python3 -m pip wheel . --no-deps -w .
python3 -m venv /tmp/venv-amazeing
/tmp/venv-amazeing/bin/pip install ./mazegen-1.0.0-py3-none-any.whl
```

O menu aceita `1` para gerar de novo (uma nova geração aleatória), `2` para mostrar/ocultar o menor caminho, `3` para alternar a cor das paredes em terminais ANSI e `4` para sair. A exportação é atualizada após cada geração.

### Configuração

O arquivo contém uma linha `KEY=VALUE` por opção. Linhas vazias e linhas iniciadas por `#` são ignoradas. Todas as chaves abaixo, exceto `SEED`, são obrigatórias; chaves repetidas ou desconhecidas são erros.

| Chave | Formato | Exemplo |
| --- | --- | --- |
| `WIDTH` | inteiro >= 2 | `WIDTH=20` |
| `HEIGHT` | inteiro >= 2 | `HEIGHT=15` |
| `ENTRY` | coordenada `x,y` dentro da grade | `ENTRY=0,0` |
| `EXIT` | coordenada `x,y` distinta | `EXIT=19,14` |
| `OUTPUT_FILE` | caminho do arquivo de saída | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | `True` ou `False` | `PERFECT=False` |
| `SEED` | inteiro opcional | `SEED=42` |

A saída contém uma linha de dígitos hexadecimais por linha da grade, uma linha vazia, entrada, saída e os movimentos `N/E/S/W` do menor caminho. Todas as linhas terminam em `\n`.

### Algoritmos e reutilização

O DFS iterativo, em `mazegen.MazeGenerator`, visita cada corredor uma vez e abre uma parede até formar uma árvore. Escolhemos essa técnica por sua relação simples entre células visitadas e ausência de ciclos, e por evitar recursão profunda. O modo padrão parte da árvore e abre paredes para reduzir pontas sem saída e criar vários ciclos. O BFS encontra o menor caminho por camadas. `grid[y][x]` contém os bits N=1, E=2, S=4, W=8; uma parede presente vale 1.

O pacote `mazegen` é reutilizável, sem entrada de terminal nem escrita de arquivos:

```python
from mazegen import MazeGenerator
maze = MazeGenerator(20, 15, (0, 0), (19, 14), seed=42,
                     perfect=False)
grid = maze.generate()
path = maze.solve()
print(grid[0][0], path)
```

Altere largura, altura, entrada, saída, seed e modo no construtor. `maze.get_structure()` também dá acesso à matriz. A documentação curta está no módulo instalável (`mazegen/__init__.py`).

## Equipe e gestão

Thamily ficou inicialmente com configuração, interface e exportação; Guilherme, com geração, solução e empacotamento. O plano previa partes paralelas e integração posterior. Na integração, o protótipo ainda tinha saída fictícia e o gerador tinha erros de sintaxe; a implementação final foi reescrita em torno de coordenadas `(x, y)` e uma API única. O contrato de bits ajudou; o contrato antigo de caminho `(linha, coluna)` precisou ser corrigido. Para melhorar, a dupla deve revisar o código final junta e repetir a bateria de testes antes da defesa. Ferramentas usadas nesta etapa: Python, Git, `pdftotext`, `flake8`, `mypy`, `pip` e ambiente virtual. A autoria exata de cada trecho final deve ser revista pela dupla.

## Resources

- Subject A-Maze-ing v2.2, fornecido para o projeto: fonte dos requisitos.
- Régua de avaliação fornecida: roteiro de conferência da entrega.
- `maze_analyzer.py` oficial fornecido: verificação dos vereditos dos dois modos, ciclos, conectividade e classificação dos becos sem saída.
- [Python `random`](https://docs.python.org/3/library/random.html): referência para gerador com seed.
- [Python `collections.deque`](https://docs.python.org/3/library/collections.html#collections.deque): referência para a fila do BFS.
- [Python Packaging User Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/): referência de empacotamento.
- [PEP 257](https://peps.python.org/pep-0257/): referência de docstrings.

Um assistente de IA foi usado para ler o subject e inspecionar o repositório, reescrever e integrar o gerador, parser, visualização, exportação, documentação e empacotamento, além de sugerir verificações. A dupla deve estudar, revisar e assumir responsabilidade pelo código antes da avaliação.

O arquivo `GUIA_DE_ESTUDOS_AMAZEING.md` é um material pessoal de estudo, separado dos arquivos de entrega do programa e do pacote.
