import base64
import codecs
import os
from io import BytesIO
from pathlib import Path
import numpy as np
from PIL import Image as pil_img
from cnn.computer_vision import ComputerVision
from cnn.cnn_model import Model as cnn_model


def pil_to_base64(image_path):
    """
    :param `image_path` for the complete path of image.
    """
    format = image_path.suffix.replace('.', '').lower()
    if not os.image_path.isfile(image_path):
        return None

    encoded_string = ''
    with open(image_path, 'rb') as img_f:
        encoded_string = base64.b64encode(img_f.read()).decode('ascii')
    return f'data:image/{format};base64, {encoded_string}'


def np_image_to_base64(np_image, format):
    np_image = pil_img.fromarray(np_image)
    img_bytes = BytesIO()
    np_image.save(img_bytes, format='PNG')
    encoded_string = codecs.encode(
        img_bytes.getvalue(), 'base64').decode('ascii')
    return f'data:image/{format};base64, {encoded_string}'


def computer_vision(image_path, image_settings):
    """
    :param `image_path` for the complete path of image.
    """
    format = image_path.suffix.replace('.', '').lower()
    # Open current file
    image = pil_img.open(image_path)
    # Image to array
    image = np.asarray(image)
    eritrocyte_length = int(image_settings['range_picker'])
    color_picker_h = [
        int(val) for val in image_settings['color_picker_h'].split(',')
    ]
    color_picker_s = [
        int(val) for val in image_settings['color_picker_s'].split(',')
    ]
    color_picker_v = [
        int(val) for val in image_settings['color_picker_v'].split(',')
    ]
    color_lower = np.array(
        [
            color_picker_h[0], color_picker_s[0], color_picker_v[0]
        ]
    )
    color_upper = np.array(
        [
            color_picker_h[1], color_picker_s[1], color_picker_v[1]
        ]
    )
    # Detect cells
    draw_image, cropped_images = ComputerVision(
        np_image=image,
        color_lower=color_lower,
        color_upper=color_upper,
        eritrocyte_length=eritrocyte_length).detect_cells()
    # Classify cells
    predictions = cnn_model(is_categorical=False).predict(cropped_images)
    return {'name': image_path.name,
            'draw_image': np_image_to_base64(draw_image, format),
            'predictions': predictions,
            }
