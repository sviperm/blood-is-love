import numpy as np
from keras import backend as K
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Lambda, Dense, Dropout,\
    Activation, Flatten
from django.conf import settings
from pathlib import Path


class Model():
    """
    Models class. Can create both of models.
    and predtict.
    """

    def __init__(self, is_categorical):
        super(Model, self).__init__()
        self.is_categorical = is_categorical
        if self.is_categorical:
            self.model = self.lanet_model_categotical()
            self.model.load_weights(
                Path(settings.BASE_DIR) / 'static' / 'weights' /
                'LaNet-categorical.hdf5')
        else:
            self.model = self.lanet_model_binary()
            self.model.load_weights(
                Path(settings.BASE_DIR) / 'static' / 'weights' /
                'LaNet-binary.hdf5')

    def summary(self):
        return self.model.summary()

    def lanet_model_categotical(self):
        self.model = Sequential()
        self.model.add(Lambda(lambda x: x / 127.5 - 1.,
                              input_shape=(120, 120, 3),
                              output_shape=(120, 120, 3)))
        self.model.add(Conv2D(32, (3, 3), input_shape=(120, 120, 3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Conv2D(32, (3, 3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Conv2D(64, (3, 3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Flatten())
        self.model.add(Dense(64))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(5))  # number of classes
        self.model.add(Activation('softmax'))

        self.model.compile(loss='categorical_crossentropy',
                           optimizer='rmsprop',
                           metrics=['accuracy'])

        return self.model

    def lanet_model_binary(self):
        self.model = Sequential()
        self.model.add(Lambda(lambda x: x / 127.5 - 1.,
                              input_shape=(120, 120, 3),
                              output_shape=(120, 120, 3)))
        self.model.add(Conv2D(32, (3, 3), input_shape=(120, 120, 3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Conv2D(32, (3, 3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Conv2D(64, (3, 3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Flatten())
        self.model.add(Dense(64))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.7))
        self.model.add(Dense(1))  # number of classes
        self.model.add(Activation('sigmoid'))

        self.model.compile(loss='binary_crossentropy',
                           optimizer='rmsprop',
                           metrics=['accuracy'])

        return self.model

    def predict(self, images):
        prediction = self.model.predict(images)
        percentage = self.model.predict_proba(images, batch_size=32, verbose=0)
        if self.is_categorical:
            classes = ['baso', 'eosi', 'lymp', 'mono', 'neut']
            prediction = np.argmax(prediction, axis=1)
        else:
            classes = ['mono', 'poly']
            prediction = np.rint(prediction.reshape(1, len(images)))[
                0].astype(int)
        result = []
        for count, i in enumerate(prediction):
            dictionary = {
                'count': count + 1,
                'result': classes[i],
            }
            if i == 0:
                percent = 1 - percentage[count]
            elif i == 1:
                percent = percentage[count]
            dictionary['percentage'] = "%.2f".replace(
                '[', '').replace(']', '') % (percent * 100)
            result.append(dictionary)
        K.clear_session()
        return result
