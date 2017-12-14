# -*- coding: utf-8 -*
from __future__ import print_function
from PIL import Image
import tensorflow as tf
import numpy as np
import os
def get_image_paths(img_dir):
    """
    Get all files' name under given dir img_dir
    """

    filenames = os.listdir(img_dir)
    filenames = [os.path.join(img_dir, item) for item in filenames]
    return filenames

pos_filenames = get_image_paths("./data/AntsClimbingTrees")
neg_filenames = get_image_paths("./data/beans")
print("num of AntsClimbingTrees is %d" % len(pos_filenames))
print("num of beans is %d" % len(neg_filenames))
# 将来嗯个文件假图片训练集：测试集 = 80：20
TRAIN_SEC, TEST_SEC = 0.8, 0.2
pos_sample_num, neg_sample_num = len(pos_filenames), len(neg_filenames)
np.random.shuffle(np.arange(len(pos_filenames)))
np.random.shuffle(np.arange(len(neg_filenames)))
pos_train, pos_test = pos_filenames[: int(pos_sample_num * TRAIN_SEC)], pos_filenames[int(pos_sample_num * TRAIN_SEC) :]
neg_train, neg_test = neg_filenames[: int(neg_sample_num * TRAIN_SEC)], neg_filenames[int(neg_sample_num * TRAIN_SEC) :]

print("AntsClimbingTrees : train num is %d, test num is %d" % (len(pos_train), len(pos_test)))
print("beans : train num is %d, test num is %d" % (len(neg_train), len(neg_test)))
# 训练集和测试集分开
all_train, all_test = [], []
all_train.extend(pos_train)
all_train.extend(neg_train)
all_test.extend(pos_test)
all_test.extend(neg_test)
all_train_label, all_test_label = np.ones(len(pos_train), dtype=np.int64), np.ones(len(pos_test), dtype=np.int64)
all_train_label.resize(len(all_train))
all_test_label.resize(len(all_test))
print("train num is %d, test num is %d" % (len(all_train), len(all_test)))
# 原始图片转换成TFRecord格式存储
def resize_img(img_path, shape):
    '''
        resize image given by `image_path` to `shape`
    '''
    im = Image.open(img_path)
    im = im.resize(shape)
    im = im.convert('RGB')
    return im
def save_as_tfrecord(samples, labels, bin_path):
    '''
        Save images and labels as TFRecord to file: `bin_path`
    '''
    assert len(samples) == len(labels)
    writer = tf.python_io.TFRecordWriter(bin_path)
    img_label = list(zip(samples, labels))
    np.random.shuffle(img_label)
    for img, label in img_label:
        #这里将图片的大小resize为128*128
        im = resize_img(img, (128, 128))
        #print(im.size)
        im_raw = im.tobytes()
        example = tf.train.Example(features=tf.train.Features(feature={
            "label": tf.train.Feature(int64_list=tf.train.Int64List(value=[label])),
            'img_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[im_raw]))
        }))
        writer.write(example.SerializeToString())
    writer.close()
save_as_tfrecord(all_test, all_test_label, "./data/train.bin")
save_as_tfrecord(all_train, all_train_label, "./data/test.bin")
# 开始构建模型

IMG_SIZE = 128  # 图像大小
LABEL_CNT = 2  # 标签类别的数量
P_KEEP_INPUT = 0.8  # 输入dropout层保持比例
P_KEEP_HIDDEN = 0.5  # 隐层dropout的保持比例


# 获取并初始化权重
def init_weights(shape):
    return tf.Variable(tf.truncated_normal(shape, stddev=0.1))


X = tf.placeholder("float", [None, IMG_SIZE, IMG_SIZE, 3])
Y = tf.placeholder("float", [None, 2])

w = init_weights([3, 3, 3, 32])
w2 = init_weights([3, 3, 32, 64])
w3 = init_weights([3, 3, 64, 128])
w4 = init_weights([3, 3, 128, 128])
w5 = init_weights([4 * 4 * 128, 625])
w_o = init_weights([625, 2])

p_keep_input = tf.placeholder("float")
p_keep_hidden = tf.placeholder("float")


# 简单的卷积模型
def simple_model(X, w, w_2, w_3, w_4, w_5, w_o, p_keep_input, p_keep_hidden):
    # batchsize * 128 * 128 * 3
    l1a = tf.nn.relu(tf.nn.conv2d(X, w, strides=[1, 1, 1, 1], padding='SAME'))
    # 2x2 max_pooling
    l1 = tf.nn.max_pool(l1a, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
    # dropout
    l1 = tf.nn.dropout(l1, p_keep_input)  # 64 * 64 * 32

    l2a = tf.nn.relu(tf.nn.conv2d(l1, w_2, strides=[1, 1, 1, 1], padding='SAME'))
    l2 = tf.nn.max_pool(l2a, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
    l2 = tf.nn.dropout(l2, p_keep_hidden)  # 32 * 32 * 64

    l3a = tf.nn.relu(tf.nn.conv2d(l2, w_3, strides=[1, 1, 1, 1], padding='SAME'))
    l3 = tf.nn.max_pool(l3a, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
    l3 = tf.nn.dropout(l3, p_keep_hidden)  # 16 * 16 * 128

    l4a = tf.nn.relu(tf.nn.conv2d(l3, w_4, strides=[1, 1, 1, 1], padding='SAME'))
    l4 = tf.nn.max_pool(l4a, ksize=[1, 4, 4, 1], strides=[1, 4, 4, 1], padding='SAME')  # 4 * 4 * 128
    l4 = tf.reshape(l4, [-1, w_5.get_shape().as_list()[0]])

    l5 = tf.nn.relu(tf.matmul(l4, w_5))
    l5 = tf.nn.dropout(l5, p_keep_hidden)

    return tf.matmul(l5, w_o)


# y_pred是预测tensor
y_pred = simple_model(X, w, w2, w3, w4, w5, w_o, p_keep_input, p_keep_hidden)

# 定义损失函数为交叉熵。
# 注意simple_model最后返回的不包含softmax操作，
# softmax_cross_entropy_with_logits会自动做softmax。
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=Y, logits=y_pred))
# 定义精度
correct_prediction = tf.equal(tf.argmax(Y, 1), tf.argmax(y_pred, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
# rmsprop方式对最小化损失函数
train_op = tf.train.RMSPropOptimizer(0.001, 0.9).minimize(cost)

# 读取数据训练模型
def read_and_decode(filename_queue):
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)   #return filename and example
    features = tf.parse_single_example(serialized_example,
                                       features={
                                           'label': tf.FixedLenFeature([], tf.int64),
                                           'img_raw' : tf.FixedLenFeature([], tf.string),
                                       })

    img = tf.decode_raw(features['img_raw'], tf.uint8)
    img = tf.reshape(img, [128, 128, 3])
    img = tf.cast(img, tf.float32) * (1. / 255) - 0.5 # normalize
    label = tf.cast(features['label'], tf.int32)
    label = tf.sparse_to_dense(label, [2], 1, 0)

    return img, label

def input_pipeline(filenames, batch_size, num_epochs=None):
    filename_queue = tf.train.string_input_producer(filenames, num_epochs=num_epochs, shuffle=True)
    example, label = read_and_decode(filename_queue)
    min_after_dequeue = 1000
    num_threads = 4
    capacity = min_after_dequeue + (num_threads + 3) * batch_size
    example_batch, label_batch = tf.train.shuffle_batch(
        [example, label], batch_size=batch_size, capacity=capacity, num_threads = num_threads,
        min_after_dequeue=min_after_dequeue)
    return example_batch, label_batch

# 获取batch。注意这里是tensor，需要运行
img_batch, label_batch = input_pipeline(["./data/train.bin"], 200)

# 接下来开始训练模型。每5步输出一次精度，每20步保存一下模型。
# disp_step = 5
# save_step = 20
# max_step = 1000  # 最大迭代次数
# step = 0
saver = tf.train.Saver()  # 用来保存模型的
# with tf.Session() as sess:
#     coord = tf.train.Coordinator()
#     sess.run(tf.initialize_all_variables())
#     sess.run(tf.initialize_local_variables())
#
#     # start_queue_runnes读取数据，具体用法参见官网
#     threads = tf.train.start_queue_runners(coord=coord)
#     try:
#         # 获取训练数据成功，并且没有到达最大训练次数
#         while not coord.should_stop() and step < max_step:
#             step += 1
#             # 运行tensor，获取数据
#             imgs, labels = sess.run([img_batch, label_batch])
#             # 训练。训练时dropout层要有值。
#             sess.run(train_op, feed_dict={X: imgs, Y: labels, p_keep_hidden: P_KEEP_HIDDEN, p_keep_input: P_KEEP_INPUT})
#             if step % disp_step == 0:
#                 # 输出当前batch的精度。预测时keep的取值均为1
#                 acc = sess.run(accuracy, feed_dict={X: imgs, Y: labels, p_keep_hidden: 1.0, p_keep_input: 1.0})
#                 print('%s accuracy is %.2f' % (step, acc))
#             if step % save_step == 0:
#                 # 保存当前模型
#                 save_path = saver.save(sess, './data/graph.ckpt', global_step=step)
#                 print("save graph to %s" % save_path)
#     except tf.errors.OutOfRangeError:
#         print("reach epoch limit")
#     finally:
#         coord.request_stop()
#     coord.join(threads)
#     save_path = saver.save(sess, './data/graph.ckpt', global_step=step)
#
# print("training is done")

# 进行预测
# 每batch随机取500张
test_img_batch, test_label_batch = input_pipeline(["./data/test.bin"], 5)
with tf.Session() as sess:
    # 加载模型。模型的文件名称看下本地情况
    saver.restore(sess, './data/graph.ckpt-1000')

    coord_test = tf.train.Coordinator()
    threads_test = tf.train.start_queue_runners(coord=coord_test)
    test_imgs, test_labels = sess.run([test_img_batch, test_label_batch])
    #预测阶段，keep取值均为1
    acc = sess.run(accuracy, feed_dict = {X : test_imgs, Y : test_labels, p_keep_hidden: 1.0, p_keep_input: 1.0})
    print("predict accuracy is %.2f" % acc)
    coord_test.request_stop()
    coord_test.join(threads_test)
