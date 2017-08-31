import os
import tensorflow as tf
from PIL import Image
import numpy as np

cwd = r'/media/irvine/Design/OneDrive/fishionRecommend/'
classes = {'suit':0, 'sports':1, 'casual':2}
writer = tf.python_io.TFRecordWriter('Taobao.tfrecords')

for name in classes:
    index = classes[name]
    class_path = cwd + name + r'/'
    print(class_path, index, name)
    for img_name in os.listdir(class_path):
        img_path = class_path + img_name
        try:
            img = Image.open(img_path)
            img = img.convert('L')
        except Exception as e:
            print(e)
            print(img_path)
            continue
        img = img.resize((300, 300), Image.ANTIALIAS)
        img_raw = img.tobytes()
        example = tf.train.Example(features=tf.train.Features(feature={
            'label': tf.train.Feature(int64_list=tf.train.Int64List(value=[index])),
            'img_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw]))
        }))
        writer.write(example.SerializeToString())
writer.close()