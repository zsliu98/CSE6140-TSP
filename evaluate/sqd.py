import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from evaluate import _check_run
from .parameters import ls_timeout, ls_seed_list, instances

plt.rcParams["font.family"] = "Linux Libertine O"


def sqd_out(in_dir: str, out_dir: str, alg: list, run: bool):
    solutions = pd.read_csv(in_dir + 'solutions.csv')
    for _alg in alg:
        for instance in instances:
            solution = solutions.loc[solutions['Instance'] == instance, 'Value'].values[0]
            for seed in ls_seed_list:
                _check_run(in_dir=in_dir, out_dir=out_dir, alg_name=_alg.upper(), timeout=ls_timeout, run=run,
                           seed=seed, instances=[instance])

            e_max = 0.0
            t_max = 0.0
            for seed in ls_seed_list:
                file = '{}_{}_{}_{}.trace'.format(out_dir + instance, _alg.upper(), ls_timeout, seed)
                time_qual = pd.read_csv(file, names=['_time', '_qual'])
                time_qual = time_qual.assign(rel_qual=(time_qual['_qual'] - solution) / solution)
                e_max = max(e_max, time_qual['rel_qual'].max())
                t_max = max(t_max, time_qual['_time'].max())
            t_list = [t_max / 16, t_max / 8, t_max / 4, t_max / 2, t_max]

            fig, ax = plt.subplots(nrows=1, ncols=1, dpi=150)
            ax.set_xlabel("Relative error", fontweight="bold")
            ax.set_ylabel("Percent", fontweight="bold")
            for t in t_list:
                qual_list = []
                for seed in ls_seed_list:
                    file = '{}_{}_{}_{}.trace'.format(out_dir + instance, _alg.upper(), ls_timeout, seed)
                    time_qual = pd.read_csv(file, names=['_time', '_qual'])
                    time_qual = time_qual.assign(rel_qual=(time_qual['_qual'] - solution) / solution)
                    time_qual = time_qual[time_qual['_time'] <= t]
                    if time_qual.shape[0] != 0:
                        qual_list.append(np.min(time_qual['rel_qual']))
                if len(qual_list) != 0:
                    qual_list.sort()
                    ax.step([0] + qual_list + [e_max],
                            list(np.arange(0, len(qual_list) + 1) / len(ls_seed_list)) + [
                                len(qual_list) / len(ls_seed_list)],
                            label=u't={:0.2f}s'.format(t), where='post')
            ax.legend(loc='best')
            fig_file = out_dir + 'eva/' + _alg + instance.lower() + '_sqd.pdf'
            fig.savefig(fig_file)
            plt.close(fig)
