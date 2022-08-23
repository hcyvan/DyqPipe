import os.path
import sys
import argparse
import time
import gzip
from core import log
from core.helper import match
import numpy as np
import scipy


def parse_arguments():
    parser = argparse.ArgumentParser(prog='Extract dmc/dmr/dhmc/dhmr value form matrix',
                                     description='')
    parser.add_argument('-v', '--version', action='version', version='0.1')
    subparsers = parser.add_subparsers(help='sub-command help', dest='subparser_name')

    parser_dmc = subparsers.add_parser('dmc', help='Calculate for each CpG point')
    parser_dmc.add_argument('-m', '--matrix', required=True, help='The input matrix')
    parser_dmc.add_argument('-i', '--in-file', required=True, help='The dmc/dhmc bed file')
    parser_dmc.add_argument('-o', '--out-file', default="", help='The output file')

    parser_dmr = subparsers.add_parser('dmr', help='b help')
    parser_dmr.add_argument('-m', '--matrix', required=True, help='The input matrix')
    parser_dmr.add_argument('-i', '--in-file', required=True, help='The dmr/dhmr bed file')
    parser_dmr.add_argument('-o', '--out-file', default="", help='The output file')

    log.info(sys.argv)
    return parser.parse_args()


def dmc_extract(in_file, out_file, matrix):
    if len(out_file) == 0:
        of = sys.stdout
    else:
        of = open(out_file, 'w')
    ifm = open(matrix, 'r')
    header_m = ifm.readline().strip().split('\t')
    ifi = open(in_file, 'r')
    _ = ifi.readline().strip().split('\t')
    headers_new = ['chrom', 'start', 'end', 'class']
    headers_new.extend(header_m[3:])
    of.write('\t'.join(headers_new) + '\n')
    bed = ifi.readline().strip().split('\t')
    start = time.perf_counter()
    idx = 0
    for line in ifm:
        if idx % 100000 == 0:
            sys.stderr.write("index {}, pass {} min\n".format(idx, round((time.time() - start) / 60), 4))
            of.flush()
        idx += 1
        line = line.strip().split('\t')
        if line[0] == bed[0] and int(line[1]) == int(bed[1]):
            dmc_line = bed[0:4]
            dmc_line.extend(line[3:])
            of.write('\t'.join(dmc_line) + '\n')
            bed = ifi.readline().strip().split('\t')
        elif line[0] == bed[0] and int(line[1]) > int(bed[1]):
            bed = ifi.readline().strip().split('\t')

    end = time.perf_counter()
    log.info("use {} min !!".format((end - start) / 60))


def dmr_extract(in_file, out_file, matrix):
    if len(out_file) == 0:
        of = sys.stdout
    else:
        of = open(out_file, 'w')
    ifm = open(matrix, 'r')
    header_m = ifm.readline().strip().split('\t')
    ifi = open(in_file, 'r')
    _ = ifi.readline().strip().split('\t')
    headers_new = ['chrom', 'start', 'end', 'class']
    headers_new.extend(header_m[3:])
    of.write('\t'.join(headers_new) + '\n')
    bed = ifi.readline().strip().split('\t')
    ncol = len(header_m) - 3
    top = np.empty((0, ncol), np.float64)

    start = time.perf_counter()
    idx = 0
    for line in ifm:
        if idx % 100000 == 0:
            log.info("index {}, pass {} min\n".format(idx, round((time.time() - start) / 60), 4))
        idx += 1
        line = line.strip().split('\t')
        if line[0] != bed[0] or int(line[1]) < int(bed[1]) or int(line[1]) > int(bed[2]) - 1:
            if top.shape[0] > 0:
                mean_ratio = np.round(np.nanmean(top, axis=0), 3).astype('str')
                dmr_line = bed[0:4]
                dmr_line.extend(mean_ratio)
                of.write('\t'.join(dmr_line) + '\n')
                of.flush()
                top = np.empty((0, ncol), np.float64)
                bed = ifi.readline().strip().split('\t')
            else:
                if int(line[1]) > int(bed[2]) - 1:
                    bed = ifi.readline().strip().split('\t')
        else:
            ratios = np.array([line[3:]]).astype(np.float64)
            ratios[ratios == -1] = np.nan
            top = np.append(top, ratios, axis=0)

    end = time.time()
    log.info("use {} min !!\n".format((end - start) / 60))


if __name__ == "__main__":
    args = parse_arguments()
    if args.subparser_name == 'dmc':
        log.info('Calculate matrix...')
        dmc_extract(
            in_file=args.in_file,
            out_file=args.out_file,
            matrix=args.matrix
        )
    elif args.subparser_name == 'dmr':
        log.info('Calculate matrix...')
        dmr_extract(
            in_file=args.in_file,
            out_file=args.out_file,
            matrix=args.matrix
        )
