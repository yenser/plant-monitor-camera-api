import cv2

def toByteArray(image):
  is_success, im_buf_arr = cv2.imencode(".jpg", image)
  return (is_success, im_buf_arr.tobytes())