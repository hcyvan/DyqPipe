#!/usr/bin/env python

from core import run_shell_cmd
from core.lib_base import add_suffix

tmp = './tmp'

beds = [
    'tmp_data/lung_cancer/lung_N1.bed',
    'tmp_data/lung_cancer/lung_N2.bed',
    'tmp_data/lung_cancer/lung_N3.bed',
    'tmp_data/lung_cancer/lung_T1.bed',
    'tmp_data/lung_cancer/lung_T2.bed',
    'tmp_data/lung_cancer/lung_T3.bed'
]

for bed in beds:
    out_bed = add_suffix(bed, 'sort', directory='tmp')
    run_shell_cmd(
        'cat {bed} |cut -f1-3 |sort -k1,1V -k2,2n > {bed_out}'.format(bed=bed, bed_out=out_bed)
    )
