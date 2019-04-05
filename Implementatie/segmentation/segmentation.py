import os
import numpy as np
import tensorflow as tf

from .model import DeepLabResNetModel


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
        """ Load image in tensorflow format """
        # Read image
        img = tf.image.decode_png(tf.read_file(self.image_path), channels=3)

        # Convert to bgr
        img_r, img_g, img_b = tf.split(axis=2, num_or_size_splits=3, value=img)
        img = tf.cast(tf.concat(axis=2, values=[img_b, img_g, img_r]), dtype=tf.float32)

        img -= self.IMG_MEAN

        return img

    def _init_network(self):
        """ Initialise model and restore weights """
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

    def run(self, img):
        """ Run segmentation on opencv image. Shape must be the same as original image! """
        return self.sess.run(self.pred, feed_dict={self.img_ph: np.expand_dims(img, axis=0)})

    def get_floor_mask(self, img, floor_label=4):
        """ Create binary mask for floor pixels """
        n, h, w, c = img.shape

        mask = np.zeros((h, w), dtype=np.uint8)
        for j, j_val in enumerate(img[0, :, :, 0]):
            for i, i_val in enumerate(j_val):
                if i_val == floor_label:
                    mask[j, i] = 1

        return mask
