from styx_msgs.msg import TrafficLight
import tensorflow as tf
import numpy as np
import cv2
import os

FASTER_RCNN_INCEPTION_V2_MODEL = 'light_classification/model_04/faster_rcnn_inception_v2_traffic_lights.pb'

class TLClassifier(object):
    def __init__(self):
        self.model_file = FASTER_RCNN_INCEPTION_V2_MODEL
        self.detection_graph = self.load_graph(self.model_file)
       
        #create session
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        self.session = tf.Session(graph=self.detection_graph, config=config)
        
        #get variables from graph in session
        self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        self.states = [TrafficLight.RED, TrafficLight.YELLOW, TrafficLight.GREEN, TrafficLight.UNKNOWN]
        self.color_text = ['RED', 'YELLOW', 'GREEN', 'OFF']


    def get_classification(self, image):
        """Performs actual classification on images"""
        image_expand = np.expand_dims(image, axis=0)
        (boxes, scores, classes) = self.session.run([self.detection_boxes, self.detection_scores, self.detection_classes], feed_dict={self.image_tensor: image_expand})

        # Remove unnecessary dimensions
        boxes = np.squeeze(boxes)
        scores = np.squeeze(scores)
        classes = np.squeeze(classes)
        
        index = int(classes[0]) - 1
        #print ("Color is", self.color_text[index])

        return self.states[index]
  

    def load_graph(self, graph_file):
        """Loads a frozen inference graph"""
        graph = tf.Graph()
        with graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(graph_file, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)

                tf.import_graph_def(od_graph_def, name='')

        return graph

        
                
       

 
