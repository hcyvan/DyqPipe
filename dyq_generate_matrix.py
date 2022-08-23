import os.path
import sys
import argparse
import time
import gzip
from core import log
from core.helper import isfloat


def parse_arguments():
    parser = argparse.ArgumentParser(prog='Extract data from bed files and generate matrix',
                                     description='')
    parser.add_argument('-v', '--version', action='version', version='0.1')
    parser.add_argument('-n', '--column', default=3, type=int, help='the bed column (0 start) to be extract. '
                                                                    '3 for 5mc and 4 for 5hmc')
    parser.add_argument('-c', '--coordinate', required=True, help='The coordinate bed file')
    parser.add_argument('-i', '--in-file', required=True, help='The input bed list to merge. separate by ","')
    parser.add_argument('-o', '--out-file', default="", help='The output matrix')
    parser.add_argument('-e', '--exclude', default='close',
                        help='exclude -1 mode: '
                             'all - exclude if all sample is -1;'
                             'one - exclude if contain one -1;'
                             'close - close exclude mode'
                        )
    log.info(sys.argv)
    return parser.parse_args()


def extract_matrix(in_file, out_file, coordinate, column=3, exclude='close'):
    files = in_file.split(',')
    samples = [os.path.splitext(os.path.basename(f))[0] for f in files]
    headers = ['chrom', 'start', 'end']
    headers.extend(samples)

    if len(out_file) == 0:
        of = sys.stdout
    else:
        of = open(out_file, 'w')
    of.write('\t'.join(headers) + '\n')

    ifs = []
    for f in files:
        ifs.append(open(f, 'r'))
    top = []
    for i, f in enumerate(ifs):
        line = f.readline()
        if line.startswith("#") or line.startswith("chrom"):
            line = f.readline()
        top.append(line.split('\t'))

    start = time.perf_counter()
    idx = 0
    for line in gzip.open(coordinate, 'r'):
        if idx % 1000000 == 0:
            log.info("index {}, pass {} min".format(idx, round((time.perf_counter() - start) / 60), 4))
        idx += 1
        line = line.decode()
        prefix = line.strip()
        row = prefix.split("\t")
        value = []
        minus1 = 0
        for i, t in enumerate(top):
            if t is None:
                value.append('-1')
                minus1 += 1
            else:
                if row[0] == t[0] and int(row[1]) == int(t[1]):
                    if isfloat(t[column]):
                        value.append(t[column])
                    else:
                        value.append('-1')
                    line = ifs[i].readline()
                    if line:
                        top[i] = line.split('\t')
                    else:
                        top[i] = None
                else:
                    value.append('-1')
                    minus1 += 1
        if (exclude == 'all' and minus1 == len(ifs)) or (exclude == 'one' and minus1 >= 1):
            pass
        else:
            of.write("{}\t{}\n".format(prefix, '\t'.join(value)))
    end = time.perf_counter()
    log.info("use {} min !!".format((end - start) / 60))


if __name__ == "__main__":
    args = parse_arguments()
    log.info('Generate matrix...')
    extract_matrix(
        in_file=args.in_file,
        out_file=args.out_file,
        coordinate=args.coordinate,
        column=args.column,
        exclude=args.exclude
    )
