import sys

# find `RESTRICTED (RHF) MOLECULAR ORBITAL COEFFICIENTS` section.
with open('nh3.out', 'r+') as f:
    for n, line in enumerate(f):
        if 'RESTRICTED (RHF) MOLECULAR ORBITAL COEFFICIENTS' in line:
            start_section = n
        if '======= MOLECULAR ORBITALS IN MOLDEN FORMAT =======' in line:
            end_section = n - 3


# collect date.
text_list = []
with open('nh3.out', 'r+') as f:
    for n, line in enumerate(f):
        if (n >= start_section) and (n <= end_section):
            text_list.append(line)


# find the eigenvalues.
eigenvalues = []
with open('nh3.out', 'r+') as f:
    for n, line in enumerate(f):
        if (n >= start_section) and (n <= end_section):
            if 'eigenvalues' in line:
                eigenvalues.append(line.split()[1:])

flatten = [item for sublist in eigenvalues for item in sublist]
print('---Eigenvalues---')
print(flatten)
print()


# find the number of orbitals.
orbital_count = int((len(text_list) - 1) / len(eigenvalues)) - 2


# find eigenvectors.
def get_section(text_list, orbital_count):
    lines = []
    start = False
    for line in text_list:
        count = 0
        if 'eigenvalues' in line:
            start = True
            if lines:
                yield lines
                lines = []
        elif start:
            lines.append(line)
            if str(orbital_count) in line.split()[0]:
                start = False
    if lines:
        yield lines


def main(text_list, orbital_count):
    coeffs = []
    for sect in get_section(text_list=text_list,
                            orbital_count=orbital_count):
        rows = [
            [float(c) for c in line[20:].split()]
            for line in sect
        ]
        transposed = list(map(list, zip(*rows)))
        coeffs.extend(transposed)

    return coeffs

coeffs = main(text_list=text_list,
              orbital_count=orbital_count)

print('---Eigenvectors---')
for i in coeffs:
        print(i)
