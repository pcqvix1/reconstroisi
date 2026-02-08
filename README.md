# Projeto: Código que Evolui Sozinho

## Definição formal
Um sistema computacional capaz de observar métricas internas, avaliar alternativas estruturais e reescrever partes do próprio código, mantendo histórico, segurança e critérios objetivos de melhoria.  
Isso **não** é IA generativa escrevendo código livremente.  
É **engenharia evolutiva controlada**.

---

## 1. Princípios fundamentais
### 1.1 Evolução ≠ aleatoriedade
O sistema:
- não improvisa;
- não cria código arbitrário;
- não “imagina” soluções.  
Ele seleciona, combina ou transforma **código pré-validado**.

### 1.2 Código é dado
O código-fonte:
- é lido;
- analisado;
- versionado;
- comparado;
- modificado.  
Isso exige uma **representação intermediária** (AST, IR, templates).

### 1.3 Métrica manda mais que opinião
Toda mudança precisa melhorar uma função de fitness explícita.  
Sem métrica → **sem evolução**.

---

## 2. Arquitetura completa (visão macro)
```
┌───────────────────┐
│   Runtime System  │
└─────────┬─────────┘
          ↓
┌───────────────────┐
│ Metrics Collector │
└─────────┬─────────┘
          ↓
┌───────────────────┐
│ Evolution Engine  │
└─────────┬─────────┘
          ↓
┌───────────────────┐
│ Code Rewriter     │
└─────────┬─────────┘
          ↓
┌───────────────────┐
│ Validator/Sandbox │
└─────────┬─────────┘
          ↓
┌───────────────────┐
│ Deployment / Swap │
└───────────────────┘
```

Todos os blocos acima são **obrigatórios**.

---

## 3. Camada 1 — Coleta de métricas (observação)
### O que medir (mínimo sério)
**Desempenho**
- tempo médio;
- p95 / p99;
- throughput.

**Memória**
- pico;
- média;
- alocações por função.

**Estrutura**
- funções mais chamadas;
- profundidade de chamadas;
- hotspots.

### Instrumentação (exemplo conceitual)
```python
@observe
def process_data(x):
    ...
```

Exemplo de saída estruturada:
```json
{
  "function": "process_data",
  "avg_time": 0.032,
  "memory_peak": 4.1,
  "calls": 18234
}
```

> Importante: **nada de logs soltos**. Apenas dados estruturados.

---

## 4. Camada 2 — Engine de evolução (o cérebro)
### 4.1 Função de fitness
Exemplo realista:
```
fitness =
    w1 * (baseline_time / current_time)
  + w2 * (baseline_memory / current_memory)
  + w3 * stability_score
```

- **baseline** = versão estável anterior;
- **stability_score** penaliza crashes e variância.

Sem melhoria mínima → mudança descartada.

### 4.2 Espaço de busca (crítico)
O sistema atua em **zonas evolutivas**, por exemplo:
- implementação de algoritmo;
- estrutura de dados;
- cache;
- paralelização;
- ordenação de operações.

Cada zona tem **regras explícitas**.

### 4.3 Estratégias evolutivas
**Seleção**
- várias implementações possíveis;
- escolhe a melhor.

**Mutação controlada**
- uma mudança por geração;
- rollback automático.

**Herança**
- nova versão herda código da anterior;
- apenas uma parte muda.

---

## 5. Camada 3 — Representação do código
### Por que AST (em Python)?
- evita `exec`;
- garante sintaxe válida;
- permite transformações estruturais.

Exemplo de forma:
```
FunctionDef
 ├── arguments
 ├── body
 │    ├── Assign
 │    ├── For
 │    └── Return
```

### Transformações permitidas (exemplos)
- substituir corpo da função;
- inserir cache;
- trocar loop por list comprehension;
- mudar algoritmo inteiro.

Cada transformação deve ser:
- isolada;
- reversível;
- testável.

---

## 6. Camada 4 — Validação e sandbox
Antes de produção:
✅ Checks obrigatórios
- sintaxe;
- tipagem (se houver);
- testes mínimos;
- limites de memória;
- tempo máximo.

🧪 Execução em sandbox
- ambiente isolado;
- input controlado;
- métricas coletadas novamente.

❌ Falhou?  
Rollback imediato.

---

## 7. Camada 5 — Deployment evolutivo
Estratégias seguras:
- **Hot swap (Python):** reload de módulo, troca de função;
- **Versionamento:** `core_v1.py`, `core_v2.py`, histórico preservado;
- **Kill switch:** se algo degrada → volta automaticamente.

---

## 8. Rust: mesmo conceito, outra filosofia
Rust não se auto-modifica em runtime. Pipeline evolutivo:
```
Executável atual
↓
Coleta métricas
↓
Gera novo código (.rs)
↓
cargo build
↓
Validação
↓
Substitui binário
↓
Reinicia
```

Isso é:
- mais lento;
- extremamente robusto;
- ideal para sistemas críticos.

---

## 9. Problemas difíceis (e como lidar)
- **Auto-sabotagem:** limites rígidos + rollback.
- **Overfitting:** ambientes de teste variados.
- **Explosão de versões:** poda genética (manter top N).
- **Segurança:** transformações whitelist only.

---

## 10. Por que isso é raro?
Porque exige:
- conhecimento de compiladores;
- engenharia de sistemas;
- ciência evolutiva;
- disciplina absurda.

É **pesquisa aplicada**, não produto comum.

---

## 11. Caminho recomendado (MVP)
1. Python + AST.
2. Função simples (ex.: processamento de dados).
3. 2–3 implementações manuais.
4. Seleção automática.
5. Reescrita real.
6. Histórico + rollback.
7. Só depois mutações.

---

## 12. MVP neste repositório
Este repositório inclui um MVP funcional em Python com:
- coleta de métricas com `MetricsCollector`;
- engine de evolução que calcula fitness;
- rewriter baseado em AST com whitelist;
- validador de corretude;
- histórico versionado em JSONL;
- hot swap via registry.

### Estrutura
```
evolver/
  metrics.py
  evolution.py
  rewriter.py
  validator.py
  deployment.py
  runtime.py
  storage.py
  pipeline.py
main.py
```

### Como executar
```bash
python main.py
```
