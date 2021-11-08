import subprocess
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-inf', action='store', dest='inf')
    parser.add_argument('-alg', action='store', dest='alg', default='BnB', choices=['BnB', 'Approx', 'LS1', 'LS2'])
    parser.add_argument('-time', action='store', dest='time', default=10)
    parser.add_argument('-seed', action='store', dest='seed', default=0)

    args = parser.parse_args()

    try:
        subprocess.run(args=['python3', str(args.alg).lower() + '.py',
                             '-inf', str(args.inf),
                             '-time', str(args.time),
                             '-seed', str(args.seed)],
                       timeout=int(args.time))
    except subprocess.TimeoutExpired:
        pass
