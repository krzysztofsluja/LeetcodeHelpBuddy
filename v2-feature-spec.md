# v2 Feature Spec — **LeetCode Help Buddy** (DB-backed caching & reuse)

## 1) Goals & Non-Goals
- **Goals**
  - Persist generated test cases to reuse across users → lower latency & OpenAI cost.
  - Allow random sampling / tag-filtered selection from cached pool.
- **Non-Goals**
  - Executing solutions or storing expected outputs.

## 2) New Components
- **Postgres** (prod) / **SQLite** (dev) for persistence.
- **Repository Layer** `app/repo/test_case_repo.py`
  - `fetch(slug, schema_hash, count) -> list[TestCase]`
  - `save_many(cases: list[TestCase])`
- **Service Update**  
  `generator_service` queries repo → fallbacks to OpenAI → persists new cases.

## 3) DB Schema (1-row-per-case)

| column       | type           | notes                                      |
|--------------|---------------|--------------------------------------------|
| id           | BIGSERIAL PK  |                                           |
| slug         | TEXT          | user-provided LC slug                      |
| schema_hash  | CHAR(64)      | SHA-256 of JSON Schema (PII-safe)          |
| tag          | TEXT[]        | e.g. `{boundary,pairwise}`                 |
| input_json   | JSONB         | full input payload for this test case      |
| created_at   | TIMESTAMPTZ   | default `now()`                            |

Constraints  
```sql
UNIQUE (slug, schema_hash, input_json);
CREATE INDEX ix_cases_slug_hash ON test_cases (slug, schema_hash);
```

## 4) API Behaviour (unchanged)
- `/api/generate-tests` now serves from cache when possible.
- If fewer than requested `count`, generator tops-up via OpenAI and stores.

## 5) Compliance & Security
- Only schema hash stored; no raw statement text.
- User may opt-out of caching → service uses `NullRepo`.

## 6) Migration Path
1. Introduce repo interface with in-memory `NullRepo` (v1 compat).
2. Add SQLModel models + Alembic migration.
3. Wire Postgres in prod config.

## 7) Open Questions
- Opt-out flag location (`header?` `query?`).
- Eviction / retention policy for seldom-used cases.
- Do we store generation **notes** per case?

---