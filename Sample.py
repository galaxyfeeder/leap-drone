import Leap, sys, thread, time, threading, serial

MAX_HEIGHT_MM = 200
MIN_HEIGHT_MM = 25
MAX_PITCH_MM = 0.7
MAX_ROLL_MM = 0.7

height_sum = 0
pitch_sum = 0
roll_sum = 0
counter_left = 0
counter_right = 0

ser = None

def clean_height():
    avg = height_sum/counter_left
    if avg > MAX_HEIGHT_MM:
        avg = MAX_HEIGHT_MM
    elif avg < MIN_HEIGHT_MM:
        avg = MIN_HEIGHT_MM
    avg -= MIN_HEIGHT_MM
    return avg*100/(MAX_HEIGHT_MM - MIN_HEIGHT_MM)

def clean_roll():
    avg = roll_sum/counter_right
    if avg > MAX_ROLL_MM:
        avg = MAX_ROLL_MM
    elif avg < -MAX_ROLL_MM:
        avg = -MAX_ROLL_MM
    avg += MAX_ROLL_MM
    return avg*100/MAX_ROLL_MM/2

def clean_pitch():
    avg = pitch_sum/counter_right
    if avg > MAX_PITCH_MM:
        avg = MAX_PITCH_MM
    elif avg < -MAX_PITCH_MM:
        avg = -MAX_PITCH_MM
    avg += MAX_PITCH_MM
    return avg*100/MAX_PITCH_MM/2

def transfrom_ascii(x):
    if x >= 0 and x <= 9:
        return str(x)
    else:
        return ':'

def sender():
    global counter_left, height_sum, ser, counter_right, pitch_sum, roll_sum
    if counter_left != 0 and counter_right != 0:
        if ser:
            ser.write(transfrom_ascii(clean_height()/10))
            ser.write(transfrom_ascii(clean_pitch()/10))
            ser.write(transfrom_ascii(clean_roll()/10))
            
        print '\033[91m Throt: %i  \033[92m \t Pitch: %i \033[93m \t Roll: %i \033[94m \t Yaw: 50 \033[39m' % (clean_height(), clean_pitch(), clean_roll())
        height_sum = 0
        pitch_sum = 0
        roll_sum = 0
        counter_left = 0
        counter_right = 0
    threading.Timer(0.1, sender).start()

class SampleListener(Leap.Listener):

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"
        sender()

    def on_disconnect(self, controller):
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        global counter_right, height_sum, counter_left, pitch_sum, roll_sum
        frame = controller.frame()
        
        for hand in frame.hands:
            if hand.is_right:
                pitch_sum += hand.direction.pitch
                roll_sum += hand.palm_normal.roll
                counter_right += 1
            elif hand.is_left:
                height_sum += hand.palm_position.y
                counter_left += 1

def main():
    global ser
    listener = SampleListener()
    controller = Leap.Controller()
    ser = serial.Serial('/dev/ttyUSB0')

    controller.add_listener(listener)
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
