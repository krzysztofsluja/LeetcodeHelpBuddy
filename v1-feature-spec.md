# v1 Feature Spec — **LeetCode Help Buddy** (Python + Gradio)

> Scope for the first release: **(A)** generate high-quality test cases from user-provided *Constraints* + *Examples* and **(B)** explain the problem (progressive hints, no full solutions). App is a **standalone web app** built with **Python + Gradio**.

---

## 1) Goals & Non-Goals

**Goals**
- Deterministic **test-case generation** driven by the pasted statement (*Constraints* + *Examples*).
- Clear, scaffolded **problem explanation** (restatement, I/O shapes, pitfalls, hints) without shipping full solutions.
- **Graceful failure**: if required inputs are missing, ask for exactly what’s needed (no guessing).
- **ToS-friendly**: operate on **user-provided text**; do not crawl/scrape LeetCode.

**Non-Goals (v1)**
- No code execution / judging.
- No problem auto-identification or scraping.
- No LangChain/LangGraph; use the OpenAI SDK with **Structured Outputs** directly.

---

## 2) User Stories

- *As a learner*, I paste a problem’s **Constraints** and **Examples**, click “Generate tests,” and get a labeled set of edge/random/pairwise cases I can copy into LeetCode.
- *As a learner*, I paste a statement and click “Explain,” and get a concise restatement, I/O shapes, gotchas, and 3 escalating hints.
- *As a learner*, if I forget to include something, I get a **polite, actionable** message telling me exactly what to add.

---

## 3) System Overview (v1 components)

- **Gradio UI (Blocks/ChatInterface)** for a single text box + two buttons (“Generate tests” / “Explain”). Supports streaming for the explainer.
- **Deterministic parser** → extracts constraints, examples, basic types; builds a **JSON Schema (2020-12)** model.
- **Generators (Python):**
  - Boundary-value & equivalence-class inputs.
  - Optional **pairwise** combinations for multi-param cases.
- **Validation**: `jsonschema` validates each generated input against the schema.
- **LLM explainer** via OpenAI SDK **Structured Outputs** (typed JSON), streamed to UI.
- **Router (deterministic-first)**: rules route to “Generate tests” if constraints+examples are present; otherwise to “Explain” if user asked to explain; else show a clarifier (no guessing).

---

## 4) Feature A — Test-Case Generation

### A.1 Techniques we implement
- **Boundary-Value Analysis (BVA):** min, min±1, max−1, max, empty/size-1, etc.
- **Equivalence Partitioning (ECP):** valid/invalid classes per field (e.g., duplicates vs distinct).
- **Pairwise (All-Pairs) combinations** for parameters with multiple categories/ranges to keep coverage high without combinatorial explosion.

### A.2 Inputs → Schema
- Parse common patterns from text (e.g., `1 ≤ n ≤ 1e5`, `−1e9 ≤ nums[i] ≤ 1e9`, “lowercase letters”, “distinct”, “non-decreasing”).
- Produce **JSON Schema (2020-12)** capturing:
  - Types (array/object/scalars), bounds (min/max, minItems/maxItems), uniqueness (`uniqueItems`), string formats/regex.

### A.3 Generation & Validation
- Generate candidates with our BVA/ECP logic; optionally **pairwise** (e.g., via `allpairspy`). Validate each candidate with **`jsonschema`**.
- Output format: downloadable **JSON** and a human-readable table with **tags** (e.g., `[boundary]`, `[pairwise]`, `[duplicates]`).

### A.4 Acceptance criteria
- Given constraints `1 ≤ n ≤ 10^5`, element range `−10^9..10^9`, we produce:
  - Min/max length cases, off-by-one where applicable, extreme element values, duplicates/unique as constrained.
  - For ≥2 parameters with multiple categories, pairwise set is strictly smaller than full Cartesian product while covering **all value pairs**.

---

## 5) Feature B — Problem Explanation (no full solutions)

### B.1 Output contract (structured)
```json
{
  "restatement": "What problem is asking, in plain words...",
  "io_shapes": ["nums: int[]", "target: int"],
  "constraints": ["1 ≤ n ≤ 1e5", "−1e9 ≤ nums[i] ≤ 1e9"],
  "common_patterns": ["hash map", "two pointers iff sorted"],
  "edge_cases": ["n=0/1", "duplicates", "overflow risk"],
  "hints": [
    {"level": 1, "text": "Think about complements to reach target."},
    {"level": 2, "text": "Can O(n) time be traded for O(n) space?"},
    {"level": 3, "text": "Index lookup while scanning once."}
  ]
}
```

- Enforced via **OpenAI Structured Outputs** (JSON Schema) and streamed to UI for responsiveness.

### B.2 UX notes
- “Integrity mode” banner: we provide **hints, not full code**.
- Explanations are concise and escalate only on user request.

---

## 6) API (internal)

### `POST /parse-statement`
**in** `{ "statementText": string }`  
**out 200** `{ "schema": JSONSchema, "warnings": string[] }`  
**422** `{ "error": "NEEDS_CONSTRAINTS_OR_EXAMPLES", "missing": ["constraints","examples"] }`

### `POST /generate-tests`
**in** `{ "schema": JSONSchema, "count": number, "pairwise": boolean }`  
**out** `{ "cases": [{"input": any, "tags": string[]}], "notes": string[] }`

### `POST /explain`
**in** `{ "statementText": string, "mode": "beginner"|"intermediate"|"advanced" }`  
**out** *(as in §5.1, validated by Structured Outputs)*.

---

## 7) Gradio UI (Python)

- **Blocks** layout with a large textbox, two primary buttons (Generate / Explain), a results panel, and a small **inline clarifier** when required sections are missing.
- **ChatInterface** (optional) for the explanation flow; use **streaming** so tokens appear live.

---

## 8) Router (deterministic-first)

**Rules**
- If **Constraints + Examples** detected → route to **Generate tests**.
- If message starts with “explain/what does…” → **Explain**.
- Else show **clarifier**: “Paste *Constraints* and at least one *Example* input/output, or ask for an explanation.” (No auto-guessing.)

*(We’ll only invoke an LLM router later if we need fuzzy intent; not in v1.)*

---

## 9) Compliance & Security

- **No crawling/scraping** LeetCode; we only process user-pasted content, honoring their ToS.
- **Validation sandbox**: we do not execute user code in v1.
- **PII**: do not log raw statements unless user opts in.

---

## 10) Telemetry & Observability

- Count of successful parses vs. `NEEDS_CONSTRAINTS_OR_EXAMPLES`.
- Distribution of generated **tags** (boundary/pairwise/etc.).
- Latency for parsing and generation; token usage for explanations.

---

## 11) Definition of Done (DoD)

- **Parsing**: 90%+ of sample statements correctly extract numeric/string/array bounds into JSON Schema (spot-checked).
- **Generation**: For multi-param inputs, pairwise mode produces a set that covers **all value pairs** (verified with a checker), and every case validates against the schema.
- **Explanation**: Output validates against schema (Structured Outputs); streams in Gradio.
- **UX**: Clarifier preserves user input and provides actionable guidance.
- **ToS**: No network calls to LeetCode content endpoints.

---

## 12) Libraries & References (non-exhaustive)

- **Python**: `jsonschema`, `allpairspy` (optional), `pydantic` (for schemas), OpenAI Python SDK, Gradio.
- **Design/UX**: Nielsen Norman Group guidance on constructive error messages.
- **Testing**: NIST combinatorial testing resources (pairwise and t-way).

---

## 13) Open Questions (track, but not blocking v1)

- Do we want an **optional** pairwise toggle in UI or always on for ≥2 parameters?
- Should we add a minimal **seed** field for reproducibility of random cases?
- Do we restrict explanation modes by difficulty (beginner/intermediate/advanced) at launch?

---

## 14) Milestones

- **M1 — Parser & Schema**: extract constraints/examples → JSON Schema; validations green.
- **M2 — Generators**: BVA + ECP + pairwise; output JSON + readable tags; schema-validated.
- **M3 — Explainer**: Structured Outputs + streaming UI; integrity mode on.
- **M4 — UX polish**: clarifier messages; copy buttons; download `.json`.
- **M5 — Beta hardening**: telemetry, rate limits, content policy checks.

---

### Appendix A — JSON Schema snippet (illustrative)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "nums": {
      "type": "array",
      "minItems": 0,
      "maxItems": 100000,
      "items": { "type": "integer", "minimum": -1000000000, "maximum": 1000000000 }
    },
    "target": { "type": "integer", "minimum": -2000000000, "maximum": 2000000000 }
  },
  "required": ["nums","target"]
}
```
