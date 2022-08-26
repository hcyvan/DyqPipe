import sys
import os
import argparse

from core import log
from core import PIPELINE_VERSION
from cmd.dyq_task_mlml import mlml

parser = argparse.ArgumentParser(prog='This is DyqPipe', description='')
parser.add_argument('-v', '--version', action='version', version=PIPELINE_VERSION)
parser.add_argument('-m', '--bs-seq', required=True, help='the BS-seq alignmented data')
parser.add_argument('-x', '--oxbs-seq', required=True, help='the OxBS-seq alignmented data')
parser.add_argument('-o', '--out-file', required=True, help='The output file.')

log.info(sys.argv)

args = parser.parse_args()
log.info('Calling mlml...')
mlml(args.bs_seq, args.oxbs_seq, args.out_file)






