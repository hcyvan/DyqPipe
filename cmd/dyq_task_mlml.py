#!/usr/bin/env python

import sys
import argparse

from core import run_shell_cmd
from core import log


def parse_arguments():
    parser = argparse.ArgumentParser(prog='Find hydroxymethylation ratio and methylation ratio',
                                     description='')
    parser.add_argument('-v', '--version', action='version', version='0.1')
    parser.add_argument('-m', '--bs-seq', required=True, type=argparse.FileType('r'),
                        help='the BS-seq alignmented data')
    parser.add_argument('-x', '--oxbs-seq', required=True, type=argparse.FileType('r'),
                        help='the OxBS-seq alignmented data')
    parser.add_argument('-o', '--out-file', required=True, type=argparse.FileType('w'), help='The output file.')

    log.info(sys.argv)
    return parser.parse_args()


def mlml(bs_seq_file, oxbs_seq_file, out_file):
    run_shell_cmd(
        'mlml '
        '-v -u {bs_seq_file} -m {oxbs_seq_file} -o {out_file}'.format(
            bs_seq_file=bs_seq_file,
            oxbs_seq_file=oxbs_seq_file,
            out_file=out_file
        )
    )


if __name__ == "__main__":
    args = parse_arguments()
    log.info('Calling mlml...')
    mlml(
        args.bs_seq.name,
        args.oxbs_seq.name,
        args.out_file.name
    )

