'''
Usage: python3 tf_record_handler.py
'''

import tensorflow as tf
import yaml
import os
from convert_xml_to_yaml import *


LABEL_DICT =  {
    "green" : 1,
    "red" : 2,
    "yellow" : 3,
    "off" : 4,
    }

def int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def int64_list_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))

def bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def bytes_list_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=value))

def float_list_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))


def create_tf_record(record):

    # data set
    height = 600 # Image height
    width = 800 # Image width

    filename = record['annotation']['filename'] # Filename of the image. Empty if image is not from file
    filename = filename.encode()

    with tf.gfile.GFile(record['annotation']['filename'], 'rb') as fid:
        encoded_image = fid.read()

    image_format = 'jpg'.encode()

    xmins = [] # List of normalized left x coordinates in bounding box (1 per box)
    xmaxs = [] # List of normalized right x coordinates in bounding box
                # (1 per box)
    ymins = [] # List of normalized top y coordinates in bounding box (1 per box)
    ymaxs = [] # List of normalized bottom y coordinates in bounding box
                # (1 per box)
    classes_text = [] # List of string class name of bounding box (1 per box)
    classes = [] # List of integer class id of bounding box (1 per box)

    #find the boxes on annotated pictures
    xmin = record['annotation']['object']['bndbox']['xmin']
    xmins.append(float(int(xmin) / width))
    xmax = record['annotation']['object']['bndbox']['xmax']
    xmaxs.append(float(int(xmax) / width))
    ymin = record['annotation']['object']['bndbox']['ymin']
    ymins.append(float(int(ymin) / height))
    ymax = record['annotation']['object']['bndbox']['ymax']
    ymaxs.append(float(int(ymax) / height))

    #set the class labels and the class ids
    klass = record['annotation']['object']['name']
    classes_text.append(klass.encode())
    klass_id = int(LABEL_DICT[klass])
    classes.append(klass_id)

    tf_record = tf.train.Example(features=tf.train.Features(feature={
        'height'        : int64_feature(height),
        'width'         : int64_feature(width),
        'filename'      : bytes_feature(filename),
        'image_encoded' : bytes_feature(encoded_image),
        'image_format'  : bytes_feature(image_format),
        'xmin'          : float_list_feature(xmins),
        'xmax'          : float_list_feature(xmaxs),
        'ymin'          : float_list_feature(ymins),
        'ymax'          : float_list_feature(ymaxs),
        'class'         : bytes_list_feature(classes_text),
        'class_id'      : int64_list_feature(classes)
    }))

    return tf_record


def main(_):

    #paths for YAML and JPG files
    INPUT_YAML_PATH = './images/train/annotations/'
    INPUT_YAML = './images/train/annotations/annotations.yaml'
    INPUT_JPG_PATH = './images/train/images/'


    #generate input yaml file
    mulitple_xml_to_yaml(INPUT_YAML_PATH)

    #set up output file
    out_file = 'tf_record_sim.record'
    #set up write for TFRecord File
    writer = tf.python_io.TFRecordWriter(out_file)

    #get the records from yaml file
    records = yaml.load(open(INPUT_YAML, 'rb').read())

    #print("Loaded ", len(records), "examples")

    #concat the file path and file name
    for i in range(len(records)):
        records[i]['annotation']['filename'] = os.path.abspath(
            os.path.join(
                os.path.dirname(INPUT_JPG_PATH), records[i]['annotation']['filename']))
        tf_record = create_tf_record(records[i])
        writer.write(tf_record.SerializeToString())

    #close TFRecord File writer
    writer.close()

if __name__ == '__main__':
    tf.app.run()
