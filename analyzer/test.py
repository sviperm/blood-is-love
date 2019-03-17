'''from model import Model
from computer_vision import Computer_vision'''

from .model import Model
from .computer_vision import ComputerVision

categorical_model = Model(is_categorical=True)
binary_model = Model(is_categorical=False)

path_dir = '/Users/sviperm/Documents/Recognition_of_leukocytes/presentation/images'
cv = ComputerVision(images_dir=path_dir, eritrocyte_length=70)
cropped_images, _, _ = cv.detect_cells()

categorical_model.predict(cropped_images)
binary_model.predict(cropped_images)

cv.show_images(cropped_images)
