#!/usr/bin/env python

import sys
import argparse
import json
import numpy as np
import pandas as pd

from core import log
from core.helper import match


def parse_arguments():
    parser = argparse.ArgumentParser(prog='intersect', description='')
    parser.add_argument('-v', '--version', action='version', version='0.1')
    parser.add_argument('-c', '--control-group', required=True, help='The samples in control group. separate by ","')
    parser.add_argument('-t', '--test-group', required=True, help='The samples in test group. separate by ","')
    parser.add_argument('-o', '--out-file', required=True, type=argparse.FileType('w'), help='The output file.')
    parser.add_argument('--matrix-5mc', type=argparse.FileType('r'), help='The input matrix')
    parser.add_argument('--matrix-5hmc', type=argparse.FileType('r'), help='The input matrix')
    parser.add_argument('--dmc', type=argparse.FileType('r'))
    parser.add_argument('--dhmc', type=argparse.FileType('r'))
    parser.add_argument('--dmr', type=argparse.FileType('r'))
    parser.add_argument('--dhmr', type=argparse.FileType('r'))
    log.info(sys.argv)
    return parser.parse_args()


def summary_global_methylation_ratio(in_file, control_group, test_group):
    control_group = control_group.split(',')
    test_group = test_group.split(',')
    ifm = open(in_file, 'r')
    in_header = ifm.readline()
    in_header = in_header.strip().split('\t')
    control_group_index = [x - 3 for x in match(control_group, in_header)]
    test_group_index = [x - 3 for x in match(test_group, in_header)]
    sum_control = 0
    sum_test = 0
    idx = 0
    for line in ifm:
        cells = line.strip().split('\t')
        arr = np.array(cells[3:], np.float64)
        if np.sum(arr == -1) > 0:
            continue

        control_group = arr[control_group_index]
        test_group = arr[test_group_index]
        sum_control += np.mean(control_group)
        sum_test += np.mean(test_group)
        idx += 1

    return sum_control / idx, sum_test / idx


def count_dm_number(dm_file):
    df = pd.read_csv(dm_file, sep='\t')
    return df.shape[0]


if __name__ == "__main__":
    args = parse_arguments()
    log.info('Summary')
    control_5mc, test_5mc = summary_global_methylation_ratio(
        in_file=args.matrix_5mc.name,
        control_group=args.control_group,
        test_group=args.test_group
    )
    control_5hmc, test_5hmc = summary_global_methylation_ratio(
        in_file=args.matrix_5hmc.name,
        control_group=args.control_group,
        test_group=args.test_group
    )

    total_dmc = count_dm_number(args.dmc.name)
    total_dhmc = count_dm_number(args.dhmc.name)
    total_dmr = count_dm_number(args.dmr.name)
    total_dhmr = count_dm_number(args.dhmr.name)

    summary = dict(
        ratio_control_5mc=control_5mc,
        ratio_test_5mc=test_5mc,
        ratio_control_5hmc=control_5hmc,
        ratio_test_5hmc=test_5hmc,
        total_dmc=total_dmc,
        total_dhmc=total_dhmc,
        total_dmr=total_dmr,
        total_dhmr=total_dhmr,
    )

    json.dump(summary, args.out_file, indent=4)
