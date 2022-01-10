import sys
import wave
import winsound as ws
import time
import readchar
import threading

class BeepSound:
    file = "c:\\windows\\media\\ring01.wav"
    mode = ws.SND_FILENAME | ws.SND_LOOP | ws.SND_ASYNC
    mode_stop = ws.SND_PURGE
    def until_keyhit(self):
        ws.PlaySound(self.file, self.mode)
        print()
        print("press any key ...")
        print()
        readchar.readkey()
        ws.PlaySound(None, self.mode_stop)

class CookingTimer:
    def __init__(self):
        self.sec = 180 
        self.event = threading.Event()
        self.thread = threading.Thread(target=self.print_time)

    def start(self, sec, stop=True):
        self.sec = sec
        self.thread.start()
        try:
            time.sleep(self.sec)
        except:
            self.event.set()
            return False
        if (stop):
            self.event.set()
        return True

    def stop(self):
        self.event.set()
        return True

    def print_time(self):
        count = 0
        while not self.event.wait(timeout=1):
            count += 1
            print(time.ctime(), ": {0} sec / T {1} sec".format(count, count - self.sec))
        self.event.clear()

if __name__ == "__main__":
    beep = BeepSound()
    cooking_timer = CookingTimer()

    if len(sys.argv) == 1:
        print("")
        print(" *** Cooking Timer ***")
        print("")
        print("   request sec(default 180sec) : ", end="")
        a = input()
        if a == "":
            sec = 180
        else:
            sec = int(a)
    else:
        sec = int(sys.argv[1])

    if cooking_timer.start(sec, False):
        beep.until_keyhit()
    cooking_timer.stop()

