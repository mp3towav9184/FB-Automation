import codehooks as chks
import traceback, os, subprocess
from time import sleep, time

HOST = os.getenv('RDP_HOST')
USER = os.getenv('RDP_USER')
PASS = os.getenv('RDP_PASS')

def needtoRun():
    try:
        r = chks.getSingleObjectFromCollection('fb-automation', '6900629fb029f9be5510e815')
        assert r.get('lastRun')
        sec = time() - r.get('lastRun')
        mints = sec / 60
        if mints >= 15:
            return True
        else:
            print(f'No need to run since it ran {int(mints)} minutes ago', flush=True)
            return False
    except:
        traceback.print_exc()
        print('Retrying needToRun after a delay...', flush=True)
        sleep(5)
        return needtoRun()


def connectRDP():
    cmd = ["xfreerdp", f"/v:{HOST}", f"/u:{USER}", f"/p:{PASS}", "/size:1920x1080", "/smart-sizing", "/cert:ignore"]
    try:
        proc = subprocess.Popen(["xvfb-run", "-a"] + cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            out, err = proc.communicate(timeout=80)
            print("Process Finished Early!", flush=True)
        except subprocess.TimeoutExpired:
            print("Terminating Process...", flush=True)
            proc.kill()
            out, err = proc.communicate()

        if out: print('='*20, 'OUTPUT', '='*20, f'\n{out}')
        if err: print('='*20, 'ERROR', '='*20, f'\n{err}')
    except:
        traceback.print_exc()
        print('Could not run connectRDP function', flush=True)


def main():
    if needtoRun():
        print('Running connectRDP function...\n', flush=True)
        connectRDP()

if __name__ == '__main__':
    main()
