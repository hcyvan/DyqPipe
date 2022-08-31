#!/usr/bin/env python

import sys
import argparse
from core import log


def parse_arguments():
    parser = argparse.ArgumentParser(prog='Merge DMC to DMR',
                                     description='')
    parser.add_argument('-v', '--version', action='version', version='0.1')
    parser.add_argument('-m', '--minimum', default=3, type=int, help='minimum dmc in the dmr')
    parser.add_argument('-d', '--dist', default=100, type=int, help='maximum distance between two dmc')
    parser.add_argument('-i', '--in-file', required=True, help='DMC bed file. "chrom, start, end, class" is necessary')
    parser.add_argument('-o', '--out-file', default="", help='DMR bed file. header: '
                                                             '"chrom, start, end, class, dmc_number, length"')
    log.info(sys.argv)
    return parser.parse_args()


def dmc2dmr(in_file, out_file, minimum, dist):
    dmr_chrom = None
    dmr_start = None
    dmr_end = None
    dmr_class = None
    dmr_cpg_num = 0

    if len(out_file) == 0:
        of = sys.stdout
    else:
        of = open(out_file, 'w')
    of.write('chrom\tstart\tend\tclass\tcpg_num\tdmr_length\n')
    for line in open(in_file, 'r'):
        dmc = line.strip().split('\t')
        if dmr_cpg_num == 0:
            dmr_chrom = dmc[0]
            dmr_start = dmc[1]
            dmr_end = dmc[2]
            dmr_class = dmc[3]
            dmr_cpg_num = 1
        else:
            if dmr_chrom == dmc[0] and int(dmc[2]) - int(dmr_end) <= dist and dmr_class == dmc[3]:
                dmr_end = dmc[2]
                dmr_cpg_num += 1
            else:
                if dmr_cpg_num >= minimum:
                    of.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(dmr_chrom, dmr_start, dmr_end, dmr_class, dmr_cpg_num,
                                                               int(dmr_end) - int(dmr_start)))
                dmr_chrom = dmc[0]
                dmr_start = dmc[1]
                dmr_end = dmc[2]
                dmr_class = dmc[3]
                dmr_cpg_num = 1


if __name__ == "__main__":
    args = parse_arguments()
    log.info('Merge Dmc...')
    dmc2dmr(
        in_file=args.in_file,
        out_file=args.out_file,
        minimum=args.minimum,
        dist=args.dist
    )
