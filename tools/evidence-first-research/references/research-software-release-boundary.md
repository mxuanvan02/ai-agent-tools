# Research-software public release boundary

Use when cleaning, documenting, packaging, or publishing a research-code repository.

## Public configuration
- Never commit API keys, tokens, real provider URLs, deployment-specific model identifiers, or local paths.
- Keep the default workflow offline and deterministic where possible.
- If remote execution is supported, commit only a non-routable template (for example, an `.invalid` endpoint), a model placeholder, and the *name* of an environment variable for the credential.
- Ignore `.env`, local/private config files, and instantiated remote configs. State that an opted-in endpoint receives the supplied evidence and authorization header.
- Add a regression/audit rule that fails if a tracked remote config contains a concrete endpoint or model rather than approved placeholders.

## README structure for scientific software
1. One-sentence artifact scope: what the software implements and what it does not release.
2. Method/artifact model: the scientific objects, contracts, or algorithms implemented.
3. Installation and a fully offline reproduction path.
4. Optional remote execution: copy a tracked template to an ignored local file; replace placeholders locally; export the credential variable.
5. Commands and repository layout.
6. Data governance: rights-cleared fixtures versus restricted/source-derived materials.
7. Citation and license.

Describe only claims that validation supports. Separate structural/integrity validation from semantic, factual, pedagogical, or effectiveness claims.

## Release gate
Before publishing: inspect tracked files for secrets/concrete remote settings; run tests, offline validation, policy/boundary audit, and package build; inspect `git diff --check`; stage specific files; commit and push only after user approval. For a manuscript source ZIP, include exactly the files needed to compile (`.tex`, `.bib`, used figures, build README), exclude auxiliary files and unused figures, then compile from a clean extraction.