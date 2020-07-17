import numpy as np
from pyscf import gto, scf, lib
lib.num_threads(1)

geometry = '''
      O       0.0000000000     0.0000000000     0.1084050200
      H      -0.7539036400     0.0000000000    -0.4794322700
      H       0.7539036400     0.0000000000    -0.4794322700
'''
mol = gto.Mole()
mol.atom = geometry
mol.basis = '3-21g'
mol.build()

mf = scf.RHF(mol)
mf.scf()

Fao = mf.get_fock()
Fmo = mf.mo_coeff.T @ Fao @ mf.mo_coeff

np.set_printoptions(formatter={'float': lambda Fmo: "{0:0.6f}".format(Fmo)})
print('F_mo')
print(Fmo)
print()
