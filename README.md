# CVAF Research Cloud — Literature-First Workspace

**Research program:** Mechanism-Guided Complex-Valued Deep Learning: Amplitude–Phase Coupling, Stable Operators, and Native Neural Architectures.

**Research goal:** Investigate general principles of complex-valued learning, with Nature Machine Intelligence / Nature Communications as aspirational targets and appropriate Q1 Top journals as alternatives. Publication and novelty are not presumed.

## Research directions

- **R1 — Complex Fundamental Operators:** complex activation, convolution, normalization, gating, attention, Complex KAN; amplitude–phase coupling and stable gradients.
- **R2 — Native Complex-Valued Architectures:** principled complex CNN, Transformer, SSM/Mamba, and KAN designs.
- **R3 — Mechanisms of Complex-Valued Learning:** controlled analysis of amplitude, relative phase, gradient, separability, structural interventions, robustness, and cross-task transfer.

## Current stage: literature-first (no formal training)

1. Inventory accessible, existing research assets and avoid repeating completed work.
2. Retrieve and verify primary papers (publisher/CVF/PMLR/OpenReview/arXiv) and their actual methods, equations, experiments, publication status, and code.
3. Build a deduplicated evidence matrix with source links and a closest-work/novelty map.
4. Identify open scientific questions and propose three falsifiable, mechanism-based hypotheses with negative controls and minimal tests.
5. Report source-backed progress, limitations, and the next ready task; do not count generic summaries as progress.

## Existing research assets (read-only until authorized)

- [CAct-PolSAR](https://github.com/HIT-WXM/CAct-PolSAR) — implementation, experimental branches, existing evidence.
- [researchops-orchestrator](https://github.com/HIT-WXM/researchops-orchestrator) — **authoritative** task/event/state protocol.

This workspace is a **literature research asset**, not a new independent research program or a replacement ResearchOps controller. Do not generate competing STATE/LEDGER files. Follow the existing outbox → single reducer → STATE/LEDGER contract only after reading and verifying its current schemas and permissions. If inaccessible, record BLOCKED_ACCESS rather than inventing state.

## Evidence and execution discipline

- Separate verified evidence, inference, and untested hypothesis. Do not fabricate references, numerical results, or paper access.
- Each claim needs a verifiable primary source; preserve DOI/arXiv, version/date, code link, task/data/metric, and relevant quotation or equation location.
- Do not use test data for design decisions. No formal GPU training, data split/label/evaluation changes, paid resource procurement, paper submission, or external communication without explicit approval.
- Keep private repositories and unpublished results private. Never commit credentials or full datasets.
- If an executor is unavailable, continue independently useful literature review; if a source is blocked, record its exact failure and proceed with available sources.
- Save durable artifacts to authorized versioned storage; a temporary cloud workspace path alone is not persistence.

## Initial acceptance criteria

A first cloud task must prove: (a) repository and primary-source access; (b) a real, nonempty evidence artifact with grounded citations; (c) a reproducible task identifier and commit; (d) an explicit next ready task. This README does not assert that any of those checks has already passed.
