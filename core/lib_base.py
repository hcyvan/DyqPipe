import os
import sys
import subprocess
import logging
import time
import signal

logging.basicConfig(format='[%(asctime)s %(levelname)s] %(message)s', stream=sys.stdout)
log = logging.getLogger(__name__)


def run_shell_cmd(cmd):
    p = subprocess.Popen(
        ['/bin/bash', '-o', 'pipefail'],  # to catch error in pipe
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        preexec_fn=os.setsid)  # to make a new process with a new PGID
    pid = p.pid
    pgid = os.getpgid(pid)
    log.info('run_shell_cmd: PID={}, PGID={}, CMD={}'.format(pid, pgid, cmd))
    t0 = time.perf_counter()
    stdout, stderr = p.communicate(cmd)
    rc = p.returncode
    t1 = time.perf_counter()
    err_str = (
        'PID={pid}, PGID={pgid}, RC={rc}, DURATION_SEC={dur:.1f}\n'
        'STDERR={stde}\nSTDOUT={stdo}'
    ).format(
        pid=pid, pgid=pgid, rc=rc, dur=t1 - t0, stde=stderr.strip(), stdo=stdout.strip()
    )
    if rc:
        try:
            os.killpg(pgid, signal.SIGKILL)
        except:
            pass
        finally:
            raise Exception(err_str)
    else:
        log.info(err_str)
    return stdout.strip('\n'), stderr.strip('\n')


def add_suffix(filename, suffix, directory=None):
    s = os.path.splitext(filename)
    new_name = '{}.{}{}'.format(s[0], suffix, s[1])
    if directory:
        file_name = os.path.basename(new_name)
        new_name = os.path.join(directory, file_name)
    return new_name
