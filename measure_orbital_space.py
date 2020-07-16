from pyscf import gto

def main():
    geometry = '''
        H     0.0000    0.0000    0.0000
        H     0.0000    0.0000    0.7400
        '''
    basis = '3-21g'
    molecule = molecule_build(geometry, basis)

    complete_space = [a for a in range(molecule.nao)]
    print(molecule.basis)
    print(complete_space)


def molecule_build(geometry, basis):
    '''
    A simple molecule builder

    Parameters
    ----------
    geometry : :class:`str`
        The geometry of the molecule.
    basis : :class:`str`
        The basis set used.

    Returns
    -------
    molecule : :class:`pyscf.gto.mole.Mole`
        The molecule to simulate.

    '''
    molecule = gto.Mole()
    molecule.atom = geometry
    molecule.basis = basis
    molecule.verbose = -1
    molecule.build()

    return molecule


if __name__ == '__main__':
    main()
