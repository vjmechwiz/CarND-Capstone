from styx_msgs.msg import TrafficLight
import cv2
import tensorflow as tf
import numpy as np


class TLClassifier(object):
    def __init__(self):
        #TODO load classifier
        self.trained_model_folder = '/home/workspace/CarND-Capstone/ros/src/tl_detector/light_classification/'
        self.trained_model_graph = self.trained_model_folder + 'traffic_lights.meta'
        
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        self.sess = tf.Session(config=config)

        self.saver = tf.train.import_meta_graph(self.trained_model_graph)
        self.saver.restore(self.sess, tf.train.latest_checkpoint(self.trained_model_folder + '.'))
        self.graph = tf.get_default_graph()
        self.x = self.graph.get_tensor_by_name("X:0")
        self.keep_prob = self.graph.get_tensor_by_name("Keep_prob:0")
        self.logits = self.graph.get_tensor_by_name("Logits:0")
        
    def get_classification(self, image):
        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        #TODO implement light color prediction
        test_prediction = 1
        req_width = int(image.shape[1] * 0.25)
        req_height = int(image.shape[0] * 0.25)
        resized_image = cv2.resize(image, (req_width, req_height), interpolation = cv2.INTER_AREA)
        norm_image = (resized_image - 127.5)/255.0
        test_input = np.expand_dims(norm_image, axis=0)
       
        test_prediction = self.sess.run(tf.argmax(self.logits, 1), feed_dict={self.x: test_input, self.keep_prob: 1.0})
   
        if test_prediction == 0:
            print("RED")
            return TrafficLight.RED
        else:
            print("UNKNOWN")
            return TrafficLight.UNKNOWN

