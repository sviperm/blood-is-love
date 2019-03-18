import base64
import urllib
from io import BytesIO, StringIO

import numpy as np
from django.test import TestCase
from PIL import Image


def image_to_html(file):

    format = file.image.format

    # io.BytesIo
    # image = file.file
    # string = base64.b64encode(image.read())
    # url = 'data:image/jpeg;base64,' + urllib.parse.quote(string)
    # html = f'<img src = "{url}"/>'
    # return url

    # PIL

    output = StringIO()
    # image2 = file.image
    # im1 = Image.open(
    #     'C:\\Users\\sviperm\\Documents\\blood-of-vlad\\analyzer\\test-img-2.png')
    im = file.image  # Your image here!
    im.load()
    # im.split()
    im.save(output, format='PNG')
    output.seek(0)
    output_s = output.read()
    img_str = base64.b64encode(output_s)

    # buffered = BytesIO()
    # image.save(buffered, format="PNG")
    # img_str = base64.b64encode(buffered.getvalue())
    # array_image = np.asarray(image)
    # image = Image.fromarray(array_image)
    # img_str = base64.b64encode(array_image)

    # buffered = BytesIO()
    # image.save(buffered, format=format.upper())
    # img_str = base64.b64encode(buffered.getvalue()

    url = f'data:image/{format.lower()};base64,{img_str}'
    html = f'<img src = "{url}"/>'
    return url
