import argparse
import matplotlib.pyplot as plt


def graph(name, data):
    time = [i*10 for i in range(len(data))]
    fig, ax = plt.subplots()
    ax.step(time, data, color="Black", where='post')
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Disk Space (GB)", color="Black")

    name = name.split(".")[0]
    fig.savefig(f"{name}.png",
                format="png",
                dpi=100,
                bbox_inches="tight")

def main():
    # Parser.
    parser = argparse.ArgumentParser()
    parser.add_argument('name', type=str, nargs="?")
    args = parser.parse_args()
    print()

    if not args.name:
        args.name = input("Input File: ")
    name = str(args.name)
    print()

    data = []
    with open(name, "r") as f:
        for line in f:
            if "/dev/nvme0n1p1" in line:
                line = line.split()[2]
                value = int(line[:-1])
                data.append(value)
    graph(name, data)

if __name__ == '__main__':
    main()
