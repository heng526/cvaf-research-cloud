"""CVAF R3: deterministic, dependency-free complex-representation contracts.

Scope: algebraic CPU preflight, not a PolSAR dataset test, model evaluation,
training run, physical augmentation policy, or evidence of task performance.

Source audit:
  HIT-WXM/CAct-PolSAR/train/polsar_dataset.py @ 076a43e41a725b6289ab8b0eef8e4530a37a5ef2
  HIT-WXM/CAct-PolSAR/reports/higher_order_complex_kan/01_DATA_STRUCTURE_AUDIT.md
  on research/higher-order-complex-kan @ 6e9afcf7825e05f479ec821d80680623eddf5653
"""

import cmath
import math
import unittest


def coherency_from_vector(k):
    """Rank-one 3x3 Hermitian positive-semidefinite T = k k^H."""
    return [[ki * kj.conjugate() for kj in k] for ki in k]


def frobenius_norm(m):
    return math.sqrt(sum(abs(x) ** 2 for row in m for x in row))


def hermitian_residual(m):
    return frobenius_norm(
        [[m[i][j] - m[j][i].conjugate() for j in range(3)] for i in range(3)]
    )


def matrix_difference(a, b):
    return [[a[i][j] - b[i][j] for j in range(3)] for i in range(3)]


def quadratic_form(m, v):
    return sum(
        v[i].conjugate() * m[i][j] * v[j]
        for i in range(3)
        for j in range(3)
    )


def split_silu(z):
    def silu(x):
        return x / (1.0 + math.exp(-x))
    return complex(silu(z.real), silu(z.imag))


def radial_gate(z):
    """A real-valued radial gain: f(z) = z/(1+|z|)."""
    return z / (1.0 + abs(z))


class RepresentationContractTests(unittest.TestCase):
    def setUp(self):
        self.k = (1.0 + 2.0j, 0.3 - 0.5j, -1.0 + 0.7j)
        self.t = coherency_from_vector(self.k)

    def test_raw_scattering_common_phase_is_coherency_invariant(self):
        """The raw k gauge action disappears after k k^H construction."""
        for theta in (0.0, 0.3, -1.2, math.pi):
            rot = cmath.exp(1j * theta)
            transformed = coherency_from_vector(tuple(rot * z for z in self.k))
            self.assertLess(frobenius_norm(matrix_difference(transformed, self.t)), 1e-12)

    def test_naive_global_phase_rotation_of_T_breaks_hermiticity(self):
        """e^(i theta) T is not the induced physical gauge action on T."""
        rotated = [[cmath.exp(0.4j) * x for x in row] for row in self.t]
        self.assertGreater(hermitian_residual(rotated), 1.0)

    def test_diagonal_unitary_congruence_preserves_Hermitian_PSD(self):
        """An algebraic T->D T D^H transformation preserves the PSD cone.

        This test does not establish that arbitrary D is a physically valid
        sensor augmentation or that a classification label is D-invariant.
        """
        d = [cmath.exp(1j * t) for t in (0.0, 0.2, -0.8)]
        t_new = [[d[i] * self.t[i][j] * d[j].conjugate() for j in range(3)] for i in range(3)]
        self.assertLess(hermitian_residual(t_new), 1e-12)
        for v in ((1+0j, 0j, 0j), (0j, 1+0j, 0j), (1+2j, -0.3+0.7j, 0.1-1j)):
            q = quadratic_form(t_new, v)
            self.assertLess(abs(q.imag), 1e-11)
            self.assertGreaterEqual(q.real, -1e-11)

    def test_radial_gate_equivariant_at_zero_and_nonzero(self):
        for z in (0j, 1+0j, 0.1-0.7j, 2.0+1.0j, 1e-9+1e-9j):
            for theta in (0.0, 0.2, math.pi/2, math.pi):
                rot = cmath.exp(1j * theta)
                self.assertLess(abs(radial_gate(rot*z) - rot*radial_gate(z)), 1e-12)

    def test_split_silu_is_not_globally_phase_equivariant(self):
        z = 1.0+0j
        rot = -1.0+0j
        defect = abs(split_silu(rot*z) - rot*split_silu(z))
        self.assertGreater(defect, 0.46)

    def test_strict_complex_linear_is_equivariant_widely_linear_is_not(self):
        """With no bias, a*z commutes with scalar rotation; a*z+b*conj(z) does not."""
        z, a, b = 0.5+1j, 0.8+0.4j, 0.3-0.2j
        rot = cmath.exp(0.73j)
        strict = lambda w: a*w
        wide = lambda w: a*w + b*w.conjugate()
        self.assertLess(abs(strict(rot*z) - rot*strict(z)), 1e-12)
        self.assertGreater(abs(wide(rot*z) - rot*wide(z)), 1e-3)

    def test_per_channel_zscore_need_not_preserve_psd(self):
        """A synthetic counterexample, NOT a test on the user's dataset.

        Two valid rank-one T matrices have T11=1 and T11=4. The first
        normalized T11 is negative, so the six-channel normalized object
        cannot be interpreted as a positive-semidefinite coherency matrix.
        """
        values = (1.0, 4.0)
        mu = sum(values)/2.0
        std = math.sqrt(sum((x-mu)**2 for x in values)/2.0)
        normalized_t11 = (values[0]-mu)/(std+1e-6)
        self.assertLess(normalized_t11, 0.0)
        self.assertLess(normalized_t11, -0.99)


if __name__ == '__main__':
    unittest.main()
