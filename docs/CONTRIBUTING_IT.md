# Linee Guida per la Contribuzione a HumOS & LINGHOS
**Identificatore Documento:** `GOV-CONTRIB-20261108-IT`  
**Stato dello Standard:** `Specifica Ufficiale di Governance del Progetto`  
**Classificazione:** `Workflow per Sviluppatori Open-Source & Standard di Protocollo`  
**Maintainer:** `SystemAdmin01`  

---

## 1. Codice di Condotta Tecnica & Filosofia Architetturale

Il progetto HumOS impone standard ingegneristici deterministici rigorosi. A differenza dei framework tradizionali per agenti conversazionali, HumOS e il suo Domain-Specific Language (LINGHOS) operano come una rappresentazione intermedia deterministica (IR) tra la volatilità cognitiva biologica e i kernel di esecuzione a valle basati su Large Language Model (LLM).

Ogni contributo — che si tratti di una patch al parser, di un potenziamento al cockpit visuale o di una revisione documentale — deve preservare tassativamente:
1. **Tolleranza Zero alle Allucinazioni:** Il compilatore e il runtime non devono mai generare parametri di stato speculativi o non deterministici.
2. **Budget Rigoroso del Contesto:** L'overhead di token deve essere ridotto al minimo su tutti i confini di serializzazione.
3. **Garanzie Formali degli Invarianti:** L'isolamento del Core Self (`CS_SECURE`), la matematica della prossimità spaziale e il bilancio termodinamico (`RAM`, `BPM`) non possono essere aggirati né indeboliti.

---

## 2. Protocollo di Proposta Primitivi (PPP)

Qualsiasi estensione alla libreria standard di LINGHOS, alla grammatica del linguaggio o ai primitivi di esecuzione deve rispettare il **Protocollo di Proposta Primitivi**. La proliferazione incontrollata di parole chiave appesantisce l'AST, consuma budget di token e introduce ambiguità nel ragionamento a valle.

### 2.1 Criteri di Accettazione dei Primitivi
Prima di inviare una proposta per un nuovo primitivo (es. `MEMORY.*`, `THREAD.*`, `SHIELD.*`), l'autore deve dimostrare che:
1. **Non Ridondanza:** La funzionalità non può essere ottenuta componendo una sequenza di primitivi già esistenti (es. `RAM.alloc()` + `THREAD.spawn()`).
2. **Efficienza nel Context Window:** L'impronta di token serializzata del primitivo non deve superare **24 token** con codifica standard Byte-Pair Encoding (BPE) UTF-8.
3. **Transizione di Stato Deterministica:** Il primitivo deve produrre una modifica di stato matematicamente dimostrabile nel modello di memoria runtime (es. deallocare RAM, limitare i BPM o modificare il raggio di minaccia).
4. **Compatibilità Retroattiva del Parser:** L'aggiunta non deve introdurre conflitti di lookahead (ambiguità shift-reduce o reduce-reduce $LR(1)$) in `linghos/parser.py`.

### 2.2 Schema Formale RFC per Proposta Primitivi
Ogni proposta deve essere presentata tramite issue o pull request con riferimento a `docs/SPEC.md` utilizzando il seguente schema tecnico:

```markdown
### Specifica Primitivo: [DOMINIO].[identificatore]
- **Specifica Sintattica:** `Call >> [DOMINIO].[identificatore](<argomenti>);`
- **Arità & Tipi:** Tipi di parametro espliciti (es. `(target_id: Identificatore, limite: Intero)`).
- **Semantica di Memoria a Runtime:** Modifica concreta dello stato in `HumOSKernel` (es. impatto su RAM, registrazione thread).
- **Impatto sugli Invarianti Spaziali / Termodinamici:** Effetto diretto sul raggio di prossimità ($r$) o sul battito cardiaco ($BPM$).
- **Comportamento di Fallback & Eccezioni:** Codice di errore emesso in caso di anomalia (es. `ERR_BUFFER_OVERFLOW`).
- **Benchmark Token:** Conteggio token BPE per l'invocazione sintattica.
```

---

## 3. Standard di Verifica delle Pull Request (PRVS)

Ogni Pull Request (PR) deve superare una checklist di verifica manuale e automatica prima della revisione e del merge.

```mermaid
flowchart TD
    PR[Pull Request Inviata] --> CHECK_SYNTAX[1. Audit Rigoroso di Grammatica & Parser AST]
    CHECK_SYNTAX --> CHECK_LEAK[2. Prova di Isolamento del Contesto & Anti-Fuga]
    CHECK_LEAK --> CHECK_TOKEN[3. Benchmark dell'Overhead & Budget Token]
    CHECK_TOKEN --> CHECK_INVARIANT[4. Test Unitari degli Invarianti Termodinamici]
    CHECK_INVARIANT --> PASS[Tutti gli Invarianti Verificati -> Approvata per Merge]
    
    CHECK_SYNTAX -- Fallimento --> REJECT[PR Respinta: Violazione Invariante Sintattico]
    CHECK_LEAK -- Fallimento --> REJECT[PR Respinta: Perdita di Memoria / Fuga Contesto]
    CHECK_TOKEN -- Fallimento --> REJECT[PR Respinta: Superamento Budget Token]
    CHECK_INVARIANT -- Fallimento --> REJECT[PR Respinta: Discrepanza Termodinamica]
```

### 3.1 Checklist di Verifica Passo-Passo

- [ ] **1. Conformità Rigorosa a Grammatica & Lexer**
  - Tutti gli esempi `.lghos` e `.lgh` compilano correttamente tramite `linghos/compiler.py` senza alcun avviso sintattico.
  - I punti e virgola, le chiusure dei blocchi (`Main() { ... }`), le direttive (`/SET_Lockdown_Mode`) e gli header macro (`#include`) seguono rigorosamente la grammatica definita in `docs/SPEC.md`.
  - Nessuno spazio bianco superfluo a fine riga o delimitatori spezzati.

- [ ] **2. Verifica Isolamento Contesto (Zero Fuga di Prompt)**
  - Le variabili dichiarate nelle sandbox locali (`PRS_VM`, `LP_Ambient_VM`) non devono riversarsi nei buffer di memoria primaria o nei thread adiacenti.
  - I payload iniettati nel system prompt dell'LLM devono contenere unicamente profili target isolati senza contaminazioni incrociate.

- [ ] **3. Benchmark dell'Impronta di Token**
  - Il vettore di stato compilato dal runtime deve dimostrare una **riduzione minima dell'85%** nel conteggio dei token rispetto al flusso di input grezzo.
  - L'overhead di serializzazione deve essere verificato tramite profilazione di caratteri e token (`len(json.dumps(state_vector)) <= 512 bytes` per carichi di lavoro nominali).

- [ ] **4. Test Unitari degli Invarianti Termodinamici**
  - Test dei limiti di memoria: Verificare che `RAM.purge()` ripristini l'utilizzo a $\le 20\%$.
  - Test del raggio spaziale: Verificare che il raggio di prossimità rispetti l'equazione $r = \max(50.0, 175.0 - (W \cdot 6.5 + C \cdot 5.5))$.
  - Test di clamp difensivo: Verificare che `Ice_shield` prevenga il thermal throttling quando la RAM supera l'$85\%$.

---

## 4. Standard dei Commit Convenzionali & Ambiti HumOS

I messaggi di commit devono aderire tassativamente alla specifica **Conventional Commits 1.0.0**. Messaggi disordinati o generici (es. `update code`, `fix stuff`) saranno bloccati dagli hook di controllo del repository.

### 4.1 Struttura del Commit
```text
<tipo>(<ambito>): <breve riassunto imperativo>

[corpo opzionale con motivazione tecnica]

[piede opzionale con riferimenti a issue o modifiche incompatibili]
```

### 4.2 Tipi Approvati & Ambiti Specifici HumOS

| Ambito | Descrizione | Tipi Consentiti | Esempio |
| :--- | :--- | :--- | :--- |
| `lghos` | Grammatica core LINGHOS, scanner lessicale, aggiunte AST | `feat`, `fix`, `refactor` | `feat(lghos): add THREAD.suspend opcode support` |
| `parser` | Compilazione AST, motore di parsing, normalizzazione istruzioni | `fix`, `perf`, `test` | `fix(parser): resolve lookahead stall on nested IF blocks` |
| `cockpit` | Interfaccia Web, canvas radar SVG interattivo, console HTML/JS | `feat`, `fix`, `style` | `feat(cockpit): render active defense labels on SVG perimeter` |
| `gap` | Modulo di sicurezza G.A.P., interrupt ricorsivi, kill-switch | `sec`, `fix`, `feat` | `sec(gap): enforce mandatory timeout on unclassified inputs` |
| `spec` | Documentazione formale, contratti del linguaggio, guide | `docs` | `docs(spec): document RAM.alloc memory invariants` |
| `storage` | Persistenza scenari locali, serializzazioni JSON, sessioni | `feat`, `fix`, `test` | `feat(storage): support custom symbol de-registration` |

### 4.3 Esempi di Messaggi di Commit

#### ✅ Messaggi di Commit Validi
```bash
feat(lghos): implement RAM.alloc buffer reservation syntax
fix(parser): prevent variable leakage across multi-VM declarations
sec(gap): force TRIGGER.kill_switch execution on heart rate breach
docs(spec): update Section 3 primitive matrix with arity contracts
```

#### ❌ Messaggi di Commit Non Validi
```bash
updated readme.md                 # Mancano tipo e ambito
fix bug in script                 # Ambito non standard, tono non imperativo
WIP: cockpit stuff                # Tag provvisorio inammissibile nella cronologia
feat: added things to parser      # Manca l'ambito, verbo al passato
```

---

## 5. Configurazione dell'Ambiente di Sviluppo & Validazione

Per testare i contributi in locale:

```bash
# 1. Clona il repository
git clone https://github.com/SystemAdmin01/HumOS.git
cd HumOS

# 2. Valida il compilatore e il motore di memorizzazione
python3 -c "
from src.linghos.compiler import LINGHOSCompiler
from src.linghos.storage import GLOBAL_STORAGE
compiler = LINGHOSCompiler()
res = compiler.compile('Main() { Call >> Ice_shield; <<@end }')
assert res['telemetry']['ice_shield'] is True
print('Verifica del compilatore superata con successo.')
"

# 3. Avvia l'istanza locale del Cockpit
python3 src/app.py
```

---

*Redatto sotto il Gruppo di Specifica HumOS.*  
*Repository Ufficiale:* [https://github.com/SystemAdmin01/HumOS](https://github.com/SystemAdmin01/HumOS)
