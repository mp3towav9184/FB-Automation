import codehooks as chks
import traceback
from time import sleep, time


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




