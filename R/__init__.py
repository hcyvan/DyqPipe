import os
from core import run_shell_cmd


def run_r(r_cmd):
    path = __path__[0]
    script = os.path.join(path, r_cmd)
    cmd = "Rscript {script}".format(script=script)
    return run_shell_cmd(cmd)
