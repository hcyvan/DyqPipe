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
    parser = argparse.ArgumentParser(prog='Calculate DMC/DHMC form matrix',
                                     description='')
    parser.add_argument('-v', '--version', action='version', version='0.1')
    subparsers = parser.add_subparsers(help='sub-command help', dest='subparser_name')

    parser_find = subparsers.add_parser('find', help='Calculate for each CpG point')
    parser_find.add_argument('-c', '--control-group', required=True,
                             help='The samples in control group. separate by ","')
    parser_find.add_argument('-t', '--test-group', required=True, help='The samples in test group. separate by ","')
    parser_find.add_argument('-i', '--in-file', required=True, help='The input matrix')
    parser_find.add_argument('-o', '--out-file', default="", help='The output file')

    parser_filter = subparsers.add_parser('filter', help='b help')
    parser_filter.add_argument('-p', '--p-value', default=0.05, type=float, help='The p value')
    parser_filter.add_argument('-f', '--fold-change', default=1.2, type=float,
                               help='The least value of abs(FoldChange)')
    parser_filter.add_argument('-i', '--in-file', required=True, help='The output file of "find" step')
    parser_filter.add_argument('-o', '--out-file', default="", help='The output file')

    log.info(sys.argv)
    return parser.parse_args()


def dmc_finder(in_file, out_file, control_group, test_group):
    control_group = control_group.split(',')
    test_group = test_group.split(',')

    if len(out_file) == 0:
        of = sys.stdout
    else:
        of = open(out_file, 'w')
    of.write('chrom\tstart\tend\tpvalue\tlog2FC\tcontrol_group\ttest_group\n')
    ifm = open(in_file, 'r')
    in_header = ifm.readline()
    in_header = in_header.strip().split('\t')
    control_group_index = [x - 3 for x in match(control_group, in_header)]
    test_group_index = [x - 3 for x in match(test_group, in_header)]
    start = time.perf_counter()
    idx = 0
    for line in ifm:
        if idx % 1000000 == 0:
            log.info("index {}, pass {} min".format(idx, round((time.perf_counter() - start) / 60), 4))
        idx += 1
        cells = line.strip().split('\t')
        arr = np.array(cells[3:], np.float64)
        if np.sum(arr == -1) > 0:
            continue
        if np.sum(arr == 0) == arr.size:
            continue
        control_group = arr[control_group_index]
        test_group = arr[test_group_index]
        test = scipy.stats.f_oneway(control_group, test_group)
        p_value = test.pvalue
        fc = np.log2(test_group.mean() / control_group.mean())
        out = '{bed}\t{p}\t{fc}\t{cgroup}\t{tgroup}\n'.format(
            bed='\t'.join(cells[0:3]),
            p=round(p_value, 4),
            fc=round(fc, 4),
            cgroup=round(control_group.mean(), 3),
            tgroup=round(test_group.mean(), 3))
        of.write(out)
    end = time.perf_counter()
    log.info("use {} min !!".format((end - start) / 60))


def dmc_filter(in_file, out_file, p_value, fold_change):
    if len(out_file) == 0:
        of = sys.stdout
    else:
        of = open(out_file, 'w')
    of.write('chrom\tstart\tend\tclass\tpvalue\tlog2FC\n')
    ifm = open(in_file, 'r')
    _ = ifm.readline()
    start = time.perf_counter()
    idx = 0
    for line in ifm:
        if idx % 1000000 == 0:
            log.info("index {}, pass {} min".format(idx, round((time.perf_counter() - start) / 60), 4))
        idx += 1
        cells = line.strip().split('\t')
        arr = np.array(cells[3:], np.float64)
        log2_fc = np.log2(fold_change)
        if arr[0] <= p_value and np.abs(arr[1]) >= log2_fc:
            if arr[1] > 0:
                d_class = 'hyper'
            else:
                d_class = 'hypo'
            of.write('{}\t{}\t{}\n'.format('\t'.join(cells[0:3]), d_class, '\t'.join(cells[3:5])))
    end = time.perf_counter()
    log.info("use {} min !!".format((end - start) / 60))


if __name__ == "__main__":
    args = parse_arguments()
    if args.subparser_name == 'find':
        log.info('Calculate matrix...')
        dmc_finder(
            in_file=args.in_file,
            out_file=args.out_file,
            control_group=args.control_group,
            test_group=args.test_group
        )
    elif args.subparser_name == 'filter':
        log.info('Calculate matrix...')
        dmc_filter(
            in_file=args.in_file,
            out_file=args.out_file,
            p_value=args.p_value,
            fold_change=args.fold_change
        )
