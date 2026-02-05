# Pre-Implementation Review
## Feedback on P0 Execution Plan

**Status:** Plan is 90% ready. Address these items before starting implementation.

---

## 1. CRITICAL: Priority Order Correction

**Current plan:** P0-1 → P0-2 → P0-3 → P0-4 → P0-5a → P0-5b

**Correct order (per handoff):** P0-1 → P0-3 → P0-2 → P0-4 → P0-5a → P0-5b

**Why:** Brazil is Day 1. CVM compliance (P0-3) is a legal blocker that outranks Sky cap (P0-2). Do not put regulatory compliance third because JSON feels easier than disclaimers.

---

## 2. CRITICAL: Missing L4 Depeg Triggers

**Issue:** Plan implements L2/L3 only. Handoff specifies L2/L3/L4 pattern.

**Fix:** Add L4 triggers for both USDC and USDT:
- L2: >1% depeg (P2_MEDIUM)
- L3: >2% depeg (P1_HIGH)  
- **L4: >5% depeg (P0_CRITICAL)** ← Missing

Without L4, system reports "fine" during an actual crisis.

---

## 3. Collector Write Locations — Verify Coverage

**Plan lists 7 CSV write locations but may be missing:**
- `coingecko_collector.py`
- `defillama_collector.py`
- `alternative_collector.py`

**Action:** Search codebase for all `df.to_csv()` and `to_csv()` calls. Verify each is covered or goes through a reporter that will be updated.

```bash
grep -rn "to_csv" src/collectors/ src/reporters/
```

---

## 4. Atomic Write Implementation Details

The `safe_write` utility needs these specifics:

| Requirement | Why |
|-------------|-----|
| Temp file in **same directory** as target | `os.replace()` only atomic on same filesystem |
| Add `flush()` + `os.fsync()` before replace | Atomic ≠ durable; protects against power loss |
| Clean up temp file in exception handler | Don't leave orphan `.tmp` files |
| Use `index=False` consistently | Most pipelines expect this |
| Use `encoding='utf-8-sig'` for CSV | Portuguese characters break Excel without BOM |

**Refined pattern:**
```python
def safe_write_csv(df: pd.DataFrame, filepath: Path, min_rows: int = 1, allow_empty: bool = False) -> bool:
    if df is None or (df.empty and not allow_empty):
        logger.warning(f"Rejecting empty write to {filepath}")
        return False
    
    temp_path = filepath.parent / f"{filepath.name}.tmp"  # Same directory!
    try:
        df.to_csv(temp_path, index=False, encoding='utf-8-sig')
        with open(temp_path, 'a') as f:
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_path, filepath)
        return True
    except Exception as e:
        logger.error(f"Write failed: {e}")
        if temp_path.exists():
            temp_path.unlink()  # Cleanup
        raise
```

**Note:** `allow_empty=False` is default for collectors (strict). Reporters may need `allow_empty=True` for "no signals today" scenarios.

---

## 5. CVM Validator Fragility

**Issue:** Regex patterns will break on:
- Markdown formatting (`**bold**`)
- Case variations (`Não` vs `não` vs `NAO`)
- Accent variations (`não` vs `nao`)
- Minor copy edits

**Fix:** Normalize content before validation:
```python
def _normalize_for_validation(self, content: str) -> str:
    import re
    import unicodedata
    # Remove markdown
    content = re.sub(r'\*+', '', content)
    content = re.sub(r'#+\s*', '', content)
    # Lowercase
    content = content.lower()
    # Normalize accents (optional: keep or remove)
    content = unicodedata.normalize('NFKD', content)
    return content
```

Also: Log **which specific part is missing** (BR-CVM-001, 002, or 003) so debugging is fast.

---

## 6. Affected Strategies — Verify Against Data

**Issue:** Plan hardcodes `USDC_AFFECTED_STRATEGIES = [1, 3, 5, 7, 9]`

**Action:** 
1. Verify this against actual `strategies.json` allocations
2. Add comment documenting where the mapping comes from
3. Consider a test that fails if strategy IDs change

```python
# Strategies using USDC-exposed protocols (Aave, Compound)
# Source: strategies.json allocations as of 2026-02-03
# Update if strategy allocations change
USDC_AFFECTED_STRATEGIES = [1, 3, 5, 7, 9]
```

---

## 7. Sky Cap Validator — Return All Violations

**Instead of:** Raising exception on first violation

**Do:** Return list of all violations so user sees complete picture

```python
def validate_sky_cap(strategies: List[Strategy]) -> List[str]:
    """Returns list of violation messages (empty = valid)."""
    violations = []
    for s in strategies:
        sky = s.allocations.get('stable', {}).get('sky', 0)
        if sky > MAX_SKY_ALLOCATION + 0.0001:  # Float tolerance
            violations.append(f"Strategy {s.id} ({s.name}): Sky at {sky*100:.1f}% exceeds 30% cap")
    return violations
```

Also: Ensure allocations still sum to 1.0 after redistribution.

---

## 8. Hypothetical Disclaimer — CSV Strategy

**Plan says:** "metadata row or separate file"

**Decision:** Use **separate companion file** (e.g., `results_disclaimer.txt`)

**Why:** Don't break CSV consumers that expect pure tabular data.

---

## 9. Missing Test Files

**Plan has inline verification but doesn't add persistent tests.**

**Add these test files:**
- `tests/test_file_io.py` — safe_write utility
- `tests/validators/test_strategy_validator.py` — Sky cap validation  
- `tests/triggers/test_stablecoin_depeg.py` — USDC/USDT triggers
- `tests/validators/test_cvm_validator.py` — CVM 3-part structure

At minimum, 1 unit test per new validator and trigger.

---

## 10. Pre-Implementation Checklist

Before starting any code changes:

```bash
# 1. Backup critical files
cp config/strategies.json config/strategies.json.bak
cp src/adelaide/localization.py src/adelaide/localization.py.bak

# 2. Verify all tests pass
pytest tests/ -v --tb=short

# 3. Document current state
ls -la data/*.csv > data_inventory_before.txt

# 4. Create feature branch
git checkout -b p0-launch-fixes
```

---

## 11. Post-Implementation Checklist

After all P0s complete:

```bash
# 1. Run full test suite
pytest tests/ -v

# 2. Run end-to-end pipeline (not just unit tests)
python src/main.py --mode=simulation  # or equivalent

# 3. Generate sample Adelaide output for each locale
# Manually verify PT-BR has CVM 3-part structure

# 4. Verify no .tmp files left behind
find . -name "*.tmp" -type f
```

---

## Summary: Fix Before Implementation

| # | Item | Severity |
|---|------|----------|
| 1 | Reorder: P0-3 before P0-2 | 🔴 Critical |
| 2 | Add L4 depeg triggers | 🔴 Critical |
| 3 | Verify all collector write locations | 🟡 Important |
| 4 | Atomic write: same dir + fsync + cleanup | 🟡 Important |
| 5 | CVM validator: normalize content | 🟡 Important |
| 6 | Verify affected strategies against data | 🟡 Important |
| 7 | Sky validator: return all violations | 🟢 Minor |
| 8 | CSV disclaimer: use separate file | 🟢 Minor |
| 9 | Add test files | 🟢 Minor |
| 10-11 | Pre/post checklists | 🟢 Minor |

---

**Once these are addressed, the plan is ready for implementation.**
