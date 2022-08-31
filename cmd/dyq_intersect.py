#!/usr/bin/env python

import sys
import argparse

from core import run_shell_cmd
from core import log


def parse_arguments():
    parser = argparse.ArgumentParser(prog='intersect', description='')
    parser.add_argument('-v', '--version', action='version', version='0.1')
    parser.add_argument('-a', '--bed-a', required=True, type=argparse.FileType('r'),
                        help='the first file')
    parser.add_argument('-b', '--bed-b', required=True, type=argparse.FileType('r'),
                        help='the second file')
    parser.add_argument('-o', '--out-file', required=True, type=argparse.FileType('w'), help='The output file.')

    log.info(sys.argv)
    return parser.parse_args()


def intersect(bed_a, bed_b, out_file):
    run_shell_cmd(
        'bedtools intersect -a {bed_a} -b {bed_b} -wb| cut -f1-3 > {out_file} '.format(
            bed_a=bed_a,
            bed_b=bed_b,
            out_file=out_file
        )
    )


if __name__ == "__main__":
    args = parse_arguments()
    log.info('')
    intersect(
        args.bed_a.name,
        args.bed_b.name,
        args.out_file.name
    )

