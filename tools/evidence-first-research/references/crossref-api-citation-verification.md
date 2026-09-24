# Crossref API Citation Verification Pattern

## When to use

When người dùng needs **verified citations** (DOI-backed, not hallucinated) for a manuscript section — especially for context citations outside the PRISMA core corpus (e.g., region-specific evidence for Discussion/Recommendations).

## Core technique

### Single DOI verification

```bash
curl -sS -m 25 "https://api.crossref.org/works/<DOI>"
```

Returns JSON with `message.title`, `message.author`, `message.issued`, `message.container-title`, `message.DOI`. Parse with `python3 -c "import json,sys; d=json.load(sys.stdin)['message']; ..."`.

### Keyword search (discovery)

```bash
curl -sS -m 25 "https://api.crossref.org/works?query=<URL-encoded-query>&rows=4&select=title,author,issued,container-title,DOI"
```

Returns up to `rows` items sorted by relevance. Use `select=` to reduce payload.

### Batch pattern (execute_code)

```python
from hermes_tools import terminal
import json, urllib.parse

queries = ["LoRaWAN Vietnam agriculture", "greenhouse Da Lat", ...]
for q in queries:
    qe = urllib.parse.quote(q)
    cmd = f'curl -sS -m 25 "https://api.crossref.org/works?query={qe}&rows=4&select=title,author,issued,container-title,DOI"'
    r = terminal(command=cmd, timeout=35)
    items = json.loads(r["output"])["message"]["items"]
    for it in items:
        yr = it.get('issued',{}).get('date-parts',[['?']])[0][0]
        title = it.get('title',['?'])[0]
        # ... print/filter
```

## Key pitfalls

1. **Google/Bing/DuckDuckGo block bots** — don't waste time on search engines for academic sources. Go straight to Crossref API.
2. **Vietnamese gov portals** (lamdong.gov.vn, thuvienphapluat.vn, gso.gov.vn) typically return 403/404 to headless requests — note as "chưa verify URL" and use peer-reviewed sources as primary citation.
3. **Crossref doesn't have every paper** — Vietnamese-language journals, theses, and government reports often missing. For those, cite by institution/title/year and mark confidence level.
4. **DOI format matters** — always lowercase, no URL prefix when querying API (`10.3390/su13126603` not `https://doi.org/...`).
5. **Abstract stripping** — Crossref returns JATS XML in abstract field. Strip with `re.sub(r'<[^>]+>', '', abstract)`.

## Integration into thesis workflow

- New citations for Discussion/Recommendations go into `references.bib` with a comment block marking them as "REGION-EVIDENCE" (not part of n=64 PRISMA corpus).
- Each entry must have `doi` field (bibtex key for traceability).
- After adding entries: full build chain with bibtex-from-output-dir fix (see SKILL.md bibtex pitfall).
- Verify: `grep -c '\\bibitem' build/main.bbl` must match expected total.

## Sources verified in session 2026-06-24

| Key | DOI | Year | Topic |
|-----|-----|------|-------|
| tran2021lamdong | 10.3390/su13126603 | 2021 | Robusta coffee irrigation Lâm Đồng |
| tran2023daklak | 10.2166/ws.2023.330 | 2023 | Coffee irrigation Đắk Lắk/Gia Lai |
| nghiem2020sonla | 10.3390/land9020056 | 2020 | Smallholder coffee Sơn La |
| markussen2016fragmentation | 10.35188/UNU-WIDER/2016/054-6 | 2016 | Land fragmentation VN |
| tranvu2019fragmentation | 10.1016/j.landusepol.2019.104247 | 2019 | Land fragmentation income VN |
| phihung2022perihanoi | 10.55677/ijlsar/v01i03y2022-02 | 2022 | Peri-urban vegetable Hanoi |
| truong2025vnfuzzy | 10.11591/ijres.v14.i2.pp440-451 | 2025 | IoT fuzzy agriculture VN |
| petajajarvi2015lora | 10.1109/ITST.2015.7377400 | 2015 | LoRa range evaluation |
| citoni2019lorawan | 10.1109/IOTM.0001.1900043 | 2019 | LoRaWAN smart farming |
| sinha2017lpwa | 10.1016/j.icte.2017.03.004 | 2017 | LPWA survey LoRa/NB-IoT |
| soy2023coverage | 10.3390/s23218859 | 2023 | LoRa/NB-IoT coverage agriculture |
| ayaz2019iot | 10.1109/ACCESS.2019.2932609 | 2019 | IoT smart agriculture survey |
| boulard1995ventilation | 10.1006/jaer.1995.1028 | 1995 | Greenhouse air exchange model |
| ruizgarcia2009wsn | 10.3390/s90604728 | 2009 | WSN agriculture review |
