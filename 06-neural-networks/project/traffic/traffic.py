import cv2
import numpy as np
import os
import sys
import warnings
warnings.filterwarnings(action='ignore')

# from tensorflow.python.keras import layers
import tensorflow as tf
from tqdm import tqdm

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
# NUM_CATEGORIES = 3
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    # tf.cast(labels, '')

    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE, random_state=42,
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    labels = []
    images = []
    categories = list(filter(lambda x: not x.startswith('.'), os.listdir(data_dir)))

    for each_category in tqdm(categories, desc='Reading folders'):
        if not each_category in map(lambda x : str(x), range(NUM_CATEGORIES)):
            # skip if not within the standard naming convention
            continue
        category_dir = os.path.join(data_dir, each_category)
        files = os.listdir(category_dir)
        # ppm refers to a Portable image format
        for file in files:

            path = os.path.join(category_dir, file)
            img = cv2.imread(path)

            # resize img 
            # According to cv2 docs:
            # To shrink an image, it will generally look best with #INTER_AREA interpolation
            img_dimension = (IMG_WIDTH, IMG_HEIGHT)
            resized = cv2.resize(img, img_dimension, interpolation = cv2.INTER_AREA)
            if resized.shape != (30, 30, 3):
                raise Exception('Error while resizing image.')

            images.append(resized/255)
            labels.append(int(each_category))

    print(resized.shape)
    print(np.unique(labels))
    return (images, labels)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    neural_network = tf.keras.models.Sequential(layers=[
        # Standardization (probably not so necessary as value is within 0-1)

        # centering data at mean = 0
        tf.keras.layers.BatchNormalization(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),


        # Pooling Layers

        # Extract primary set of informations (edges, contours)
        tf.keras.layers.Conv2D(filters=32, kernel_size=(3,3), activation='relu'),
        # Max Pooling to sample our data by the maximum value within block (2x2 pooling)
        tf.keras.layers.MaxPooling2D(pool_size=(2,2)),

        # Extract secondary set of informations (like objects)
        tf.keras.layers.Conv2D(filters=64, kernel_size=(3,3), activation='relu'),
        tf.keras.layers.MaxPooling2D(pool_size=(2,2)),

        # Extract tertiary set of informations (i don't know)
        tf.keras.layers.Conv2D(filters=128, kernel_size=(3,3), activation='relu'),
        tf.keras.layers.MaxPooling2D(pool_size=(2,2)),

        # flatten data so as it becomes the initial units of a deep neural network
        tf.keras.layers.Flatten(),

        # add a hidden layer here 
        tf.keras.layers.Dense(units=128, activation='relu'),
        
        # add a dropout so as to avoid overfitting (avoid over-reliance on specific units)
        tf.keras.layers.Dropout(rate=0.5),

        # Output Layer, using softmax to convert to probability distributions
        tf.keras.layers.Dense(NUM_CATEGORIES, activation='softmax'),
    ])

    neural_network.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return neural_network


if __name__ == "__main__":
    main()
