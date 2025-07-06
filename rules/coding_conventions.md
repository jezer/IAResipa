# Convenções de Código (Python)

Para o código Python, a base será a **PEP 8**, que é o guia de estilo oficial para Python.

*   **Formatação:**
    *   **Indentação:** 4 espaços para cada nível de indentação.
    *   **Comprimento da Linha:** Máximo de 79 caracteres (para código) e 72 caracteres (para docstrings e comentários).
    *   **Quebras de Linha:** Use parênteses, colchetes ou chaves para quebrar linhas longas.
*   **Nomenclatura:**
    *   **Módulos e Pacotes:** `snake_case` (ex: `meu_modulo.py`, `meu_pacote/`).
    *   **Classes:** `PascalCase` (ex: `MinhaClasse`).
    *   **Funções e Variáveis:** `snake_case` (ex: `minha_funcao()`, `minha_variavel`).
    *   **Constantes:** `UPPER_CASE` (ex: `MINHA_CONSTANTE`).
*   **Docstrings:**
    *   Utilize docstrings para módulos, classes e funções, seguindo a **PEP 257**.
    *   Use aspas triplas (`"""Docstring aqui."""`).
    *   Descreva o propósito, parâmetros (`Args:`), e o que a função retorna (`Returns:`).
*   **Type Hinting:**
    *   Sempre que possível, utilize anotações de tipo (type hints) para parâmetros de funções e valores de retorno. Isso melhora a legibilidade e a capacidade de detecção de erros por ferramentas.
*   **Importações:**
    *   Agrupe as importações na seguinte ordem:
        1.  Módulos da biblioteca padrão.
        2.  Módulos de terceiros.
        3.  Módulos locais do projeto.
    *   Cada grupo deve ser separado por uma linha em branco.
    *   As importações dentro de cada grupo devem ser ordenadas alfabeticamente.
*   **Tratamento de Erros:**
    *   Utilize blocos `try-except` para lidar com exceções esperadas.
    *   Evite `except` genéricos sem especificar o tipo de exceção.
*   **Modularidade:**
    *   Mantenha funções e classes pequenas e com responsabilidades únicas.