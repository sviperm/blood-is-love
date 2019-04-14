import numpy as np
from PIL import Image as pil_img
import base64


def pil_to_base64(image_path):
    """
    :param `image_path` for the complete path of image.
    """
    import os
    format = image_path.suffix.replace('.', '').lower()
    if not os.image_path.isfile(image_path):
        return None

    encoded_string = ''
    with open(image_path, 'rb') as img_f:
        encoded_string = base64.b64encode(img_f.read()).decode('ascii')
    return f'data:image/{format};base64, {encoded_string}'


def np_image_to_base64(np_image, format):
    import codecs
    from io import BytesIO
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
    from .cnn.computer_vision import ComputerVision
    from .cnn.cnn_model import Model as cnn_model
    format = image_path.suffix.replace('.', '').lower()
    # Open current file
    image = pil_img.open(image_path)
    # Image to array
    image = np.asarray(image)
    # if image has alfa layer -> delete it
    if np.size(image, 2) == 4:
        image = np.delete(image, 3, 2)
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


def get_result(images):
    result = {'types': [],
              'total': 0, }
    for image in images:
        for prediction in image['predictions']:
            result['total'] += 1
            if result['types']:
                for cell_type in result['types']:
                    type_exist = False
                    if cell_type['name'] == prediction['result']:
                        cell_type['count'] += 1
                        type_exist = True
                        break
                if not type_exist:
                    result['types'].append({
                        'name': prediction['result'],
                        'count': 1,
                    })
            else:
                result['types'].append({
                    'name': prediction['result'],
                    'count': 1,
                })
    for cell_type in result['types']:
        cell_type['percent'] = "%.2f" % (
            cell_type['count'] / result['total'] * 100)
    return result
