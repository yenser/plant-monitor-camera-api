import time
import picamera
import picamera.array
import cv2

class Camera:
  def capture(self):
    with picamera.PiCamera() as camera:
      # Set the camera resolution
      x = 1024
      y = 768
      camera.resolution = (x, y)

      # Various optional camera settings below:
      # camera.framerate = 5
      # camera.awb_mode = 'off'
      # camera.awb_gains = (0.5, 0.5)

      # Need to sleep to give the camera time to get set up properly
      time.sleep(1)

      with picamera.array.PiRGBArray(camera) as stream:
        # Grab data from the camera, in colour format
        # NOTE: This comes in BGR rather than RGB, which is important
        # for later!
        camera.capture(stream, format='rgb')
        image = stream.array

        # image = rotate_image(image, 180)

        # Get the individual colour components of the image
        # b, g, r = cv2.split(image)

        # # Calculate the NDVI

        # # Bottom of fraction
        # bottom = (r.astype(float) + b.astype(float))
        # bottom[bottom == 0] = 0.01  # Make sure we don't divide by zero!

        # ndvi = (r.astype(float) - b) / bottom
        # ndvi = contrast_stretch(ndvi)
        # ndvi = ndvi.astype(np.uint8)

        # # Combine ready for display
        # combined = disp_multiple(b, g, r, ndvi)

        # Display
        # cv2.imshow('image', combined)

        # cv2.imwrite('images/image.jpg', image)

        stream.truncate(0)

        return image