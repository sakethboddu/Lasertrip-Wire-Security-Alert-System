import time
from gpiozero import LightSensor, Buzzer
import RPi.GPIO as GPIO
from picamera2.encoders import H264Encoder
from picamera2 import Picamera2
import telepot
reading=0
def send_video():
  print("Recording video...")
  picam2 = Picamera2()
  video_config = picam2.create_video_configuration()
  picam2.configure(video_config)
  encoder = H264Encoder(bitrate=10000000)  
  picam2.start_recording(encoder, VIDEO_OUTPUT_PATH)
  time.sleep(10)  
  picam2.stop_recording()
  picam2.close()  
  print("Sending video...")
  try:
    bot = telepot.Bot(TELEGRAM_BOT_TOKEN)
    bot.sendVideo(chat_id='1896095728', video=open(VIDEO_OUTPUT_PATH, 'rb'))  
    print("Video sent successfully!")
  except Exception as e:
    print("Error sending video:", e)
    return
buzzer=Buzzer(18)
ldr_pin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
TELEGRAM_BOT_TOKEN = '7181373072:AAGXnq6cH7shlZug91scdljupWQUnebPILc'
VIDEO_OUTPUT_PATH = '/home/pi/Desktop/test.h264'

while True:
    GPIO.setup(ldr_pin,GPIO.OUT)
    GPIO.output(ldr_pin,GPIO.LOW)
    time.sleep(1)
    GPIO.setup(ldr_pin,GPIO.IN)
    while(GPIO.input(ldr_pin)==GPIO.LOW):
        reading = reading + 1
    print(reading)
    if (reading) >=3000 :
        print("LDR value above threshold, buzzer activated!")
        buzzer.on()
        buzzer.beep()
        send_video()
        buzzer.off()
        time.sleep(1)
    else:
        print(reading)
        print("LDR value below threshold, buzzer deactivated!")
        buzzer.off()
        time.sleep(1)
