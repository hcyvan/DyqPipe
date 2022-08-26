import sys
import argparse
import pandas as pd
from core import log
from core.plot import plot_cor_heatmap


def parse_arguments():
    parser = argparse.ArgumentParser(prog='Script for draw',
                                     description='')
    parser.add_argument('-v', '--version', action='version', version='0.1')
    subparsers = parser.add_subparsers(help='sub-command help', dest='subparser_name')

    parser_dmr_dhmr_cor = subparsers.add_parser('dmr_dhmr_cor', help='cpg correlation plot')
    parser_dmr_dhmr_cor.add_argument('-g', '--group', default='',
                                     help='The samples in control group. separate by ","')
    parser_dmr_dhmr_cor.add_argument('-a', '--in-file-a', required=True, help='The input dmr bed file')
    parser_dmr_dhmr_cor.add_argument('-b', '--in-file-b', required=True, help='The input dhmr bed file')
    parser_dmr_dhmr_cor.add_argument('-o', '--out-file', required=True, help='The output file')

    log.info(sys.argv)
    return parser.parse_args()


def plot_dmr_dhmr_cor(group, in_file_a, in_file_b, out_file):
    matrix_5mc = pd.read_csv(in_file_a, sep='\t')
    matrix_5hmc = pd.read_csv(in_file_b, sep='\t')
    m5mc = matrix_5mc.iloc[:, 4:]
    m5hmc = matrix_5hmc.iloc[:, 4:]
    a = (m5mc == -1).sum(1) == 0
    b = (m5hmc == -1).sum(1) == 0
    if len(group) > 0:
        group = group.split(',')
        mc = m5mc[a * b][group].mean(1)
        hmc = m5hmc[a * b][group].mean(1)
    else:
        mc = m5mc[a * b].mean(1)
        hmc = m5hmc[a * b].mean(1)
    plot_cor_heatmap(mc.to_numpy(),
                     hmc.to_numpy(),
                     output=out_file,
                     xlabel='DMR Ratio Rank',
                     ylabel='DHMR Ratio Rank')


if __name__ == "__main__":
    args = parse_arguments()
    if args.subparser_name == 'dmr_dhmr_cor':
        plot_dmr_dhmr_cor(
            group=args.group,
            in_file_a=args.in_file_a,
            in_file_b=args.in_file_b,
            out_file=args.out_file
        )
    elif args.subparser_name == 'dmr':
        pass
