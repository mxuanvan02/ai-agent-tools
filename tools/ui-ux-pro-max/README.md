# UI/UX Pro Max for AI Agents

> **UI/UX Design Intelligence with Cognitive Psychology & Extreme Minimalism Framework**  
> *Searchable local intelligence for web, mobile, and desktop interfaces. Built for AI agents and human designers who demand clean, calm, and psychologically sound products.*

---

## Overview

`ui-ux-pro-max` is a high-density, zero-network design intelligence engine. It arms AI agents with structured design knowledge across 12 distinct domains, 22 technical stacks, and a cognitive psychology framework grounded in how human perception, attention, and decision-making actually operate.

### Key Capabilities
- **Design System Generation**: Automatically synthesize color palettes, font pairings, component styles, and anti-patterns tailored to specific product domains and user demographics.
- **Cognitive & Behavioral Psychology**: Enforces Calm Technology, the 60-30-10 color rule, Hick's Law, the Zeigarnik Effect, the Von Restorff Isolation Effect, and tactile micro-interactions.
- **Extreme Minimalism ("Zero-Filler Prose")**: Strips conversational fluff, unnecessary greetings, and obvious explanations in favor of high-glanceability metric deltas, semantic pills, and clean action hierarchies.
- **Deterministic & Offline**: 100% standard library Python 3. No external dependencies, no API keys, no network calls.

---

## Dataset Architecture

| Resource | Count | Primary Source | Purpose |
| :--- | :--- | :--- | :--- |
| **Searchable Styles** | 79 (50 active) | `data/styles.csv` | Visual aesthetics (Glassmorphism, Bento, Brutalism, Minimal, etc.) |
| **Product Palettes** | 192 | `data/products.csv` | Industry-tuned primary, secondary, and accent color scales |
| **Reasoning Profiles** | 192 | `data/ui-reasoning.csv` | Multi-variable rules selecting optimal style/font/color combos |
| **Font Pairings** | 74 | `data/font-pairings.csv` | Typography harmonies with Google Fonts fallbacks |
| **UX Guidelines** | **127** | `data/ux-guidelines.csv` | Actionable rules including cognitive psychology & minimalism |
| **Curated Icons** | 105 | `data/icons.csv` | Standard Phosphor / Heroicons mappings |
| **Motion Presets** | 17 | `data/motion-presets.csv` | GSAP / CSS easing, durations, and transitions |
| **Chart Types** | 25 | `data/charts.csv` | Data visualization selection matrix |
| **Supported Stacks** | 22 | `data/stacks/` | Implementation guidelines (React, Next.js, Tailwind, Vue, iOS, etc.) |

---

## Cognitive & Behavioral Psychology Framework

Interfaces built with `ui-ux-pro-max` are governed by 8 core psychological principles:

1. **Calm Technology & 60-30-10 Rule**: Prevent sensory overload by allocating 60% to neutral surfaces, 30% to structural hierarchy, and strictly 10% to intentional accents.
2. **Zero-Filler Prose & Pre-attentive Scanning**: Eliminate conversational filler. People scan in F/Z patterns; communicate through bold metric deltas, clear status pills, and concise verbs.
3. **Hick's Law & Choice Architecture**: Minimize cognitive fatigue by limiting primary viewport choices to 3–5 actions. Defer advanced tools via Progressive Disclosure.
4. **Zeigarnik Effect & Visual Feedback**: Calm the anxiety of unfinished tasks with explicit progress indicators (`Step 2 of 4`) and reassuring auto-save indicators.
5. **Von Restorff Isolation Effect**: Ensure the single most critical Call-to-Action stands out via elevated contrast, leaving secondary actions muted or outlined.
6. **Peak-End Rule & Moments of Delight**: Anchor positive product sentiment at task peaks and completion moments with smooth success modals and friction-free next steps.
7. **Fitts's Law & Tactile Micro-Interactions**: Reinforce user agency with minimum touch targets (≥44pt) and tactile compression feedback (`button:active { transform: scale(0.98); }`).
8. **Pre-attentive Visual Hierarchy**: Anchor critical metrics at top-left with significant font scale contrast (e.g. 28px bold value vs 12px uppercase label).

---

## CLI Usage

All queries run via the bundled standalone CLI `scripts/search.py`:

```bash
# 1. Generate full design system for a product
python3 scripts/search.py "hotel hospitality property management" --design-system -p "StayOps"

# 2. Search specific UX domain for psychology guidelines
python3 scripts/search.py "psychology calm" --domain ux

# 3. Search for extreme minimalism & content rules
python3 scripts/search.py "minimalism" --domain ux

# 4. Search technical implementation rules for a stack
python3 scripts/search.py "table pagination virtual list" --stack nextjs

# 5. Search curated icons
python3 scripts/search.py "calendar check bell" --domain icons
```

---

## Validation & Quality Gates

To verify data contract compliance across all CSV/JSON records:

```bash
python3 scripts/validate_data.py
python3 scripts/public_hygiene_check.py
```

Both commands must exit with code `0`.

---

## License

MIT License. Copyright (c) 2026 Mai Xuan Van.
