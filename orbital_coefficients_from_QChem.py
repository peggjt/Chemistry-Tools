'''
The code finds the original input cooridnates and the
restricted Hartree-Fock (RHF) molecular orbtial coefficients.

The code is run as a command line program. See:
    $python Harvest.py <file>

where, the `file` is a Q-Chem output. 

Author: James T. Pegg
'''

import argparse
import sys
import numpy as np
from numpy import linalg as LA
from pyscf import gto, scf, ci


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name')
    args = parser.parse_args()

    file_name = str(args.file_name)

    coordinates = _find_corrodinates(file_name)
    basis = _find_basis(file_name)

    mol = gto.Mole()
    mol.atom = coordinates
    mol.basis = basis
    mol.verbose = -1
    mol.build()

    mean_field = scf.RHF(mol)
    mean_field.scf()

    start_section, end_section = _mo_section_limits(file_name)
    harvest = _harvest_data(file_name, start_section, end_section)
    eigenvalues, eigenrows = _find_eigenvalues(file_name, start_section, end_section)
    count_orbital = _number_of_orbitals(harvest, eigenrows)
    mo_coeffs = _mo_coeffs(harvest, count_orbital)

def _find_corrodinates(file_name):
    with open(file_name, 'r+') as f:
        coordinates_section = []
        inside = False
        for n, line in enumerate(f):
            if 'Standard Nuclear Orientation (Angstroms)' in line:
                inside = True
            elif 'Nuclear Repulsion Energy =' in line:
                inside = False
            elif inside:
                coordinates_section.append(line.split()[1:])

    input_end = int(len(coordinates_section) / 2)
    input_section = coordinates_section[1: input_end + 1]
    modified_section = input_section[1:-2]
    flatten_section = [item for sublist in modified_section for item in sublist]
    line_section = [x for y in (flatten_section[i:i+4] + ['\n'] * (i < len(flatten_section) - 2) for
                    i in range(0, len(flatten_section), 4)) for x in y]
    input_coordinates = ' '.join(line_section)

    print('---Input Coordinates---')
    print(input_coordinates)

    return input_coordinates


def _find_basis(file_name):
    with open(file_name, 'r+') as f:
        for line in f:
            if ('basis' in line) and ('aux_basis' not in line):
                if 'basis' in line.split()[0]:
                    basis = str(line.split()[1])
    return basis


def _mo_section_limits(file_name):
    '''
    Finds `RESTRICTED (RHF) MOLECULAR ORBITAL COEFFICIENTS` section.
    '''
    with open(file_name, 'r+') as f:
        for n, line in enumerate(f):
            if 'RESTRICTED (RHF) MOLECULAR ORBITAL COEFFICIENTS' in line:
                start_section = n
            if '======= MOLECULAR ORBITALS IN MOLDEN FORMAT =======' in line:
                end_section = n - 3

    return start_section, end_section

def _harvest_data(file_name, start_section, end_section):
    ''' 
    Collect data.
    '''
    harvest = []
    with open(file_name, 'r+') as f:
        for n, line in enumerate(f):
            if (n >= start_section) and (n <= end_section):
                harvest.append(line)

    return harvest


def _find_eigenvalues(file_name, start_section, end_section):
    '''
    Find the eigenvalues.
    '''
    eigenlist = []
    with open(file_name, 'r+') as f:
        for n, line in enumerate(f):
            if (n >= start_section) and (n <= end_section):
                if 'eigenvalues:' in line:
                    eigenlist.append(line.split()[1:])

    eigenvalues = [item for sublist in eigenlist for item in sublist]
    eigenrows = len(eigenlist)
    print('---Eigenvalues---')
    print(eigenvalues)
    print()

    return eigenvalues, eigenrows


def _number_of_orbitals(harvest, eigenrows):
    '''
    Find the number of orbitals.
    '''
    count_orbital = int((len(harvest) - 2) / eigenrows)

    return count_orbital


def _mo_coeffs(harvest, count_orbital):
    coefficients = []
    for sect in _get_section(harvest=harvest,
                             count_orbital=count_orbital):
        rows = [
            [float(c) for c in line[20:].split()]
            for line in sect
        ]
        transposed = list(map(list, zip(*rows)))
        coefficients.extend(transposed)

    print('---Eigenvectors---')
    for i in coefficients:
        print(i)
    print()

    mo_coeffs = np.array(coefficients)
    return mo_coeffs


def _get_section(harvest, count_orbital):
    lines = []
    start = False
    for line in harvest:
        count = 0
        if 'eigenvalues' in line:
            start = True
            if lines:
                yield lines
                lines = []
        elif start:
            lines.append(line)
            if str(count_orbital - 1) in line.split()[0]:
                start = False
    if lines:
        yield lines


if __name__ == '__main__':
    main()
