import tensorflow as tf
import numpy as np

slim = tf.contrib.slim

BATCH_SIZE = 16
LEARNING_RATE_BASE = 1e-3
LEARNING_RATE_DECAY = 0.99
REGULARIZATION_RATE = 0.001
TRAINING_STEPS = 10000
MOVING_AVERAGE_DECAY = 0.99

IMAGE_SIZE = 300
NUM_CHANNELS = 1
NUM_LABELS = 3
FC_SIZE = 4096


def read_data(fileNameQue):
    reader = tf.TFRecordReader()
    _, serialize_example = reader.read(fileNameQue)
    features = tf.parse_single_example(serialize_example,
                                       features={
                                           'label': tf.FixedLenFeature([], tf.int64),
                                           'img_raw': tf.FixedLenFeature([], tf.string),
                                       })
    img = tf.decode_raw(features["img_raw"], tf.uint8)
    img = tf.reshape(img, [IMAGE_SIZE, IMAGE_SIZE])  # 恢复图像原始大小
    label = tf.cast(features["label"], tf.int32)
    return img, label


def batch_input(filename, batchSize):
    fileNameQue = tf.train.string_input_producer([filename], shuffle=True)
    img, label = read_data(fileNameQue)  # fetch图像和label
    min_after_dequeue = 10000
    capacity = min_after_dequeue + 3 * batchSize
    # 预取图像和label并随机打乱，组成batch，此时tensor rank发生了变化，多了一个batch大小的维度
    exampleBatch, labelBatch = tf.train.shuffle_batch([img, label], batch_size=batchSize, capacity=capacity,
                                                      min_after_dequeue=min_after_dequeue)
    return exampleBatch, labelBatch


def vgg16(inputs):
    with slim.arg_scope([slim.conv2d, slim.fully_connected],
                        activation_fn=tf.nn.relu,
                        weights_initializer=tf.truncated_normal_initializer(0.0, 0.01),
                        weights_regularizer=slim.l2_regularizer(0.0005)):
        net = slim.repeat(inputs, 2, slim.conv2d, 64, [3, 3], scope='conv1')
        net = slim.max_pool2d(net, [2, 2], scope='pool1')
        net = slim.repeat(net, 2, slim.conv2d, 128, [3, 3], scope='conv2')
        net = slim.max_pool2d(net, [2, 2], scope='pool2')
        net = slim.repeat(net, 3, slim.conv2d, 256, [3, 3], scope='conv3')
        net = slim.max_pool2d(net, [3, 3], 3, scope='pool3')
        net = slim.repeat(net, 3, slim.conv2d, 512, [3, 3], scope='conv4')
        net = slim.max_pool2d(net, [5, 5], 5, scope='pool4', padding='SAME')
        net = slim.repeat(net, 3, slim.conv2d, 512, [3, 3], scope='conv5')
        net = slim.max_pool2d(net, [5, 5], 5, scope='pool5')
        net = slim.fully_connected(net, 4096, scope='fc6')
        net = slim.dropout(net, 0.5, scope='dropout6')
        net = slim.fully_connected(net, FC_SIZE, scope='fc7')
        net = slim.dropout(net, 0.5, scope='dropout7')
        net = slim.fully_connected(net, NUM_LABELS, activation_fn=None, scope='fc8')
    return net


if __name__ == '__main__':
    # 定义输出为4维矩阵的placeholder
    x = tf.placeholder(tf.float32, [
        BATCH_SIZE,
        IMAGE_SIZE,
        IMAGE_SIZE,
        NUM_CHANNELS],
        name='x-input')
    y_ = tf.placeholder(tf.int64, [BATCH_SIZE], name='y-input')
    # tf.summary.image('image', x, 1)
    y = vgg16(x)
    y = tf.reshape(y, [-1, NUM_LABELS])
    global_step = tf.Variable(0, trainable=False)

    # 定义损失函数、学习率、滑动平均操作以及训练过程。
    variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)
    variables_averages_op = variable_averages.apply(tf.trainable_variables())
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=(y + 1e-10), labels=y_)
    # tf.summary.histogram('cross_entropy', cross_entropy)
    loss = tf.reduce_mean(cross_entropy)
    # tf.summary.histogram('loss', loss)

    learning_rate = tf.train.exponential_decay(
        LEARNING_RATE_BASE,
        global_step,
        10000 / BATCH_SIZE, LEARNING_RATE_DECAY,
        staircase=True)
    # tf.summary.scalar('learning_rate', learning_rate)
    train_step = tf.train.AdamOptimizer(learning_rate).minimize(loss, global_step=global_step)
    with tf.control_dependencies([train_step, variables_averages_op]):
        train_op = tf.no_op(name='train')
    # correct_prediction = tf.equal(tf.argmax(y, 1), y_)
    # accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    # 初始化TensorFlow持久化类。
    saver = tf.train.Saver()
    exampleBatch, labelBatch = batch_input("./Taobao.tfrecords", batchSize=BATCH_SIZE)
    #exampleTest, labelTest = batch_input("./Letter_train_test.tfrecords", batchSize=BATCH_SIZE)
    # merged = tf.summary.merge_all()

    with tf.Session() as sess:
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord, sess=sess)
        tf.global_variables_initializer().run()
        for i in range(TRAINING_STEPS):
            example, labeltemp = sess.run([exampleBatch, labelBatch])
            reshaped_xs = np.reshape(example, (
                BATCH_SIZE,
                IMAGE_SIZE,
                IMAGE_SIZE,
                NUM_CHANNELS))
            # writer = tf.summary.FileWriter('./tensorboard', sess.graph)
            _, loss_value, step = sess.run([train_op, loss, global_step], feed_dict={x: reshaped_xs, y_: labeltemp})
            print("Step %d the loss value is: %f" % (step, loss_value))
            # writer.add_summary(summary, step)
            if i % 100 == 0:
                saver.save(sess, './model/Taobao.ckpt')
                print('The model has been saved.')
            #     exampleTest, labeltemp_t = sess.run([exampleBatch, labelBatch])
            #     reshaped_t = np.reshape(exampleTest, (
            #         BATCH_SIZE,
            #         IMAGE_SIZE,
            #         IMAGE_SIZE,
            #         NUM_CHANNELS))
            #     accuracy_t = sess.run(accuracy, feed_dict={x: reshaped_t, y_: labeltemp_t})
            #     print("After %d training step(s), loss on training batch is %g, accuracy:%g." % (
            #     step, loss_value, accuracy_t))
        coord.request_stop()
        coord.join(threads)
