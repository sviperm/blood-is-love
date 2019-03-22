import os
import numpy as np
import cv2
# import PyQt5
import matplotlib
# matplotlib.use('Qt5Agg')

# In[0]: %matplotlib inline
from matplotlib import pyplot as plt
from pprint import pprint as pp


def get_list_of_dir(path):
    return [f for f in os.listdir(path) if not f.startswith('.')]


class ComputerVision():
    """docstring for Computer_vision."""

    # er_length = 40

    def __init__(self,
                 images_dir: str,
                 eritrocyte_length: int,
                 color_lower=np.array([120, 80, 50]),
                 color_upper=np.array([175, 270, 270])):
        super(ComputerVision, self).__init__()
        self.images_dir = images_dir
        self.images_file_names = get_list_of_dir(images_dir)
        self.color_lower = color_lower
        self.color_upper = color_upper
        self.eritrocyte_length = eritrocyte_length
        self.min_cell_size = eritrocyte_length

    def detect_cells(self):
        """
        Detect cells and return images with them
        Returning: images_list, draw_list, source_images"""
        # Pick custom color via 'helpers/color_picker.py'
        # I suggest change only mid lower value
        lower = self.color_lower
        upper = self.color_upper
        source_images = []
        images_list = []
        draw_list = []
        # Convert to HCV format, then masking (black/white image),
        # then bluring (cleaning from dirt and small detected objects)
        for file_name in self.images_file_names:
            image_path = os.path.join(self.images_dir, file_name)
            img = cv2.imread(image_path)
            img_for_paint = cv2.imread(image_path)
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            mask = cv2.inRange(hsv, lower, upper)
            median = cv2.medianBlur(mask, 7)

            # Combine nearby nucleus
            # https://stackoverflow.com/questions/50432349/combine-contours-vertically-and-get-convex-hull-opencv-python
            rect_kernel = cv2.getStructuringElement(
                cv2.MORPH_ELLIPSE, (15, 15))
            threshed = cv2.morphologyEx(median, cv2.MORPH_CLOSE, rect_kernel)

            # Clean small dirt on image
            _, contours, _ = cv2.findContours(
                threshed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = self.clean_image(contours)

            # Draw detected nucleus on source image
            cv2.drawContours(image=img_for_paint, contours=contours,
                             contourIdx=-1, color=(0, 255, 0),
                             thickness=2, lineType=8, offset=(0, 0))

            # Crop source image to small one and only cell samll images
            cropped_images = self.crop_image(img, img_for_paint, contours)
            source_images.append(img)
            images_list.append(cropped_images)
            draw_list.append(img_for_paint)
        return images_list[0], draw_list, source_images

    def clean_image(self, contours):
        """Returning contours without dirt (if dirt less then 2/3
        of the length of the circle of eritrocyte)"""
        # Read for more info about convexHull:
        # https://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html
        for index, contour in reversed(list(enumerate(contours))):
            if (len(contour) < self.min_cell_size):
                contours = np.delete(arr=contours, obj=index)
        contours = np.array([cv2.convexHull(contour) for contour in contours])
        return contours

    def crop_image(self, image_for_crop, image_for_paint, contours):
        """Croping images around single contour with right proportion"""

        height, width = image_for_crop.shape[:2]
        cropped_images = []
        # Get max and min x/y of nucleus.
        # https://www.pyimagesearch.com/2016/04/11/finding-extreme-points-in-contours-with-opencv/
        for i, c in enumerate(contours):
            x_min = tuple(c[c[:, :, 0].argmin()][0])[0]
            y_min = tuple(c[c[:, :, 1].argmin()][0])[1]
            x_max = tuple(c[c[:, :, 0].argmax()][0])[0]
            y_max = tuple(c[c[:, :, 1].argmax()][0])[1]

            # x/y delta for cropping full cel, not just only nucleus
            crop_size = 3 * self.eritrocyte_length
            x_delta = int(x_max - x_min)
            y_delta = int(y_max - y_min)
            max_delta = max([x_delta, y_delta])

            if crop_size > x_delta and crop_size > y_delta:
                crop_delta = (crop_size - max_delta) // 2
                # Make sure that we are in borders of the image
                x_min = 0 if x_min - crop_delta < 0 else x_min - crop_delta
                x_max = width if x_max + crop_delta > width else x_max + crop_delta
                y_min = 0 if y_min - crop_delta < 0 else y_min - crop_delta
                y_max = height if y_max + crop_delta > height else y_max + crop_delta

            # Draw
            cv2.rectangle(image_for_paint, (x_min, y_min),
                          (x_max, y_max), (255, 0, 0), 2)

            # Cropping
            cropped_img = image_for_crop[y_min:y_max, x_min:x_max]
            cropped_img = cv2.resize(cropped_img,
                                     dsize=(120, 120),
                                     interpolation=cv2.INTER_CUBIC)
            cropped_images.append(cropped_img)

        cropped_images = np.asarray(cropped_images)
        return cropped_images

    def show_images(self, images):
        for i in range(len(images)):
            plt.imshow(images[i])
            plt.axis('off')
            plt.show()
