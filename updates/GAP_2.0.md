# G.A.P. 2.0 — Gestione Attiva delle Percezioni e delle Evidenze

> **HumOS V.18.4.0** · Modulo C++ di riferimento · Prototipo dimostrativo compilabile

---

## Scopo

Separare **percezioni**, **osservazioni** ed **evidenze**; classificare lo stato epistemico senza trasformare l'assenza di prove in una prova di assenza.

## Limiti espliciti

- Non effettua verifiche autonome nel mondo reale.
- Non diagnostica condizioni psicologiche.
- Non decide se una persona o una situazione sia pericolosa.
- È un componente dimostrativo per organizzare informazioni dichiarate dall'operatore.

---

## Compilazione

```bash
c++ -std=c++17 -Wall -Wextra -pedantic GAP_2.0.cpp -o gap_demo
./gap_demo
```

---

## Struttura dati

### Stati epistemici (`EvidenceState`)

| Stato | Significato |
|---|---|
| `Supported` | Evidenze attendibili **sostengono** l'ipotesi |
| `Disconfirmed` | Evidenze attendibili **contraddicono** l'ipotesi |
| `Insufficient` | Dati assenti o insufficienti per concludere |
| `Conflicting` | Evidenze attendibili ma **discordanti** |

> [!IMPORTANT]
> `Insufficient` ≠ falso. L'assenza di prove non è prova di assenza.

### Polarità evidenza (`EvidencePolarity`)

| Valore | Descrizione |
|---|---|
| `Supports` | L'evidenza supporta l'ipotesi |
| `Contradicts` | L'evidenza contraddice l'ipotesi |
| `Neutral` | Irrilevante per la valutazione |

### Qualità evidenza (`EvidenceQuality`)

| Valore | Descrizione |
|---|---|
| `Low` | Non sufficiente da sola per classificare |
| `Medium` | Accettabile con verifica |
| `High` | Affidabile e verificata |

---

## Strutture principali

### `Evidence` — una singola evidenza

```cpp
struct Evidence {
    std::string description;           // Descrizione dell'evidenza
    std::string source;                // Fonte
    std::string observed_at;           // Data/momento dell'osservazione
    EvidencePolarity polarity;         // Supports / Contradicts / Neutral
    EvidenceQuality  quality;          // Low / Medium / High
    bool independently_verifiable;    // Verificabile in modo indipendente?
};
```

### `CaseFile` — il caso da valutare

```cpp
struct CaseFile {
    std::string id;                        // Identificatore univoco
    std::string perceived;                 // Pensiero, timore o interpretazione
    std::vector<std::string> observations; // Fatti osservati (senza interpretarli)
    std::vector<Evidence>    evidence;     // Elementi con fonte e qualità
    std::vector<std::string> unknowns;     // Informazioni mancanti
};
```

### `Evaluation` — esito della valutazione

```cpp
struct Evaluation {
    EvidenceState state;              // Stato epistemico risultante
    std::size_t   supporting_count;  // Evidenze usabili che supportano
    std::size_t   contradicting_count;
    std::size_t   low_quality_count; // Evidenze scartate per qualità o non verificabilità
    std::string   rationale;         // Motivazione testuale
    bool          requires_review;   // Richiede revisione contestuale
};
```

---

## Logica di valutazione

Un'evidenza è **usabile** (`is_usable`) solo se soddisfa **tutti** i criteri:

```cpp
inline bool is_usable(const Evidence& item) {
    return item.independently_verifiable          // verificabile
        && item.quality != EvidenceQuality::Low   // non di qualità bassa
        && item.polarity != EvidencePolarity::Neutral; // non neutrale
}
```

### Regole di classificazione (`evaluate`)

```
has_support && has_contradiction  →  CONFLICTING  (revisione obbligatoria)
has_support only                  →  SUPPORTED    (verificare contesto)
has_contradiction only            →  DISCONFIRMED (aggiornare senza negare l'esperienza)
nessuno dei due                   →  INSUFFICIENT (esito incerto; non equivale a falso)
```

---

## Output del report

```
[GAP_CASE]                   GAP-DEMO-001
[PERCEIVED]                  Temo che una conversazione fosse riferita a me.
[OBSERVATIONS]               1
[EVIDENCE]                   0
[UNKNOWN]                    1
[STATE]                      INSUFFICIENT
[SUPPORTING]                 0
[CONTRADICTING]              0
[LOW_QUALITY_OR_UNVERIFIED]  0
[REASON]                     Non ci sono evidenze utilizzabili sufficienti. L'esito
                             resta incerto: assenza di prove non significa prova di assenza.
[REVIEW_REQUIRED]            YES
[ACTIVE_ATTENTION]           NO
[ARCHIVE]                    Originale conservato per eventuale revisione.
```

---

## Funzione `release_attention`

```cpp
inline ArchivedCase release_attention(const CaseFile& input, const Evaluation& evaluation);
```

Archivia il caso originale e rimuove il contenuto dall'attenzione attiva.

> [!NOTE]
> `release_attention` **non** cancella il pensiero, **non** lo dichiara falso e **non** elimina la possibilità di riaprire il caso quando emergono nuove informazioni.

---

## Sorgente completo

```cpp
// ============================================================================
// HumOS V.18.4.0 — G.A.P. 2.0
// Gestione Attiva delle Percezioni e delle Evidenze
// Compilazione: c++ -std=c++17 -Wall -Wextra -pedantic GAP_2.0.cpp -o gap_demo
// ============================================================================

#include <algorithm>
#include <cstddef>
#include <iostream>
#include <string>
#include <utility>
#include <vector>

namespace humos::gap {

enum class EvidenceState {
    Supported,    // Evidenze attendibili sostengono l'ipotesi.
    Disconfirmed, // Evidenze attendibili contraddicono l'ipotesi.
    Insufficient, // Dati assenti o insufficienti per concludere.
    Conflicting   // Evidenze attendibili ma discordanti.
};

enum class EvidencePolarity { Supports, Contradicts, Neutral };
enum class EvidenceQuality  { Low, Medium, High };

struct Evidence {
    std::string      description;
    std::string      source;
    std::string      observed_at;
    EvidencePolarity polarity{EvidencePolarity::Neutral};
    EvidenceQuality  quality{EvidenceQuality::Low};
    bool             independently_verifiable{false};
};

struct CaseFile {
    std::string              id;
    std::string              perceived;
    std::vector<std::string> observations;
    std::vector<Evidence>    evidence;
    std::vector<std::string> unknowns;
};

struct Evaluation {
    EvidenceState state{EvidenceState::Insufficient};
    std::size_t   supporting_count{0};
    std::size_t   contradicting_count{0};
    std::size_t   low_quality_count{0};
    std::string   rationale;
    bool          requires_review{false};
};

struct ArchivedCase {
    CaseFile   original;
    Evaluation latest_evaluation;
    bool       active_attention{false};
};

inline bool is_usable(const Evidence& item) {
    return item.independently_verifiable
        && item.quality  != EvidenceQuality::Low
        && item.polarity != EvidencePolarity::Neutral;
}

inline Evaluation evaluate(const CaseFile& input) {
    Evaluation result;

    for (const auto& item : input.evidence) {
        if (item.quality == EvidenceQuality::Low || !item.independently_verifiable)
            ++result.low_quality_count;
        if (!is_usable(item)) continue;

        if (item.polarity == EvidencePolarity::Supports)    ++result.supporting_count;
        else if (item.polarity == EvidencePolarity::Contradicts) ++result.contradicting_count;
    }

    const bool has_support       = result.supporting_count    > 0;
    const bool has_contradiction = result.contradicting_count > 0;

    if (has_support && has_contradiction) {
        result.state          = EvidenceState::Conflicting;
        result.rationale      = "Sono presenti evidenze utilizzabili in entrambe le "
                                "direzioni; serve una revisione del contesto e delle fonti.";
        result.requires_review = true;
    } else if (has_support) {
        result.state          = EvidenceState::Supported;
        result.rationale      = "Le evidenze utilizzabili sostengono l'ipotesi; verificare "
                                "proporzionalmente il contesto prima di decidere.";
        result.requires_review = true;
    } else if (has_contradiction) {
        result.state          = EvidenceState::Disconfirmed;
        result.rationale      = "Le evidenze utilizzabili contraddicono l'ipotesi; "
                                "aggiornare la valutazione senza negare l'esperienza soggettiva.";
        result.requires_review = false;
    } else {
        result.state          = EvidenceState::Insufficient;
        result.rationale      = "Non ci sono evidenze utilizzabili sufficienti. "
                                "L'esito resta incerto: assenza di prove non significa prova di assenza.";
        result.requires_review = true;
    }

    return result;
}

inline std::string to_string(EvidenceState state) {
    switch (state) {
        case EvidenceState::Supported:    return "SUPPORTED";
        case EvidenceState::Disconfirmed: return "DISCONFIRMED";
        case EvidenceState::Insufficient: return "INSUFFICIENT";
        case EvidenceState::Conflicting:  return "CONFLICTING";
    }
    return "UNKNOWN";
}

// Archivia senza cancellare. Non dichiara il pensiero falso.
// Il caso può essere riaperto quando emergono nuove informazioni.
inline ArchivedCase release_attention(const CaseFile& input, const Evaluation& evaluation) {
    ArchivedCase archived;
    archived.original           = input;
    archived.latest_evaluation  = evaluation;
    archived.active_attention   = false;
    return archived;
}

inline void print_report(const CaseFile& input, const Evaluation& evaluation) {
    std::cout << "[GAP_CASE] "                 << input.id                        << '\n';
    std::cout << "[PERCEIVED] "                << input.perceived                 << '\n';
    std::cout << "[OBSERVATIONS] "             << input.observations.size()       << '\n';
    std::cout << "[EVIDENCE] "                 << input.evidence.size()           << '\n';
    std::cout << "[UNKNOWN] "                  << input.unknowns.size()           << '\n';
    std::cout << "[STATE] "                    << to_string(evaluation.state)     << '\n';
    std::cout << "[SUPPORTING] "               << evaluation.supporting_count     << '\n';
    std::cout << "[CONTRADICTING] "            << evaluation.contradicting_count  << '\n';
    std::cout << "[LOW_QUALITY_OR_UNVERIFIED] "<< evaluation.low_quality_count    << '\n';
    std::cout << "[REASON] "                   << evaluation.rationale            << '\n';
    std::cout << "[REVIEW_REQUIRED] "          << (evaluation.requires_review ? "YES" : "NO") << '\n';
}

} // namespace humos::gap

#ifndef GAP_NO_MAIN
int main() {
    using namespace humos::gap;

    CaseFile sample;
    sample.id        = "GAP-DEMO-001";
    sample.perceived = "Temo che una conversazione fosse riferita a me.";
    sample.observations.push_back("Ho sentito una frase, ma non era chiaro a chi fosse rivolta.");
    sample.unknowns.push_back("Non conosco il contesto completo della conversazione.");

    // Nessuna evidenza verificabile → INSUFFICIENT (non falso positivo).
    const Evaluation    result   = evaluate(sample);
    print_report(sample, result);

    const ArchivedCase  archived = release_attention(sample, result);
    std::cout << "[ACTIVE_ATTENTION] " << (archived.active_attention ? "YES" : "NO") << '\n';
    std::cout << "[ARCHIVE] Originale conservato per eventuale revisione.\n";

    return 0;
}
#endif
```

---

*Parte dell'ecosistema HumOS · [← Torna agli update](README.md)*
