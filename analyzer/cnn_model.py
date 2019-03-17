from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Lambda, Dense, Dropout, Activation, Flatten
import numpy as np


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
            self.model.load_weights('presentation/weights/LaNet-categorical.hdf5')
        else:
            self.model = self.lanet_model_binary()
            self.model.load_weights('presentation/weights/LaNet-binary.hdf5')

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
        if self.is_categorical:
            classes = ['baso', 'eosi', 'lymp', 'mono', 'neut']
            prediction = np.argmax(prediction, axis=1)
        else:
            classes = ['mono', 'poly']
            prediction = np.rint(prediction.reshape(1, len(images)))[0].astype(int)
        return [classes[i] for i in prediction]
