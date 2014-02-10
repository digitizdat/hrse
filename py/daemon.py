"""Generic daemonizing code for a Python daemon

Martin McGreal - March 23, 2006

"""

import os
import sys
import resource

alive = 0

def become(close_stderr=True):
    """He mounted the storm, his terrible chariot, reins hitched to the side.
    Yoked four in hand the appalling team with sharp, poisoned teeth:
    the Killer, the Pitiless, Trampler, Haste.
    They knew arts of plunder, skills of murder.
        - The Enuma Elis
    """
    pid = os.fork()
    if pid != 0:
        sys.exit()

    # Become the new session leader, the group leader of a new process group,
    # and let no terminal control you.
    os.setsid()

    # Should you open a terminal in some later stage of life, you may yet be
    # controlled by that terminal, as you are a session leader. So I say unto
    # you: fork again! And though you will give up your rights as session
    # leader, you will never be controlled by a terminal again.
    pid = os.fork()
    if pid != 0:
        sys.exit()

    os.close(0)
    fd = os.open("/dev/null", os.O_RDWR)
    os.dup2(fd, 1);
    
    # We may want to keep this open for tracebacks
    if close_stderr:
        os.dup2(fd, 2);

    alive = 1

    (soft, hard) = resource.getrlimit(resource.RLIMIT_NOFILE)
    for fd in range(3, soft):
        try:
            os.close(fd)
        except OSError:  # fd wasn't open
            pass

    os.chdir('/')
    os.umask(0)

    return os.getpid()

