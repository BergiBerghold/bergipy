import time, os


def check_pid(pid):
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def wait_for_prev_measurement(prev_pid):
    print('Waiting until previous measurement is done...')

    while True:
        if check_pid(prev_pid):
            time.sleep(1)
        else:
            break

    print(f'PID {prev_pid} is done. Starting in 3s ...')