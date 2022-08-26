import os.path
import sys
from jinja2 import Environment, FileSystemLoader
import argparse
from core import log
from core.helper import check_dir


def parse_arguments():
    parser = argparse.ArgumentParser(prog='Generate DyqPipe Report',
                                     description='')
    parser.add_argument('-v', '--version', action='version', version='0.1')
    parser.add_argument('-o', '--out-dir', default="", help='The output report path')
    log.info(sys.argv)
    return parser.parse_args()


def generate_report(out_dir):
    env = Environment(loader=FileSystemLoader(searchpath='./res'))
    template = env.get_template('report.html')
    out_html = template.render()
    check_dir(out_dir)
    report_html = os.path.join(out_dir, 'report.html')
    with open(report_html, 'w') as of:
        of.write(out_html)


if __name__ == "__main__":
    args = parse_arguments()
    log.info('Generate Report...')
    generate_report(
        out_dir=args.out_dir
    )
