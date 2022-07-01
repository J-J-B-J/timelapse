from picamera import PiCamera
from os import system
import datetime
from time import sleep


def get_input(input_text: str):
    """Get an input as a None or int"""
    try:
        return int(input(input_text))
    except ValueError as e:
        if str(e) == "invalid literal for int() with base 10: ''":
            return None
        else:
            print("Invalid input!")
            exit()


print("Enter two of the following values:")
tlminutes = get_input("How many minutes to shoot for? ")
secondsinterval = get_input("How many seconds to wait between photos? ")
numphotos = get_input("How many photos to take? ")

if tlminutes and secondsinterval and (not numphotos):
    numphotos = int((tlminutes * 60) / secondsinterval)
elif tlminutes and (not secondsinterval) and numphotos:
    secondsinterval = int((tlminutes * 60) / secondsinterval)
elif (not tlminutes) and secondsinterval and numphotos:
    tlminutes = int((secondsinterval * numphotos) / 60)
else:
    print("Invalid input!")
    exit()

print("Taking {} photos with a {} second interval over {} minutes".
      format(numphotos, secondsinterval, tlminutes))

fps = 30  # frames per second timelapse video

dateraw = datetime.datetime.now()
datetimeformat = dateraw.strftime("%Y-%m-%d_%H:%M")
print("RPi started taking photos for your timelapse at: " + datetimeformat)

camera = PiCamera()
camera.resolution = (1024, 768)

system(
    'rm /home/pi/Pictures/*.jpg')  # delete all photos in the Pictures
# folder before timelapse start

for i in range(numphotos):
    camera.capture('/home/pi/Pictures/image{0:06d}.jpg'.format(i))
    sleep(secondsinterval)
print("Done taking photos.")
print("Please standby as your timelapse video is created.")

system(
    'ffmpeg -r {} -f image2 -s 1024x768 -nostats -loglevel 0 -pattern_type glob -i "/home/pi/Pictures/*.jpg" -vcodec libx264 -crf 25  -pix_fmt yuv420p /home/pi/Videos/{}.mp4'.format(
        fps, datetimeformat))
# system('rm /home/pi/Pictures/*.jpg')
print(
    'Timelapse video is complete. Video saved as /home/pi/Videos/{}.mp4'.format(
        datetimeformat))
