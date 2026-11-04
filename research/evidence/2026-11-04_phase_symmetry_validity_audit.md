# CVAF R3 — PolSAR phase-symmetry validity audit (2026-11-04)

Status: **SOURCE-VERIFIED CODE AUDIT / NO TRAINING**. This is an independent one-unit deliverable, not proof that the earlier Dot-reported 17-paper matrix has been saved.

## Source provenance

- `HIT-WXM/CAct-PolSAR`, default branch commit `076a43e41a725b6289ab8b0eef8e4530a37a5ef2`, file `train/polsar_dataset.py`: https://github.com/HIT-WXM/CAct-PolSAR/blob/076a43e41a725b6289ab8b0eef8e4530a37a5ef2/train/polsar_dataset.py
- `HIT-WXM/researchops-orchestrator`, commit `ccae9c4017cb0b908b5060e7d9c89ad9e59731c9`, `README.md`, `AGENTS.md`, `docs/ARCHITECTURE.md`, `schemas/record.schema.json`: https://github.com/HIT-WXM/researchops-orchestrator
- Existing project branches were enumerated, including `feat/ss2d-scan-accel`, `feat/paper-protocol-replica`, `research/higher-order-complex-kan`. **This audit reads the default-branch loader only; it does not assert other branches have the same behavior.**

## Concrete source finding

The dataset loader defines `ComplexPolSARAugment` with a common complex rotation `(x_r+i x_i) -> exp(i phi)(x_r+i x_i)`. In `load_train_test_from_dir`, however, it deliberately instantiates this augmentor with `phase_rotate_prob=0.0` and documents the reason: the six coherency/covariance elements `T11,T12,T13,T22,T23,T33` carry physically meaningful inter-channel phase relations. Thus **the code already disables naïve phase augmentation by default**; this is not a newly discovered missing fix.

## Mathematical implication — independent derivation, not an experiment

Let `k` be a complex scattering vector and `T=k k^H` its Hermitian coherency matrix. A common scattering-vector phase `k' = exp(i theta) k` satisfies

`T' = k' k'^H = exp(i theta) k k^H exp(-i theta) = T`.

This is **invariance of the coherency representation under the gauge action on the raw vector**. It does *not* imply that applying `T -> exp(i theta) T` is physically valid: for generic `theta`, the transformed matrix is no longer Hermitian. Therefore a 'global phase-equivariant PolSAR model' claim must specify whether the group acts on raw scattering vectors, coherency matrices, or intermediate learned complex features. These are different hypotheses.

For a pointwise operator, equivariance `f(exp(i theta)z)=exp(i theta)f(z)` holds for radial `f(z)=g(|z|)z` (with `f(0)=0` and real scalar `g`). It does not hold generally for split-SiLU: taking `z=1`, `theta=pi`, `s(t)=t/(1+exp(-t))`, yields `s(-1)=-0.2689414214` versus `-s(1)=-0.7310585786`. This is an exact counterexample to **unconditional** phase equivariance, not evidence of inferior classification accuracy.

## Falsifiable research question

**R3-H1:** Is a representation-aware symmetry constraint useful only when the input representation retains the nuisance phase, rather than after the coherency transform already removes it?

Proposed future controls (specification only, not authorized training):
1. Define the physically admissible transformation group for each actual dataset representation.
2. Verify invariance/equivariance analytically and with synthetic tensors, including Hermitian and positive-semidefinite checks.
3. Compare constrained and unconstrained operators with matched capacity and compute on independent data after an L3 experiment authorization.
4. Falsify H1 if matched tests show no robust advantage or gains vanish under protocol controls.

## Execution and persistence boundaries

No training, dataset access, split change, formal benchmark, cloud job, or Codex environment binding was verified here. The earlier 17-paper matrix remains **UNVERIFIED** until an actual artifact and commit are located. This document is an evidence note, not a replacement for `STATE.json` or `LEDGER.*`. The ResearchOps protocol requires actor-owned immutable outboxes and a single reducer for derived state; no outbox record was written because current project-specific state and idempotency ownership were not established.

**Next ready unit:** Compare the actual active research-branch loader and feature definitions with this default-branch behavior; separately recover and deduplicate the Dot-reported 17-paper matrix before further literature ingestion.
