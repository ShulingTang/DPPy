# coding: utf8
""" Unit tests:

- :class:`InclusionProbabilitiesProjectionDPP` to check that exact samplers for finite DPPs have the right (at least 1 and 2) inclusion probabilities
"""

import unittest

import numpy as np
import numpy.random as rndm

from scipy.linalg import qr
from scipy.stats import chisquare

from itertools import chain  # to flatten list of samples

import sys
sys.path.append('..')

from dppy.finite_dpps import FiniteDPP
from dppy.utils import det_ST


class InclusionProbabilitiesProjectionDPP(unittest.TestCase):
    """Check that exact samplers for finite DPPs have the right (at least 1 and 2) inclusion probabilities

    .. math::

        \\mathbb{P}[S\\subset \\mathcal{X}] = \\det K_S
    """

    rank, N = 6, 10
    nb_samples = 100

    def singleton_adequation(self, dpp, tol=0.05):
        """Perform chi-square test"""

        singletons = list(chain.from_iterable(dpp.list_of_samples))

        freq, _ = np.histogram(singletons, bins=range(self.N + 1), density=True)
        marg_theo = np.diag(dpp.K) / self.rank

        _, pval = chisquare(f_obs=freq, f_exp=marg_theo)

        return pval > tol

    def doubleton_adequation(self, dpp, tol=0.05):
        """Perform chi-square test"""

        samples = list(map(set, dpp.list_of_samples))

        nb_doubletons_to_check = 10
        doubletons = [set(rndm.choice(self.N,
                                      size=2,
                                      p=np.diag(dpp.K) / self.rank,
                                      replace=False))
                      for _ in range(nb_doubletons_to_check)]

        counts = [sum([doubl.issubset(sampl) for sampl in samples])
                  for doubl in doubletons]
        freq = np.array(counts) / self.nb_samples
        marg_theo = [det_ST(dpp.K, list(d)) for d in doubletons]

        _, pval = chisquare(f_obs=freq, f_exp=marg_theo)

        return pval > tol

    # From eigendecomposition
    def test_proj_dpp_sampler_from_eigdec_mode_Chol(self):
        """ Test whether 'Chol' sampling mode generates samples with the right 1 and 2 points inclusion probabilities when DPP defined by orthogonal projection correlation kernel K from its eigendecomposition.

        Complexity :math:`\\mathcal{O}(N rank^2)`

        .. seealso::

            - :cite:`Pou19` Algorithm 1
        """
        eig_vals = np.ones(self.rank)
        eig_vecs, _ = qr(rndm.randn(self.N, self.rank), mode="economic")
        dpp = FiniteDPP(kernel_type='correlation',
                        projection=True,
                        **{'K_eig_dec': (eig_vals, eig_vecs)})

        dpp.flush_samples()
        for _ in range(self.nb_samples):
            dpp.sample_exact(mode='Chol')

        dpp.compute_K()

        self.assertTrue(self.singleton_adequation(dpp))
        self.assertTrue(self.doubleton_adequation(dpp))


    def test_proj_dpp_sampler_from_eigdec_mode_GS(self):
        """ Test whether 'GS' sampling mode generates samples with the right 1 and 2 points inclusion probabilities when DPP defined by orthogonal projection correlation kernel K from its eigendecomposition

        Complexity :math:`\\mathcal{O}(N rank^2)`

        This is the default sampler when calling `.sample_exact()`
        """
        eig_vals = np.ones(self.rank)
        eig_vecs, _ = qr(rndm.randn(self.N, self.rank), mode="economic")
        dpp = FiniteDPP(kernel_type='correlation',
                        projection=True,
                        **{'K_eig_dec': (eig_vals, eig_vecs)})

        dpp.flush_samples()
        for _ in range(self.nb_samples):
            dpp.sample_exact(mode='GS')

        dpp.compute_K()

        self.assertTrue(self.singleton_adequation(dpp))
        self.assertTrue(self.doubleton_adequation(dpp))

    def test_proj_dpp_sampler_from_eigdec_mode_GS_bis(self):
        """ Test whether 'GS_bis' sampling mode generates samples with the right 1 and 2 points inclusion probabilities when DPP defined by orthogonal projection correlation kernel K from its eigendecomposition

        Complexity :math:`\\mathcal{O}(N rank^2)`

        Evaluate the conditionals using an alternative GS
        """
        eig_vals = np.ones(self.rank)
        eig_vecs, _ = qr(rndm.randn(self.N, self.rank), mode="economic")
        dpp = FiniteDPP(kernel_type='correlation',
                        projection=True,
                        **{'K_eig_dec': (eig_vals, eig_vecs)})

        dpp.flush_samples()
        for _ in range(self.nb_samples):
            dpp.sample_exact(mode='GS_bis')

        dpp.compute_K()

        self.assertTrue(self.singleton_adequation(dpp))
        self.assertTrue(self.doubleton_adequation(dpp))

    def test_proj_dpp_sampler_from_eigdec_mode_KuTa12(self):
        """ Test whether 'KuTa12' sampling mode generates samples with the right 1 and 2 points inclusion probabilities when DPP defined by orthogonal projection correlation kernel K from its eigendecomposition

        Complexity :math:`\\mathcal{O}(N rank^3)`
        """
        eig_vals = np.ones(self.rank)
        eig_vecs, _ = qr(rndm.randn(self.N, self.rank), mode="economic")
        dpp = FiniteDPP(kernel_type='correlation',
                        projection=True,
                        **{'K_eig_dec': (eig_vals, eig_vecs)})

        dpp.flush_samples()
        for _ in range(self.nb_samples):
            dpp.sample_exact(mode='KuTa12')

        dpp.compute_K()

        self.assertTrue(self.singleton_adequation(dpp))
        self.assertTrue(self.doubleton_adequation(dpp))

    def test_proj_dpp_sampler_from_eigdec_mode_Chol(self):
        """ Test whether 'Chol' sampling mode generates samples with the right 1 and 2 points inclusion probabilities when DPP defined by orthogonal projection correlation kernel K from its eigendecomposition.

        Complexity :math:`\\mathcal{O}(N rank^2)`

        .. seealso::

            - :cite:`Pou19` Algorithm 1
        """
        eig_vals = np.ones(self.rank)
        eig_vecs, _ = qr(rndm.randn(self.N, self.rank), mode="economic")
        dpp = FiniteDPP(kernel_type='correlation',
                        projection=True,
                        **{'K_eig_dec': (eig_vals, eig_vecs)})

        dpp.flush_samples()
        for _ in range(self.nb_samples):
            dpp.sample_exact(mode='Chol')

        dpp.compute_K()

        self.assertTrue(self.singleton_adequation(dpp))
        self.assertTrue(self.doubleton_adequation(dpp))

    # From kernel
    def test_proj_dpp_sampler_from_kernel_mode_GS(self):
        """ Test whether 'GS' sampling mode generates samples with the right 1 and 2 points inclusion probabilities when DPP defined by orthogonal projection correlation kernel K from its eigendecomposition

        Complexity :math:`\\mathcal{O}(N rank^2)`

        This is the default sampler when calling `.sample_exact()`
        """
        eig_vals = np.ones(self.rank)
        eig_vecs, _ = qr(rndm.randn(self.N, self.rank), mode="economic")
        dpp = FiniteDPP(kernel_type='correlation',
                        projection=True,
                        **{'K': (eig_vecs * eig_vals).dot(eig_vecs.T)})

        dpp.flush_samples()
        for _ in range(self.nb_samples):
            dpp.sample_exact(mode='GS')

        # dpp.compute_K()

        self.assertTrue(self.singleton_adequation(dpp))
        self.assertTrue(self.doubleton_adequation(dpp))

    def test_proj_dpp_sampler_from_kernel_mode_Schur(self):
        """ Test whether 'Schur' sampling mode generates samples with the right 1 and 2 points inclusion probabilities when DPP defined by orthogonal projection correlation kernel K from its eigendecomposition

        Evaluate the conditionals using the Schur complement updates
        """
        eig_vals = np.ones(self.rank)
        eig_vecs, _ = qr(rndm.randn(self.N, self.rank), mode="economic")
        dpp = FiniteDPP(kernel_type='correlation',
                        projection=True,
                        **{'K': (eig_vecs * eig_vals).dot(eig_vecs.T)})

        dpp.flush_samples()
        for _ in range(self.nb_samples):
            dpp.sample_exact(mode='Schur')

        self.assertTrue(self.singleton_adequation(dpp))
        self.assertTrue(self.doubleton_adequation(dpp))


def main():

    unittest.main()


if __name__ == '__main__':
    main()
