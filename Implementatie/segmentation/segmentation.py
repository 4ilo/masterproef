import os
import numpy as np
import tensorflow as tf
import cv2

from segmentation.model import DeepLabResNetModel

IMG_MEAN = np.array((104.00698793, 116.66876762, 122.67891434), dtype=np.float32)
NUM_CLASSES = 27


class Segmentation:
    def __init__(self, image_path):
        self.image_path = image_path
        self.net = False
        self.img_ph = False
        self.pred = False
        self.sess = False

        self.IMG_MEAN = np.array((104.00698793, 116.66876762, 122.67891434), dtype=np.float32)
        self.NUM_CLASSES = 27

        self._init_network()

    def _load_image(self):
        # Read image
        img = tf.image.decode_png(tf.read_file(self.image_path), channels=3)

        # Convert to bgr
        img_r, img_g, img_b = tf.split(axis=2, num_or_size_splits=3, value=img)
        img = tf.cast(tf.concat(axis=2, values=[img_b, img_g, img_r]), dtype=tf.float32)

        img -= IMG_MEAN

        return img

    def _init_network(self):
        self._load_image()
        self.img_ph = tf.placeholder(tf.float32, shape=[None, None, None, 3])
        self.net = DeepLabResNetModel({'data': self.img_ph}, is_training=False, num_classes=self.NUM_CLASSES)

        restore_var = tf.global_variables()

        # Predictions
        raw_output = self.net.layers['fc_out']
        raw_output_up = tf.image.resize_bilinear(raw_output, tf.shape(self._load_image())[0:2, ])
        raw_output_up = tf.argmax(raw_output_up, axis=3)
        self.pred = tf.expand_dims(raw_output_up, axis=3)

        # Setup tf
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        self.sess = tf.Session(config=config)
        init = tf.global_variables_initializer()

        self.sess.run(init)

        # Load weights
        checkpoint = tf.train.get_checkpoint_state("segmentation/restore_weights")

        if checkpoint and checkpoint.model_checkpoint_path:
            loader = tf.train.Saver(var_list=restore_var)
            load_step = int(os.path.basename(checkpoint.model_checkpoint_path).split('-')[1])
            loader.restore(self.sess, checkpoint.model_checkpoint_path)
            print("Restored model parameters from {}".format(checkpoint.model_checkpoint_path))
        else:
            print("No checkpoint file found")

    def run(self, image_path):
        img = cv2.imread(image_path)
        return self.sess.run(self.pred, feed_dict={self.img_ph: np.expand_dims(img, axis=0)})


def run_segmentation(image_path: str):
    """ Run segmentation network on the given image """
    # Read image
    img = tf.image.decode_png(tf.read_file(image_path), channels=3)

    # Convert to bgr
    img_r, img_g, img_b = tf.split(axis=2, num_or_size_splits=3, value=img)
    img = tf.cast(tf.concat(axis=2, values=[img_b, img_g, img_r]), dtype=tf.float32)

    img -= IMG_MEAN

    img_ph = tf.placeholder(tf.float32, shape=[None, None, None, 3])
    # net = DeepLabResNetModel({'data': tf.expand_dims(img, axis=0)}, is_training=False, num_classes=NUM_CLASSES)
    net = DeepLabResNetModel({'data': img_ph}, is_training=False, num_classes=NUM_CLASSES)

    restore_var = tf.global_variables()

    # Predictions
    raw_output = net.layers['fc_out']
    raw_output_up = tf.image.resize_bilinear(raw_output, tf.shape(img)[0:2, ])
    raw_output_up = tf.argmax(raw_output_up, axis=3)
    pred = tf.expand_dims(raw_output_up, axis=3)

    # Setup tf
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)
    init = tf.global_variables_initializer()

    sess.run(init)

    # Load weights
    checkpoint = tf.train.get_checkpoint_state("segmentation/restore_weights")

    if checkpoint and checkpoint.model_checkpoint_path:
        loader = tf.train.Saver(var_list=restore_var)
        load_step = int(os.path.basename(checkpoint.model_checkpoint_path).split('-')[1])
        loader.restore(sess, checkpoint.model_checkpoint_path)
        print("Restored model parameters from {}".format(checkpoint.model_checkpoint_path))
    else:
        print("No checkpoint file found")

    test = cv2.imread(image_path)
    test2 = np.array(test)
    test2 = np.expand_dims(test2, axis=0)
    preds = sess.run(pred, feed_dict={img_ph: test2})

    return preds
