#!/usr/bin/env python

import sys
import argparse

from R import run_r
from core import log


def parse_arguments():
    parser = argparse.ArgumentParser(prog='Do enrichment analysis',
                                     description='')
    parser.add_argument('-v', '--version', action='version', version='0.1')
    parser.add_argument('-g', '--genome', default="hg38", help='The genome version')
    parser.add_argument('-i', '--in-file', required=True, help='bed file')
    parser.add_argument('-o', '--out-dir', default="./", help='The default output directory')

    log.info(sys.argv)
    return parser.parse_args()


def enrichment(in_file, out_dir, genome):
    run_r(
        f"regionEnrichment.R -i {in_file} -g {genome} -o {out_dir}"
    )


if __name__ == "__main__":
    args = parse_arguments()
    log.info('Calling mlml...')
    enrichment(
        in_file=args.in_file,
        genome=args.genome,
        out_dir=args.out_dir
    )
