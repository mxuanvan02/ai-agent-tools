# OmniProxy TLV pilot: direct API path

Use this when người dùng asks to run a small multimodal bài TQA-generation pilot and the frozen data plus OmniProxy/model are already available, but a full runner is unfinished.

## Preconditions

1. Probe the OpenAI-compatible endpoint using `/v1/models`; record HTTP status and model IDs, never secrets.
2. For this verified session environment: OmniProxy `http://127.0.0.1:20131`; `gpt-5.6-terra` accepted a real image at `/v1/chat/completions`.
3. Freeze a manifest that records chunk/document IDs, condition, source image paths, byte counts, SHA-256 values, and excludes machine-generated visual descriptions.

## Minimal direct-API execution

- Send base text for `T`; text plus structural fields for `TL_struct`; and base text/structure plus original image bytes for `TLV`.
- Encode original images as OpenAI-compatible `image_url` data URLs (base64), after rechecking bytes and SHA-256 immediately before the call.
- Record each response as JSONL with: `experiment_id`, `chunk_id`, `condition`, `method`, requested/returned model, prompt version/hash, input hash, whether an image was attached, status/reason, parsed response, raw response/hash, and elapsed time.
- Before a broad run, execute at least 3–5 clear TLV cases for ECM. A one-case probe only proves the route works.

## Fail-closed statuses

- Image absent, unreadable, size/hash mismatch: `BLOCKED_INPUT_INTEGRITY`.
- Backend rejects/does not support the image request: `BLOCKED_UNSUPPORTED_IMAGE_INPUT`; never retry in text-only mode.
- Invalid JSON or missing schema fields: `REJECTED`.
- ECM needs nonempty `motif`, `derivation`, `answer_parts`, and `trace`. For a TLV case designed to require the picture, require at least one `trace` item with `source: "image"`; otherwise `REJECTED`.

## Claim boundary and reporting

`PARSED` means only that the model output passed the format/contract checks. It does not establish semantic correctness, source grounding, visual necessity, or superiority over baselines. Those need independent human annotation/adjudication.

Show người dùng actual **input → output** for each selected case: concise evidence description, image-attached flag, motif, derivation, trace, question, four choices, selected answer, and a clear “chưa chấm người” label. Provide raw JSONL path and result checksum for audit.

## Editing/testing pitfall

Avoid hand-escaped JSON inside Python string literals or nested triple quotes. Build response/test JSON using `json.dumps`. If a patch cannot locate its anchor, do not force it: reread the exact region and make a small anchored patch.
