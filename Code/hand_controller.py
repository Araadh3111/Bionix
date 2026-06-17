# =====================================================================
#  Unbound Bionics - hand controller  (Raspberry Pi Pico / MicroPython)
#  Pin map taken directly from Peak.net schematic:
#     Thumb  servo -> GPIO10   Index servo -> GPIO11
#     Middle servo -> GPIO12   Ring  servo -> GPIO13
#     Pinky  servo -> GPIO14
#     EMG signal   -> GPIO26 (ADC0)
#  Servos powered from 5V (buck), signal lines from the Pico GPIO.
# =====================================================================

from machine import Pin, PWM, ADC
import time

# ---------- servo driver ----------
SERVO_FREQ = 50          # 50 Hz standard hobby servo
MIN_US = 500             # pulse width at 0 deg   (tune per servo)
MAX_US = 2500            # pulse width at 180 deg (tune per servo)

class Servo:
    def __init__(self, gpio, open_deg=0, closed_deg=110):
        self.pwm = PWM(Pin(gpio))
        self.pwm.freq(SERVO_FREQ)
        self.open_deg = open_deg        # finger straight / open
        self.closed_deg = closed_deg    # finger curled / closed
        self.write(open_deg)

    def write(self, deg):
        deg = max(0, min(180, deg))
        us = MIN_US + (MAX_US - MIN_US) * deg / 180
        # duty_u16: fraction of the 20 ms (20000 us) period
        duty = int(us / 20000 * 65535)
        self.pwm.duty_u16(duty)
        self._deg = deg

    def open(self):   self.write(self.open_deg)
    def close(self):  self.write(self.closed_deg)
    def to(self, frac):  # frac 0.0 (open) .. 1.0 (closed)
        self.write(self.open_deg + (self.closed_deg - self.open_deg) * frac)

# ---------- map fingers to the schematic pins ----------
thumb  = Servo(10)
index  = Servo(11)
middle = Servo(12)
ring   = Servo(13)
pinky  = Servo(14)
FINGERS = [thumb, index, middle, ring, pinky]

# ---------- EMG input ----------
emg = ADC(Pin(26))       # ADC0
def read_emg():
    # average a few samples to smooth noise
    s = 0
    for _ in range(16):
        s += emg.read_u16()
    return s // 16

# ---------- grip presets ----------
def grip_open():
    for f in FINGERS: f.open()

def grip_fist():
    for f in FINGERS: f.close()

def grip_pinch():
    # thumb + index close, rest open  (pinch / hold a pen)
    thumb.close(); index.close()
    middle.open(); ring.open(); pinky.open()

def grip_point():
    # index out, rest closed
    index.open()
    thumb.close(); middle.close(); ring.close(); pinky.close()

def grip_write():
    # writing tripod: thumb + index + middle lightly closed
    thumb.to(0.7); index.to(0.7); middle.to(0.6)
    ring.close(); pinky.close()

# ---------- smooth move (so it doesn't snap) ----------
def smooth_to(frac, steps=20, dly=0.02):
    start = [f._deg for f in FINGERS]
    target = [f.open_deg + (f.closed_deg - f.open_deg) * frac for f in FINGERS]
    for s in range(steps + 1):
        for i, f in enumerate(FINGERS):
            f.write(start[i] + (target[i] - start[i]) * s / steps)
        time.sleep(dly)

# =====================================================================
#  MODE 1 - EMG control
#  Flex muscle -> hand closes. Relax -> opens.
# =====================================================================
EMG_BASELINE = 8000      # calibrate: resting EMG value
EMG_THRESHOLD = 18000    # calibrate: flex above this = close

def calibrate_emg():
    print("Relax your arm... measuring baseline")
    time.sleep(2)
    vals = [read_emg() for _ in range(50)]
    base = sum(vals) // len(vals)
    print("baseline =", base)
    return base

def run_emg_mode():
    base = calibrate_emg()
    thresh = base + 10000
    print("EMG mode running. Flex to close.")
    while True:
        v = read_emg()
        # map EMG strength to grip fraction
        if v > thresh:
            frac = min(1.0, (v - base) / (thresh - base) - 0.0)
            for f in FINGERS: f.to(min(1.0, frac))
        else:
            grip_open()
        time.sleep(0.05)

# =====================================================================
#  MODE 2 - preset cycle (good for the 90-second demo / no EMG)
#  Cycles open -> fist -> pinch -> write so you can film it.
# =====================================================================
def run_demo_cycle():
    seq = [("open", grip_open), ("fist", grip_fist),
           ("pinch", grip_pinch), ("write", grip_write)]
    while True:
        for name, fn in seq:
            print("grip:", name)
            fn()
            time.sleep(2)

# =====================================================================
#  pick a mode here
# =====================================================================
if __name__ == "__main__":
    grip_open()
    time.sleep(1)
    # run_emg_mode()      # <- uncomment for EMG control
    run_demo_cycle()      # <- preset demo cycle (default)
