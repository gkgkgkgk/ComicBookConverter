import functools
import os

from matplotlib import gridspec
import matplotlib.pylab as plt
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import PIL.Image as Image

print("TF Version: ", tf.__version__)
print("TF Hub version: ", hub.__version__)
print("Eager mode enabled: ", tf.executing_eagerly())
print("GPU available: ", tf.config.list_physical_devices('GPU'))


def get_img(image_url):
  return tf.keras.utils.get_file(os.path.basename(image_url)[-128:], image_url)


@functools.lru_cache(maxsize=None)
def load_image(image_url):
  """Loads and preprocesses images."""
  # Cache image file locally.
  # Load and convert to float32 numpy array, add batch dimension, and normalize to range [0, 1].
  image_path = get_img(image_url)
  img = tf.io.decode_image(
      tf.io.read_file(image_path),
      channels=3, dtype=tf.float32)[tf.newaxis, ...]

  return img


def tensor_to_image(tensor):
  print(tf.size(tensor))
  tensor = tensor*255
  tensor = np.array(tensor, dtype=np.uint8)
  if np.ndim(tensor)>3:
    assert tensor.shape[0] == 1
    tensor = tensor[0]
  return Image.fromarray(tensor)

def generate_image(content_image_url):
  style_image_url = 'https://cafans.b-cdn.net/images/Category_96487/subcat_144155/YjnkHUty_1003181702191gpadd.jpg'

  content_image = load_image(content_image_url)
  style_image = load_image(style_image_url)
  style_image = tf.nn.avg_pool(style_image, ksize=[2,2], strides=[1,1], padding='SAME')

  hub_handle = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'
  hub_module = hub.load(hub_handle)

  outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
  stylized_image = outputs[0]
  img_overlay = tensor_to_image(stylized_image)
  img_overlay.save("./result_fg.png")
  fg = img_overlay.convert("RGBA")


  style_image_url = 'https://www.sellmycomicbooks.com/images/cap-villains-hitler.jpg'
  style_image = load_image(style_image_url)
  style_image = tf.nn.avg_pool(style_image, ksize=[5,5], strides=[1,1], padding='SAME')

  outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
  stylized_image = outputs[0]
  background = tensor_to_image(stylized_image)
  background.save("./result_bg.png")
  bg = background.convert("RGBA")



  new_img = Image.blend(bg, fg, 0.25)
  new_img.save("new.png","PNG")

# 960 x 448
# outputs = hub_module(tf.constant(stylized_image), tf.constant(content_image))
# stylized_image = outputs[0]
# img = tensor_to_image(stylized_image).save("./result_second.png")

generate_image('https://www.thewrap.com/wp-content/uploads/2022/03/Robert-Pattinson-The-Batman1-936x527.jpg')