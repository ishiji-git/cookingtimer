import sys
import getopt
import pathlib
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

def convert_timestr_to_sec(timestr):
    import re
    val = 0
    sec = 0
    fields = re.split("([hms])", timestr.rstrip().lower())
    for field in fields:
        if field == "h":
            sec += val * 3600
            val = 0
        elif field == "m":
            sec += val * 60
            val = 0
        elif field == "s":
            sec += val
            val = 0
        elif field == "":
            break
        else:
            val = float(field)
    if val != 0:
        sec += val
    return int(sec)

if __name__ == "__main__":
    beep = BeepSound()
    cooking_timer = CookingTimer()

    _usage = """Usage: {} [time]

    time: timer time. default is 180s.

      FORMAT)
          s, S: seconds
          m, M: minites
          h, H: hours
      Example)
        180s  : 180 seconds. typical time for Nissin Cup Noodle to be ready.
        5m    : 5 minites. typical time for ToyoSuisan Akai Kitsune to be ready.
        1.5h  : 1 and a half hour. tonight menu is the curry.
        1h30m : 1 hour and 30 minites. simmering time for kintoki beans.

    """

    sec = 0
    if len(sys.argv) < 2:
        print("")
        print(" *** Cooking Timer ***")
        print("")
        print(_usage.format(sys.argv[0]))
        print("")
        print("   request sec(default 180sec) : ", end="")
        a = input()
        if a == "":
            sec = 180
        else:
            timestr = a
    else:
        timestr = sys.argv[1]
    if sec == 0:
        sec = convert_timestr_to_sec(timestr)

    if sec <= 60:
        print(f"\ntimer start: {sec}s\n")
    elif sec > 60:
        print(f"\ntimer start: {sec}s/{int(sec/60)}m{sec-int(sec/60)*60}s")

    if cooking_timer.start(sec, False):
        beep.until_keyhit()
    cooking_timer.stop()

