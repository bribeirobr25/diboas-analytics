# FILE: 02_v4_phase0_core_contracts.md

# diBoaS v4 — Phase 0 Core Contracts (Truth Spine)

**Document ID:** V4-P0-CONTRACTS-001  
**Status:** Enforceable list for Phase 0 implementation  
**Rule:** No contract = no ingest

This list defines the smallest set of **granular** Truth Contracts required to produce one reproducible weekly Adelaide edition.

Bundles are presentation-only. Contracts remain granular for debuggability.

---

## SLA definitions
- **internal_sla:** max age tolerated for pipeline health (alerts/tasks)
- **publication_sla:** max age allowed when referenced in a published edition (hard blocker)

---

## Core Contracts (Phase 0)

### A) Rates & Macro (TradFi cadence)
1. `rates_us2y_yield_v1`  
2. `rates_us10y_yield_v1`  
3. `rates_us30y_yield_v1`  
4. `rates_2s10s_spread_v1` (derived; explicit formula required)  
5. `rates_us10y_real_yield_v1` (proxy acceptable; disclose)  
6. `macro_us_inflation_breakeven_10y_v1` (proxy acceptable; disclose)  
7. `macro_global_liquidity_proxy_v1` (lagging; disclosure required)

### B) TradFi risk & positioning (proxies allowed with disclosure)
8. `fx_usd_index_proxy_v1`  
9. `equity_spx_proxy_v1`  
10. `vol_vix_proxy_v1`  
11. `credit_hy_ig_spread_proxy_v1`

### C) Crypto spot & structure (fast cadence)
12. `crypto_btc_spot_usd_v1`  
13. `crypto_eth_spot_usd_v1`  
14. `crypto_btc_perps_funding_v1`  
15. `crypto_btc_perps_open_interest_v1`  
16. `crypto_eth_perps_funding_v1`  
17. `crypto_eth_perps_open_interest_v1`

### D) Stablecoins (health + stress)
18. `stablecoin_total_supply_v1`  
19. `stablecoin_depeg_events_v1` (near-real-time; critical)

### E) DeFi baseline
20. `defi_bluechip_tvl_v1`  
21. `defi_yield_benchmark_v1` (composite; methodology disclosure)

### F) Bridge: RWA (recommended to include in Phase 0)
22. `rwa_tokenized_treasury_tvl_nav_v1` (issuer + on-chain verification if possible; lag disclosure)  
23. `rwa_tokenized_treasury_net_flows_v1` (derived formula required if computed from TVL/NAV deltas)

---

## Default SLA targets (initial)
| Contract group | internal_sla | publication_sla | Notes |
|---|---:|---:|---|
| Rates / TradFi proxies | <24h | <48h | TradFi holidays allowed; forward-fill permitted only per policy |
| Macro liquidity proxy | <14d | <14d | **Lag disclosure required in any edition that references it** |
| Crypto spot/perps | <60m | <12h | No forward-fill allowed |
| Stablecoin depeg events | <15m | <4h | Critical escalation |
| DeFi TVL/yield | <24h | <48h | Composite + heterogeneity disclosures as needed |
| RWA TVL/flows | <48h | <72h | Issuer lag disclosure required |

---

## Publication rule
If a contract is referenced in an edition but exceeds publication_sla → **block publication**.