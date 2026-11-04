# CVAF Literature-First — Recovery, Branch Audit, and Representation-Symmetry Preflight

**Date:** 2026-11-04 (Asia/Taipei)  
**Scope:** L0 evidence verification and L1 deterministic CPU preflight only. No training, datasets, protocol change, new ResearchOps bus, or publication claim.

## 1. Previous 17-paper matrix: recovered and persistence verified

- **Persistent repository:** `heng526/activation-special-researchops` (private), commit `2b3cba58f9cbfafc9820b21ecc3ddda5aa2bb42b`; reducer follow-up `8e2fec8a04bf3dec7002a3df4bfe17a49458e60c`.
- **Batch directory:** `reports/activation-special/factory/review/literature_first_20261103_b01/`.
- **Core artifacts:** `papers.jsonl`, `overlap_matrix.csv`, `corpus_mapping_proposal.jsonl`, `r1.md`, `r2.md`, `r3.md`, `synthesis.md`, `candidate_questions.md`, `review_checks.md`.
- **Counts verified from stored records:** 17 `papers.jsonl` entries, 17 distinct `canonical_match_key` values, 17 corpus-mapping entries. This establishes within-batch uniqueness, **not** that all 17 are novel additions to the historical corpus.
- **Potential historical matches:** P03 *Better than Real: Complex-valued Neural Nets for MRI Fingerprinting* → OpenAlex `W2726753035`; P05 *The universal approximation theorem for complex-valued neural networks* → `W3111213259`, `W4311254982`, `W4311305958`. The other 15 have no title match in the recorded proposal; this is **not proof of absence**.
- **ResearchOps:** `researchops/state/STATE.json` `state_version=7`, `last_seq=21`; ledger sequence 20 = controller TASK and 21 = worker RESULT; task `P01-CVAF-LITERATURE-FIRST-20261103-B01`, result status PASS. Original 17-paper records have primary links, formulas and protocol descriptions, but their claims were not independently rechecked against every full paper during this follow-up.
- **Next corpus task:** Resolve the 2 title collisions using DOI/arXiv/venue metadata and re-query the remaining 15 by DOI/arXiv aliases before changing any historical registry. Do not overwrite existing corpus or count duplicate cards as new works.

## 2. Actual research-branch code comparison

| Branch / inspected code | Input and normalization | Phase treatment and additional behavior |
|---|---|---|
| `main` @ `076a43e41a725b6289ab8b0eef8e4530a37a5ef2` | `train/polsar_dataset.py` loads six complex channels; `ComplexStandardizer` fits real and imaginary channel means/stds **separately on train**; applies to train and val | `load_train_test_from_dir` explicitly constructs augmentation with `phase_rotate_prob=0.0`; horizontal/vertical flips enabled in train by default |
| `feat/paper-protocol-replica` @ `b1dd6cf29f8265c51bfe5dd70524e21732bc8a1d` | Loader adds `load_train_test_from_shared_split` with shared train IDs and optional external validation MAT, fits stats only on selected train subset | Both shared-index and default loaders explicitly set `phase_rotate_prob=0.0`; the training CLI can select the shared-index path |
| `feat/ss2d-scan-accel` @ `7de058fe4cf274ac3b6edc7c5cd6bd23c3df12c3` | `train/polsar_dataset.py` blob matches `main`; adds 13×13 center-context complex ConvNeXt/SS2D and model-factory entries | Existing augmentation unchanged; `complex_small_patch.py` supports strict complex or widely-linear-four-branch layers, default is the latter |
| `research/higher-order-complex-kan` @ `6e9afcf7825e05f479ec821d80680623eddf5653` | Loader blob matches `main`; `train/model_ext_hocaf.py` adds spectral HPD KAN and optional de-standardize/re-standardize using available train stats | Existing report states original MATLAB pre-standardization stats are missing, so de-standardizing the loader's *second* normalization cannot recover raw physical coherency |

**Source links:**
- Loader: https://github.com/HIT-WXM/CAct-PolSAR/blob/main/train/polsar_dataset.py
- Shared-index loader: https://github.com/HIT-WXM/CAct-PolSAR/blob/feat/paper-protocol-replica/train/polsar_dataset.py
- Small-patch backbone: https://github.com/HIT-WXM/CAct-PolSAR/blob/feat/ss2d-scan-accel/train/complex_small_patch.py
- HPD model: https://github.com/HIT-WXM/CAct-PolSAR/blob/research/higher-order-complex-kan/train/model_ext_hocaf.py
- Existing physical-data audit: https://github.com/HIT-WXM/CAct-PolSAR/blob/research/higher-order-complex-kan/reports/higher_order_complex_kan/01_DATA_STRUCTURE_AUDIT.md

**Critical existing evidence, not a new discovery:** `01_DATA_STRUCTURE_AUDIT.md` reports the six-channel MATLAB data were standardized before patch extraction, original mean/scale stats were not saved, and many normalized reconstructed matrices are non-positive-definite. Thus normalized channels are valid **learning features** but should not be treated as physically valid raw coherency matrices in a symmetry claim. This source is a project report; the underlying numerical statistics were not independently rerun in this follow-up.

## 3. Falsifiable hypothesis and minimum preflight

**R3-REP-H1 (representation-dependent symmetry).** The physically meaningful nuisance group depends on whether input is (a) raw scattering vector `k`, (b) raw coherency `T = k k^H`, (c) pre-standardized six-channel features, or (d) hidden complex activations. A model-level global complex-phase equivariance claim is not automatically a physically valid PolSAR claim.

**Null/alternative separation:**
- Mathematical identity: `k -> exp(i theta)k` leaves `T` unchanged; any additional raw-gauge invariance claim for `T` alone is redundant as a symmetry guarantee (not necessarily as a regularizer).
- Invalid substitution: `T -> exp(i theta)T` generally destroys Hermitian structure; do not use it as a physically valid augmentation.
- Algebraic contrast: `T -> D T D^H` preserves Hermitian PSD for unitary diagonal `D`, but arbitrary `D` is **not automatically** a valid physical sensor transform or label-preserving augmentation.
- Hidden-feature contrast: unbiased strict complex-linear `a z` and radial `g(|z|)z` are scalar-phase equivariant; general widely-linear `a z + b conj(z)` and split-SiLU are not. Equivariance of one layer does not prove whole-network equivariance.
- Falsifier for any *empirical* advantage: with the correct representation, matched real degrees of freedom, compute, initialization, and training protocol, a pre-registered validation effect is absent or disappears under the proper controls. No such training has been approved or performed.

**Executable L1 preflight:** `tests/test_phase_representation_contract.py` in `heng526/cvaf-research-cloud` (standard library only). Seven deterministic tests cover gauge invariance, invalid `T` rotation, algebraic unitary congruence, radial equivariance, split-SiLU counterexample, strict vs widely-linear equivariance, and a synthetic z-score PSD counterexample. Run:

```bash
python -m unittest discover -s tests -p 'test_phase_representation_contract.py' -v
```

**Acceptance:** all 7 tests pass with fixed double-precision arithmetic tolerance `1e-12` where applicable. A passing test verifies only the specified algebraic cases, not any neural-network performance or dataset physical validity. Local isolated Python preflight: **7 tests passed**. The published Codex cloud environment has **not** been observed running this file yet.

**Next L2-ready engineering task (no training):** on a known active code branch, use PyTorch `complex128` to compare exact operator outputs and gradients under a valid, precisely defined group action; test `ComplexLayerNorm2d`, strict complex conv, widely-linear conv, activation, and entire backbone separately. Record phase defect, relative residual, dtype, `eval()` mode, bias/affine parameters, and SHA. Do not assume 6-channel standardized inputs are physical `T`.

**Data/protocol gate:** An empirical claim about raw scattering-vector gauge invariance is **BLOCKED_DATA_PROVENANCE** until raw `k` or provenance-preserving physical `T`/normalization stats and a valid group action are established. Existing standardized patches do not authorize reinterpreting their channels as raw coherency. Any new data role/split/label/evaluation protocol is L4 and needs user approval. Formal multi-seed training is L3 and needs approval.

## 4. Orchestration handoff

- ResearchOps protocol source `HIT-WXM/researchops-orchestrator` v0.2.0: actor-owned immutable outboxes, one reducer, derived `STATE/LEDGER`; do not edit derived state directly.
- New work is stored as a non-derived evidence note and an L1 test in the authorized `cvaf-research-cloud` asset; it does not replace the existing private ResearchOps corpus or create a second controller.
- The current automation lookup returned the existing hourly `CVAF 文献研究与云端巡检` task with `is_enabled=false`, `environment_selection=inherited`, `environments=null`; therefore **hourly dispatch is currently paused** and explicit Codex cloud binding is **UNVERIFIED**. Do not claim 7×24 execution or create a duplicate task.
- Next research turn: verify the 2 historical corpus collisions, then audit phase equivariance of the *actual instantiated layers* under fixed, valid representation assumptions. Do not redo the recovered 17-paper search.
