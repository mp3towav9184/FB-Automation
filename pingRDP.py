import traceback, os, subprocess, sys, requests as rq
from time import sleep, time

HOST = os.getenv('RDP_HOST')
USER = os.getenv('RDP_USER')
PASS = os.getenv('RDP_PASS')
isErr = False

def needtoRun():
    global isErr
    try:
        r = rq.get('https://letscountapi.com/api/public/counters/8a1e77bc-187a-4e51-87a0-dcc28e5ed1fe', headers={'X-API-Key': '22eadebffed458047131479e91d49ff1bae9f6c397c9cb66c0b61f0879041142'})
        d = r.json()
        lr = d.get('value')
        assert lr
        sec = time() - lr
        mints = sec / 60
        if mints >= 15:
            return True
        else:
            print(f'No need to run since it ran {int(mints)} minutes ago', flush=True)
            return False
    except:
        traceback.print_exc()
        isErr = True
        print('Retrying needToRun after a delay...', flush=True)
        sleep(5)
        return needtoRun()


def connectRDP():
    global isErr
    cmd = ["xfreerdp", f"/v:{HOST}", f"/u:{USER}", f"/p:{PASS}", "/size:1920x1080", "/smart-sizing", "/cert:ignore"]
    try:
        proc = subprocess.Popen(["xvfb-run", "-a"] + cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            out, err = proc.communicate(timeout=80)
            print("Process Finished Early!", flush=True)
        except subprocess.TimeoutExpired:
            print("Terminating Process...", flush=True)
            proc.terminate()
            # proc.kill()
            out, err = proc.communicate()

        if out: print('='*20, 'OUTPUT', '='*20, f'\n{out}')
        if err:
            isErr = True
            print('='*20, 'ERROR', '='*20, f'\n{err}')
    except:
        isErr = True
        traceback.print_exc()
        print('Could not run connectRDP function', flush=True)


def main():
    if needtoRun():
        print('Running connectRDP function...\n', flush=True)
        connectRDP()
    
    if isErr: sys.exit(1)

if __name__ == '__main__':
    main()
