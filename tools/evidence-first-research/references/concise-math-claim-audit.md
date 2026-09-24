# Concise math/claim audit style for người dùng

Use this reference when người dùng asks for research-method brainstorming, manuscript review, or claim tightening with minimal prose.

## Output style

- Write as short as possible, but make mathematics explicit.
- Prefer stepwise blocks: symbols -> rule/gate -> proposition -> assumptions -> proof/test -> boundary.
- Avoid ornamental prose. Every important phrase in the paper should map to something checkable.

## Claim audit template

For each important claim, force this shape:

```text
Claim:
Mathematical object:
Test / evidence:
Boundary:
```

If any line is missing, weaken the claim.

## Verified/certified dataset claims

Use strong words only under explicit conditions.

A transparent gate can be written as:

```math
Accept(x)=\bigwedge_{k=1}^{K} \mathbf{1}[s_k(x)\succeq_k\theta_k]
```

where each criterion has its own threshold and pass direction. Do **not** accept by a composite score; composite/Pareto analysis belongs after the item has passed every required gate.

For unsupported-claim control, define:

```math
\varepsilon=\Pr(Y=1 \mid \text{judge admits},\text{no abstain})
```

Then, under independent calibration, no auto-accept on abstention, and transfer from calibration to release distribution:

```math
\mathbb{E}[UCR_{auto}]\le \varepsilon.
```

With expert audit fraction `beta` and expert miss probability `eta`:

```math
\mathbb{E}[UCR_{release}]\le (1-\beta)\varepsilon+\beta\eta.
```

Always state: calibration set, audit rate, CI, abstention handling, and distribution-shift boundary.

## Proxy vs bound discipline

Do not conflate an operational score with an information-theoretic bound.

For reverse reconstruction:

```math
S \rightarrow X \rightarrow \hat S,
I(S;\hat S)\le I(S;X)
```

ARA can be an interpretable gate proxy, e.g. semantic fidelity times lexical/key-concept recall. A variational quantity such as `I_NCE` is the MI lower-bound estimate. Write them separately.

## Hypothesis vs theorem

State empirical patterns as hypotheses unless proven:

```math
Acc(Remember) \ge Acc(Understand) \ge Acc(Apply) \ge Acc(Analyze)
```

and

```math
\Delta_b = Acc_{CoT}(b)-Acc_{Std}(b)
```

with monotonicity of `Delta_b` treated as a falsifiable hypothesis, not a law.
