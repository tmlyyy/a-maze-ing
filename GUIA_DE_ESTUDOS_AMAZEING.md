# Guia de estudos A-Maze-ing — Thamily e Guilherme

Este guia é pessoal para estudar o código final. Os arquivos da entrega são o programa e seus três módulos de interface, a configuração, o pacote `mazegen`, o wheel, `README.md`, `LICENSE.md`, `Makefile`, `pyproject.toml` e `.gitignore`. Este guia não substitui o README nem o subject.

## O que o subject v2.2 pede

**Obrigatório:** Python >= 3.10; estilo flake8, tipos e mypy com os parâmetros do Makefile; docstrings; script `a_maze_ing.py config.txt`; configuração `KEY=VALUE` com seis chaves obrigatórias; erros claros; labirinto aleatório e reproduzível por seed; paredes simétricas e bordas fechadas; corredores conectados; ausência de área 3x3 totalmente aberta; “42” de células fechadas quando houver espaço; modo perfeito sem ciclos; modo padrão com centro e cantos abertos, vários ciclos e poucas pontas; menor caminho; exportação hexadecimal no formato do PDF; visualização e três interações; pacote reutilizável instalável, documentação, licença, README e Makefile.

**Bônus:** modo padrão sem nenhuma ponta sem saída, múltiplos algoritmos, animação. O código usa um único algoritmo de geração e não promete o bônus de zero pontas. Quando não há espaço para o “42”, o programa avisa e continua, como o subject permite.

## O que aprender primeiro

1. Listas e índices, laços `for` e `while`, conjuntos (`set`) e dicionários (`dict`).
2. Arquivos com `with open`, exceções `ValueError`/`OSError` e argumentos `sys.argv`.
3. Bits (`&`, `|`, `~`), grafos, pilha do DFS e fila do BFS.
4. Classes, métodos, tipos, `pip wheel`, `venv` e leitura dos testes.

## Coordenadas, matriz, bits e hexadecimal

Uma posição é `(x, y)`: `x` cresce para leste e `y` para sul. A linha é escolhida antes da coluna: `grid[y][x]`. Por exemplo, `(2, 1)` é `grid[1][2]`.

Cada célula guarda um inteiro de 0 a 15. N=1, E=2, S=4, W=8. `15` (`1111` em binário, `F` em hexadecimal) fecha tudo. `9` (`1001`) fecha oeste e norte. `cell & E` testa se a parede leste existe. Para abrir leste, o código faz `grid[y][x] &= ~E` e **também** abre oeste no vizinho. Por isso as paredes ficam simétricas. Na saída, `f"{cell:X}"` transforma um inteiro em um único dígito hexadecimal.

Exemplo pequeno: numa grade 2x2 inicialmente `FF/FF`, abrir leste entre `(0,0)` e `(1,0)` transforma os dois valores em `D` e `7`: `D7/FF`. `F & ~2 = D`; `F & ~8 = 7`.

## DFS, BFS, conectividade e ciclos

`MazeGenerator._carve_tree()` usa uma **pilha**. Começa na entrada, escolhe um vizinho ainda não visitado, abre a parede e empilha o vizinho. Quando não há opção, desempilha e volta. Cada nova abertura liga uma célula nova à parte já visitada: todos os corredores acabam conectados e nenhuma abertura fecha um ciclo. As células “42” ficam de fora desse grafo.

Exemplo 2x2: se o DFS abrir `(0,0)->(1,0)->(1,1)->(0,1)`, temos quatro células e três passagens. Há um único trajeto entre quaisquer duas. Abrir depois a parede `(0,1)->(0,0)` criaria uma quarta passagem e um ciclo: agora há duas rotas entre alguns pontos. O modo padrão abre várias paredes extras e tenta corrigir pontas sem saída, sempre recusando uma abertura que forme uma área 3x3 inteira.

`shortest_path()` usa uma **fila** (`deque`). Visita primeiro os vizinhos a um passo, depois a dois passos etc. O dicionário `parents` registra de onde veio cada célula. Quando chega à saída, volta pelos pais e inverte a lista. Assim obtém o menor caminho em número de passos, inclusive quando há ciclos.

**Seed:** `random.Random(seed)` controla as escolhas do DFS e das paredes extras. Duas chamadas com a mesma configuração e a mesma seed geram a mesma matriz. No menu, “gerar novamente” remove a seed fixa daquela instância para criar uma nova grade aleatória; o arquivo de configuração permanece igual.

## “42” e os dois modos

`DIGITS` em `mazegen/generator.py` descreve um desenho de 8x5. `#` vira célula totalmente fechada (`F`); ponto continua corredor. O “4” usa quatro colunas para não criar um beco interno. O “2” ainda forma dois becos junto ao desenho. O analisador oficial classifica esses dois como cercados pelo “42”, separados dos becos reais. O gerador procura uma posição com margem de uma célula, sem cobrir entrada, saída ou locais obrigatórios, e verifica se os corredores restantes ainda formam uma região conectada. Em grade menor que 10x7, não há largura ou altura para o desenho com essa margem; o programa mostra aviso.

Com `PERFECT=True`, o DFS deixa uma árvore: nenhum ciclo, embora haja várias pontas. Com `PERFECT=False`, o mesmo DFS é a base; `_add_routes()` abre outras paredes, inclusive para reduzir pontas. Isso produz pelo menos dois ciclos independentes. Os quatro cantos e `grid[height // 2][width // 2]` permanecem corredores acessíveis. Em ambos, as bordas externas ficam fechadas, inclusive na entrada e na saída, porque elas são células **dentro** da grade.

## Papel de cada arquivo e fluxo

- `config.txt`: valores usados no exemplo padrão.
- `a_maze_ing.py`: `main()` trata erros; `run()` coordena geração, exportação, tela e menu.
- `config_parser.py`: `read_config()` lê o arquivo; `parse_point()` interpreta coordenadas; `make_generator()` converte os valores e cria o gerador.
- `maze_exporter.py`: `directions()` converte o caminho para N/E/S/W; `export_maze()` escreve o arquivo.
- `maze_renderer.py`: `render()` desenha a tela; contém paletas e constantes visuais.
- `mazegen/generator.py`: classe única de geração; valida dimensões, escolhe o padrão, gera a árvore e abre rotas extras.
- `mazegen/solver.py`: BFS do menor caminho.
- `mazegen/__init__.py`: API pública e exemplo reutilizável.
- `pyproject.toml`: metadados para construir `mazegen-*.whl`.
- `Makefile`: install, run, debug, clean, lint e lint-strict.
- `README.md`: documentação oficial da entrega, recursos, equipe e execução.
- `LICENSE.md`: licença MIT para reutilização e distribuição.
- `.gitignore`: exclusões de caches, ambientes e artefatos locais.

Fluxo: `main()` em `a_maze_ing.py` verifica o argumento e chama `run()` -> `read_config()` e `make_generator()` em `config_parser.py` leem e convertem a configuração -> `generate()` e `solve()` em `mazegen` geram e resolvem -> `export_maze()` em `maze_exporter.py` escreve hex, linha vazia, entrada, saída e direções -> `render()` em `maze_renderer.py` monta a tela -> o menu em `run()` responde às opções.

### Por que separar e como os imports funcionam

O arquivo principal importa funções de configuração, exportação e renderização. Cada módulo da interface importa `MazeGenerator` de `mazegen`, sem importar o principal nem outro módulo da interface. Dentro do pacote, `__init__.py` expõe a classe de `generator.py`, que importa `shortest_path()` de `solver.py`. Não existe caminho de volta da geração para a interface, nem import circular.

Separar por responsabilidade permite encontrar cada etapa sem percorrer o menu: configuração interpreta a entrada, exportação grava a saída, renderização monta o texto, e o principal coordena. Não criamos novas classes nem mudamos a API do pacote. O alias `Point = tuple[int, int]` apenas dá um nome ao tipo de coordenada; cada módulo que precisa dele o declara localmente.

O wheel inclui somente `mazegen`, conforme `packages = ["mazegen"]` em `pyproject.toml`. Para executar a interface em outra pasta, copie `a_maze_ing.py`, `config_parser.py`, `maze_exporter.py` e `maze_renderer.py` juntos e instale o wheel no Python escolhido.

## Como o renderizador desenha a tela

`render()` em `maze_renderer.py` apenas lê `grid[y][x]` e as coordenadas retornadas pelo BFS. Não altera a matriz nem a exportação. Cada célula ocupa quatro colunas por duas linhas de texto. A tela tem `2 * HEIGHT + 1` linhas e `4 * WIDTH + 1` colunas, mais a legenda. O centro de `(x, y)` fica na coluna `4*x+2`, linha `2*y+1`.

`walls` e `route` são duas matrizes auxiliares usadas apenas para desenhar. A primeira guarda os segmentos das paredes; a segunda, os segmentos do caminho. A função interna `connect()` liga duas posições horizontais ou verticais. Em cada posição, guarda os bits N=1, E=2, S=4 e W=8 das direções dos segmentos. Uma posição ligada ao norte e ao leste, por exemplo, guarda 3. A tabela `GLYPHS` traduz esses valores em paredes Unicode espessas, como `━`, `┃` e `┗`.

O caminho liga os centros de células consecutivas retornadas pelo BFS, incluindo as posições intermediárias nas passagens abertas. Antes de ligar, o código confere vizinhança, parede aberta e ausência de células do “42”. Nos segmentos de `route`, desenha bolinhas `●` apenas nas colunas pares: uma a cada duas colunas na horizontal ou uma linha na vertical. Esse espaçamento equilibra a distância visual dos pontos em uma fonte monoespaçada típica, nas retas e nas curvas. Quando `show_path` é falso, `route` fica vazia.

Cada célula reservada do “42” vira três bolinhas `●●●` na linha do centro, nas colunas `4*x+1`, `4*x+2` e `4*x+3`. Não desenhamos caixas de paredes entre essas células reservadas; as bolinhas preservam o desenho original de 8×5 células e seus espaços internos. Ao compor o texto, a função aplica as paredes ou o caminho, depois as bolinhas do “42” e por último os marcadores da entrada e da saída.

Tudo usa cor do texto (foreground); o fundo do terminal fica intacto. A opção `3` alterna **branco → vermelho → azul → rosa → branco**. O caminho e o “42” usam o mesmo tom mais claro da paleta. A entrada é sempre uma bolinha verde; a saída, uma bolinha vermelha. A legenda identifica os dois pontos. A opção `2` oculta/restaura somente o caminho, preservando paredes, “42” e marcadores. A opção `1` continua gerando outro mapa.

As cores RGB são explícitas para reduzir a variação entre temas de terminal. Fonte, tamanho e espaçamento ainda podem mudar a aparência. Sem ANSI (saída redirecionada, `TERM=dumb`, `TERM=unknown` ou `NO_COLOR`), usamos paredes `-`, `|`, `+`, pontos `.` para o caminho, `ooo` por célula do “42” e marcadores `E`/`X`, sem códigos de cor. Terminais sem codificação UTF também usam esses símbolos ASCII. A composição mantém posições fixas em todas as paletas.

## Executar e verificar

```sh
python3 a_maze_ing.py config.txt
make run
flake8 .
mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
python3 -m pip wheel . --no-deps --no-build-isolation -w .
python3 -m venv /tmp/venv-amazeing
/tmp/venv-amazeing/bin/pip install ./mazegen-1.0.0-py3-none-any.whl
```

Para experimentar, edite `config.txt` e use valores válidos; rode outra vez. `SEED=42` permite comparar saídas. Sem `SEED`, cada execução sorteia uma grade nova. Em `OUTPUT_FILE`, confira que há `HEIGHT` linhas hexadecimais, uma linha vazia e três linhas finais, todas com `\n`.

## Roteiro curto da avaliação

O subject define os requisitos, a régua organiza a conferência e o analisador oficial mede algumas propriedades do arquivo. O analisador não valida o caminho escrito, as bordas externas nem a regra da área 3x3; precisamos conferir esses pontos também.

### Gerar e analisar os dois modos

Na raiz do projeto, crie cópias temporárias do config. Assim os testes não alteram o arquivo padrão nem a saída de trabalho:

```sh
export AMAZEING_REVIEW_DIR=$(mktemp -d)
python3 - <<'PY'
import os
from pathlib import Path

directory = Path(os.environ["AMAZEING_REVIEW_DIR"])
source = Path("config.txt").read_text()
for name, mode in (("perfect", "True"), ("standard", "False")):
    lines = []
    for line in source.splitlines():
        if line.startswith("OUTPUT_FILE="):
            line = f"OUTPUT_FILE={directory / (name + '.txt')}"
        elif line.startswith("PERFECT="):
            line = f"PERFECT={mode}"
        lines.append(line)
    (directory / (name + '.cfg')).write_text("\n".join(lines) + "\n")
PY
python3 a_maze_ing.py "$AMAZEING_REVIEW_DIR/perfect.cfg"
python3 /home/tmly/Downloads/maze_analyzer.py "$AMAZEING_REVIEW_DIR/perfect.txt"
python3 a_maze_ing.py "$AMAZEING_REVIEW_DIR/standard.cfg"
python3 /home/tmly/Downloads/maze_analyzer.py "$AMAZEING_REVIEW_DIR/standard.txt"
```

Use `4` para sair depois de cada primeira geração. Leia a linha `Verdict:` inteira: no primeiro arquivo ela deve começar com `PERFECT maze`, no segundo com `Pac-Man-USABLE`. O código de saída 0 do analisador também aparece quando o veredito é desfavorável, portanto sozinho não prova aprovação.

`Independent loops` conta os ciclos independentes: em um grafo conectado, passagens menos corredores mais um. No perfeito, deve ser zero; no padrão, pelo menos dois. `Dead-ends` separa os becos **reais**, que possuem uma parede voltada para outro corredor, dos **enclosed by the '42'**, cercados por células fechadas ou pela borda. O limite padrão é no máximo dois becos reais.

Com 20x15 e seed 42, os relatórios conferidos mostraram zero ciclos no perfeito e 34 no padrão. O padrão teve zero becos reais e dois cercados pelo “42”, em `(12,6)` e `(12,8)`. O relatório usa a expressão `bonus-grade` para esse caso, mas este projeto não reivindica o bônus de zero becos. Nas verificações também foram usados 10x7, 10x8, 11x7 e 12x9; em 9x7, 10x6, 4x4 e 2x3 o desenho é omitido com aviso no console.

### Tela, menu e erros de configuração

Compare o primeiro mapa com as linhas hexadecimais: os bits devem reproduzir as mesmas paredes. Siga os passos N/E/S/W da entrada à saída; cada passo precisa atravessar uma parede aberta. A quantidade de passos precisa ser a menor distância, conferida por BFS.

Use `2` duas vezes para ocultar e restaurar o caminho; `3` quatro vezes para conferir branco → vermelho → azul → rosa → branco e as bolinhas do caminho e do “42” no mesmo tom mais claro, mantendo a entrada verde e a saída vermelha; `1` para gerar novamente. A regeneração recalcula o BFS e atualiza o arquivo. Iniciar outra execução com a seed original repete o primeiro mapa.

Em cópias temporárias, o avaliador pode remover qualquer chave obrigatória, escrever uma linha sem `=`, trocar números por letras, usar `PERFECT=Maybe` ou escrever `ENTRY=1;2` e `EXIT=1,2,3`. O programa informa `Erro: ...` e termina com código 1, sem traceback. Esse encerramento é controlado. Teste também coordenadas fora da grade ou entrada igual à saída.

### Reconstruir e instalar o pacote em ambientes diferentes

Na raiz, com o diretório temporário acima ainda definido:

```sh
flake8 .
mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
python3 -m venv "$AMAZEING_REVIEW_DIR/build-env"
"$AMAZEING_REVIEW_DIR/build-env/bin/python" -m pip install setuptools wheel
"$AMAZEING_REVIEW_DIR/build-env/bin/python" -m pip wheel . --no-deps --no-build-isolation -w "$AMAZEING_REVIEW_DIR/dist"
python3 -m venv "$AMAZEING_REVIEW_DIR/install-env"
"$AMAZEING_REVIEW_DIR/install-env/bin/python" -m pip install "$AMAZEING_REVIEW_DIR/dist/mazegen-1.0.0-py3-none-any.whl"
mkdir -p "$AMAZEING_REVIEW_DIR/interface"
cp a_maze_ing.py config_parser.py maze_exporter.py maze_renderer.py "$AMAZEING_REVIEW_DIR/interface/"
"$AMAZEING_REVIEW_DIR/install-env/bin/python" -I -c 'from mazegen import MazeGenerator; m = MazeGenerator(20, 15, (0, 0), (19, 14), seed=42); m.generate(); print(m.solve())'
"$AMAZEING_REVIEW_DIR/install-env/bin/python" "$AMAZEING_REVIEW_DIR/interface/a_maze_ing.py" "$AMAZEING_REVIEW_DIR/standard.cfg"
```

A opção `-I` no teste da API evita importar o pacote da pasta do repositório. No teste da interface, a pasta temporária contém os quatro módulos, mas não contém uma pasta `mazegen`; por isso ela importa o pacote instalado. Não usamos `-I` nessa execução, pois ele também impediria os imports dos módulos vizinhos da interface. Confira `mazegen.__file__` no ambiente instalado: deve apontar para `site-packages`. Depois de qualquer alteração em `mazegen` ou nos metadados, reconstrua o wheel entregue na raiz.

Para explicar oralmente: o DFS usa uma pilha para ligar células novas e formar a árvore; o BFS usa uma fila para encontrar a saída pelo menor número de passos; os quatro bits guardam as paredes em um único número. O “42” é reservado antes de cavar os corredores. Abrir uma parede entre corredores já conectados cria um ciclo; um corredor com uma única passagem é um beco. As aberturas extras reduzem becos, criam alternativas e são recusadas se formarem uma área 3x3 totalmente aberta.

## Perguntas prováveis na avaliação

**Por que `grid[y][x]`?** A matriz é uma lista de linhas, por isso `y` seleciona a linha e `x` a coluna. A API sempre recebe pontos `(x, y)`.

**Por que uma parede precisa ser alterada duas vezes?** É compartilhada por duas células; leste de uma é oeste da outra. `_open()` altera os dois bits.

**Por que o perfeito não tem ciclos?** O DFS só abre para uma célula ainda não visitada; cada abertura adiciona uma célula e uma aresta à árvore.

**Como o padrão mantém conectividade?** `_connected_shape()` verifica a área antes de escolher a posição; o DFS visita todos os corredores restantes.

**Por que BFS dá o menor caminho?** A fila visita células por distância crescente; a primeira visita à saída usa o menor número de passos.

**O que muda em `PERFECT=False`?** `_add_routes()` abre paredes internas extras, reduz pontas e exige ao menos dois ciclos; protege centro, cantos e a regra da área 3x3.

**O que uma seed garante?** A mesma configuração com o mesmo número gera as mesmas escolhas aleatórias e a mesma matriz.

**Como é o arquivo de saída?** Um dígito hexadecimal por célula, uma linha por `y`, linha vazia, `x,y` da entrada, `x,y` da saída, e sequência N/E/S/W do caminho BFS.

**Qual arquivo é importado por outro projeto?** O wheel instala `mazegen`; `from mazegen import MazeGenerator` dá acesso a `generate()`, `get_structure()` e `solve()` sem depender do programa de terminal.

**O que acontece com entrada inválida?** O parser em `config_parser.py` e a classe em `mazegen/generator.py` lançam `ValueError`; `main()` captura e imprime `Erro: ...` sem traceback esperado.
