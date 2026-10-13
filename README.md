*This project has been created as part of the 42 curriculum by thamoliv, gproenca.*

# A-Maze-ing

Gerador de labirintos em Python, com solução por menor caminho, visualização
no terminal e exportação hexadecimal. Projeto desenvolvido em dupla na 42SP.

## Descrição

O programa lê uma configuração, gera um mapa, calcula o menor caminho entre
entrada e saída e salva o resultado. Em seguida, mostra o labirinto e um menu
para gerar outro mapa, mostrar ou ocultar a solução e trocar as cores.

A geração e a solução ficam no pacote independente `mazegen`. A configuração,
a tela e a escrita do arquivo ficam nos módulos da aplicação.

### Dois modos de geração

| Configuração | Comportamento |
| --- | --- |
| `PERFECT=True` | O DFS forma uma árvore: corredores conectados, sem ciclos e com uma única rota entre quaisquer dois corredores. |
| `PERFECT=False` | Parte da mesma árvore e abre rotas extras para criar pelo menos dois ciclos independentes e reduzir becos sem saída. É o modo padrão do construtor, usado também no config fornecido. |

Nos dois modos, as paredes compartilhadas são coerentes, as bordas externas
ficam fechadas e não são abertas áreas 3×3 inteiras. Entrada e saída são células
internas à grade, não buracos na borda. No modo padrão, centro e quatro cantos
são corredores acessíveis. Se as dimensões não permitem dois ciclos, o gerador
informa um erro. Não reivindicamos bônus de zero becos, animação ou múltiplos
algoritmos de geração.

### O padrão “42”

O desenho ocupa uma região de 8×5 células. Suas células reservadas têm todas
as paredes fechadas (`F`), ficando fora dos corredores visitados pelo DFS.
O gerador procura uma posição com margem, sem cobrir entrada, saída ou locais
protegidos, e confere a conectividade dos corredores restantes.

Quando não encontra uma posição válida, o programa avisa no console e gera
sem o desenho. Com a margem usada nesta implementação, tamanhos menores que
10×7 não comportam o padrão. Na tela, cada célula reservada aparece como três
bolinhas claras; isso não muda a matriz nem a exportação.

## Instruções

### Requisitos e execução

- Python **3.10 ou posterior** e `pip` para instalar/construir o pacote.
- `make install` instala `flake8` e `mypy` para as verificações de código.
- Terminal com ANSI e UTF para o visual colorido; há alternativa ASCII.
- A execução usa apenas a biblioteca padrão e o pacote local `mazegen`.

Na raiz do repositório:

```sh
make install
make lint
python3 a_maze_ing.py config.txt
```

`make install` instala o pacote `mazegen`, `flake8` e `mypy`. Ele usa o
interpretador Python real para evitar a tentativa de atualizar shims do
`pyenv` sem permissão. O Makefile também inclui o diretório de executáveis
do usuário no `PATH`, onde o `pip` pode instalar `mypy`. Os módulos da
interface continuam na pasta do projeto, de onde o comando principal deve
ser executado. Se usar um ambiente virtual, crie-o fora da raiz do projeto,
pois `flake8 .` percorre diretórios dentro dela.

| Comando real do Makefile | O que faz |
| --- | --- |
| `make install` | Instala o pacote e as ferramentas `flake8` e `mypy` com o Python ativo. |
| `make run` | Executa o programa com `config.txt`. |
| `make debug` | Abre o programa com o depurador `pdb`. |
| `make clean` | Remove diretórios `__pycache__`, `.mypy_cache` e `.pytest_cache`. |
| `make lint` | Executa flake8 e mypy com os parâmetros exigidos. |
| `make lint-strict` | Executa flake8 e `mypy . --strict`; é uma conferência adicional. |

O comando completo de tipos usado por `make lint` é:

```sh
mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
```

### Configuração completa

Cada linha contém `KEY=VALUE`. Linhas vazias e comentários iniciados por `#`
são ignorados. As chaves são maiúsculas; espaços ao redor de chave e valor
são removidos. Chaves desconhecidas, repetidas ou com valor vazio são erros.

| Chave | Obrigatória | Formato e validação | Exemplo |
| --- | --- | --- | --- |
| `WIDTH` | Sim | Inteiro ≥ 2; o modo padrão também precisa comportar dois ciclos. | `20` |
| `HEIGHT` | Sim | Inteiro ≥ 2; sujeito à mesma validação do modo. | `15` |
| `ENTRY` | Sim | Dois inteiros `x,y`, dentro da grade. | `0,0` |
| `EXIT` | Sim | Dois inteiros `x,y`, dentro da grade e distintos da entrada. | `19,14` |
| `OUTPUT_FILE` | Sim | Caminho não vazio; a escrita precisa ser permitida. | `maze.txt` |
| `PERFECT` | Sim | Exatamente `True` ou `False`. | `False` |
| `SEED` | Não | Inteiro; sem a chave, a geração é aleatória. | `42` |

Exemplo do mapa padrão:

```ini
# Coordenadas no formato x,y
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=42
```

Arquivo ausente, linha sem `=`, valores inválidos, coordenadas impossíveis e
falhas de escrita geram mensagens claras em inglês. O programa termina com código 1
nesses erros, sem traceback esperado.

### Coordenadas e seed

As posições sempre usam `(x, y)`: `x` é a coluna e `y` é a linha, começando
em zero. Na matriz, acessamos **`grid[y][x]`**. Assim, `(2, 1)` corresponde a
`grid[1][2]`.

A mesma configuração e a mesma seed repetem a matriz e o caminho nesta
implementação. A opção `1` remove a seed fixa da instância e faz uma nova
geração aleatória; ela não altera o config. Iniciar outra execução com o
config original repete o primeiro mapa.

### Menu e aparência

| Opção | Ação |
| --- | --- |
| `1` | Gera outro mapa, recalcula o BFS e atualiza o arquivo exportado. |
| `2` | Oculta ou restaura somente as bolinhas do menor caminho. |
| `3` | Alterna branco → vermelho → azul → rosa → branco. |
| `4` | Sai do programa. EOF e Ctrl+C no menu também encerram de forma controlada. |

As paredes usam linhas Unicode espessas (`━`, `┃` e junções), com cor do texto,
sem pintar o fundo. O caminho usa bolinhas claras a cada duas colunas ou uma
linha de texto. O “42” usa **três bolinhas por célula reservada**, na mesma
cor clara do caminho. Entrada e saída permanecem, respectivamente, verde e
vermelha, identificadas por uma legenda.

Saída redirecionada, `TERM=dumb`, `TERM=unknown` ou `NO_COLOR` usam ASCII sem
códigos ANSI: paredes `-`, `|`, `+`, caminho `.`, padrão `ooo` por célula e
marcadores `E`/`X`. Sem codificação UTF, os símbolos também usam ASCII.
As cores RGB são explícitas, mas fonte, tamanho e espaçamento do terminal
podem mudar a aparência.

## Algoritmos e representação

### DFS iterativo para gerar

O DFS usa uma lista como pilha. Escolhe um vizinho ainda não visitado, abre a
parede nos dois lados e avança. Quando não há vizinho novo, volta pela pilha.
Cada abertura liga uma célula nova à região visitada: isso produz uma árvore
conectada, sem ciclos. Escolhemos essa abordagem por ser possível acompanhá-la
passo a passo e por evitar recursão profunda em Python.

No modo padrão, `_add_routes()` abre paredes extras entre corredores já
conectados. Primeiro tenta reduzir becos e depois completar as rotas extras.
Cada tentativa que criaria uma área 3×3 inteiramente aberta é desfeita.

### BFS para resolver

O BFS usa uma fila `deque`: visita primeiro as células a um passo, depois a
dois passos, e assim por diante. Registra os pais para reconstruir a solução.
Como cada passagem tem o mesmo custo, encontra o menor caminho em número de
passos, inclusive quando existem ciclos. A lista inclui entrada e saída.

### Máscaras de bits e exportação

| Parede | Máscara | Bit |
| --- | --- | --- |
| Norte | `1` | `0001` |
| Leste | `2` | `0010` |
| Sul | `4` | `0100` |
| Oeste | `8` | `1000` |

Bit 1 significa parede fechada. `cell & 2` testa a parede leste; abrir uma
passagem remove esse bit e o bit oeste do vizinho. `F` equivale a 15, com
quatro paredes fechadas; `A` equivale a 10, com leste e oeste fechados.

O arquivo contém:

1. `HEIGHT` linhas, cada uma com `WIDTH` dígitos hexadecimais, sem espaços;
2. uma linha vazia;
3. entrada `x,y`;
4. saída `x,y`;
5. menor caminho em letras `N/E/S/W`.

Todas as linhas terminam em `\n`. Por exemplo, `EES` significa dois passos
para leste e um para sul. A visualização não altera esse formato.

## Estrutura e responsabilidades

```text
a-maze-ing/
├── a_maze_ing.py
├── config_parser.py
├── maze_renderer.py
├── maze_exporter.py
├── mazegen/
│   ├── __init__.py
│   ├── generator.py
│   └── solver.py
├── config.txt
├── Makefile
├── pyproject.toml
├── .gitignore
├── README.md
├── LICENSE.md
└── mazegen-1.0.0-py3-none-any.whl
```

| Arquivo | Responsabilidade |
| --- | --- |
| `a_maze_ing.py` | `main()`, `run()`, menu e coordenação das etapas. |
| `config_parser.py` | `parse_point()`, `read_config()` e `make_generator()`. |
| `maze_renderer.py` | `render()`, paletas, símbolos e constantes da apresentação. |
| `maze_exporter.py` | `directions()` e `export_maze()` no formato do subject. |
| `mazegen/generator.py` | Classe `MazeGenerator`, validação, padrão e geração. |
| `mazegen/solver.py` | BFS em `shortest_path()`. |
| `mazegen/__init__.py` | API pública e exemplo curto de uso independente. |
| `pyproject.toml` | Metadados e seleção exclusiva de `mazegen` para o wheel. |
| `config.txt`, `Makefile` | Exemplo de configuração e comandos de trabalho. |
| `.gitignore` | Exclusão de caches, ambientes e artefatos locais. |
| `LICENSE.md` | Licença MIT para reutilização e distribuição. |

O fluxo é configuração → geração → BFS → exportação → tela → menu.
Os módulos da interface importam `mazegen`, mas o pacote não importa a
interface. Isso permite usar o gerador em outro programa sem ler config,
escrever arquivos ou abrir um menu.

## Reutilização e wheel

### Exemplo executável

```python
from mazegen import MazeGenerator

maze = MazeGenerator(20, 15, (0, 0), (19, 14), seed=42,
                     perfect=False)
maze.generate()
grid = maze.get_structure()
path = maze.solve()
print("Primeira célula:", grid[0][0])
print("Menor caminho:", path)
```

Passe tamanho, entrada, saída, seed e modo no construtor. `generate()` também
retorna a matriz de inteiros; `get_structure()` acessa a estrutura gerada, e
`solve()` retorna coordenadas `(x, y)`. Chame `generate()` antes de acessar a
estrutura ou resolver.

### Reconstruir e testar em dois ambientes

Execute os comandos abaixo na raiz do projeto. O primeiro ambiente reconstrói
o wheel; o segundo instala esse arquivo e executa a aplicação. Eles ficam fora
do repositório e não precisam ser ativados:

```sh
python3 -m venv ../amz-build-env ../amz-test-env
../amz-build-env/bin/python -m pip wheel . --no-deps -w .
../amz-test-env/bin/python -m pip install --no-deps --force-reinstall ./mazegen-1.0.0-py3-none-any.whl
mkdir -p ../amz-test-app
cp a_maze_ing.py config_parser.py maze_exporter.py maze_renderer.py config.txt ../amz-test-app/
cd ../amz-test-app
../amz-test-env/bin/python -c 'import mazegen; print(mazegen.__file__)'
../amz-test-env/bin/python a_maze_ing.py config.txt
```

O caminho impresso deve conter `amz-test-env`, confirmando que `mazegen` veio
do wheel instalado. No menu, digite `4` para sair. A pasta `amz-test-app` tem
apenas os arquivos da interface e a configuração; assim, não há uma cópia local
de `mazegen` que possa esconder o pacote instalado. O wheel contém o gerador e
seus metadados, incluindo o README. Reconstrua-o após alterar o pacote ou seus
metadados.

## Equipe e organização do trabalho

| Integrante | Divisão inicial de tarefas |
| --- | --- |
| **thamoliv — Thamily** | Configuração, interface e exportação. |
| **gproenca — Guilherme** | Geração, solução e empacotamento. |

O planejamento inicial previa partes paralelas e integração posterior.
Durante a integração, foi necessário unificar coordenadas `(x, y)`, a
representação das paredes e a API do gerador. A interface passou por ajustes
visuais; depois, suas responsabilidades foram separadas em módulos para
facilitar leitura e estudo. Essa divisão inicial não identifica a autoria
individual de cada trecho final.

Funcionou bem manter a geração e a solução no pacote independente e validar
os dois modos com o analisador fornecido. Poderíamos ter definido as
coordenadas, os bits das paredes e a API comum antes das partes paralelas;
isso teria reduzido o retrabalho durante a integração.

Ferramentas utilizadas: Python, Git, VS Code, `flake8`, `mypy`,
`pip`, ambientes virtuais e o analisador oficial.

## Resources — Referências


| Referência consultada | Uso |
| --- | --- |
| [Princeton — grafos não direcionados](https://algs4.cs.princeton.edu/41graph/index.php) | DFS, BFS, conectividade e caminhos em grafos. |
| [Python — `collections.deque`](https://docs.python.org/3/library/collections.html#collections.deque) | Fila usada pelo BFS. |
| [Python — `random`](https://docs.python.org/3/library/random.html) | Aleatoriedade e reprodução com seed. |
| [Microsoft — sequências de terminal](https://learn.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences) | Sequências ANSI e cores do texto. |
| [Unicode — Box Drawing](https://www.unicode.org/charts/PDF/U2500.pdf) | Caracteres das paredes e junções. |
| [Python Packaging User Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/) | Construção e instalação do pacote. |
| [PEP 257](https://peps.python.org/pep-0257/) | Referência de docstrings. |

### Uso de IA

- **ChatGPT/Codex:** auxílio técnico no desenvolvimento e integração do
  parser, gerador, BFS, exportação e interface; refatoração, revisão,
  verificações, documentação e explicações para estudo.
- **NotebookLM:** organização dos materiais e produção de conteúdo de estudo.
- **Gemini:** auxílio com dúvidas e explicações de conceitos.
