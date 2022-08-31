#!/usr/bin/env python

import shutil
import os.path
import sys
from jinja2 import Environment, PackageLoader
import argparse
from core import log
from core.helper import check_dir


def parse_arguments():
    parser = argparse.ArgumentParser(prog='Generate DyqPipe Report',
                                     description='')
    parser.add_argument('-v', '--version', action='version', version='0.1')
    parser.add_argument('-o', '--out-dir', default="", help='The output report path')
    parser.add_argument('--img-cor-5mc-5hmc-control', type=argparse.FileType('r'))
    parser.add_argument('--img-cor-5mc-5hmc-test', type=argparse.FileType('r'))
    log.info(sys.argv)
    return parser.parse_args()


def generate_report(report_dir, img_dict):
    env = Environment(loader=PackageLoader(package_name='core', package_path='./res'))
    template = env.get_template('report.html')
    out_html = template.render(img=img_dict)
    report_html = os.path.join(report_dir, 'report.html')
    with open(report_html, 'w') as of:
        of.write(out_html)


if __name__ == "__main__":
    args = parse_arguments()
    log.info('Generate Report...')
    out_dir = args.out_dir

    out_image_dir = os.path.join(out_dir, "image")
    check_dir(out_dir)
    check_dir(out_image_dir)


    def cp_file(src):
        dst = os.path.join(out_image_dir, os.path.basename(src))
        dst_html = os.path.join("./image", os.path.basename(src))
        shutil.copy(src, dst)
        return dst_html


    images = dict()
    for k, image_path in args.__dict__.items():
        if k.startswith("img_") and image_path is not None:
            images[k[4:]] = cp_file(image_path.name)
    print(images)
    generate_report(
        report_dir=out_dir,
        img_dict=images
    )
