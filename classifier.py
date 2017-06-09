import mlb_parser
import tensorflow as tf
import os 
import urllib
import numpy as np


data = mlb_parser.main()

testing_data = data[20:]
train_data = data[:100]

# Model parameters
W = tf.Variable([.3], tf.float32)
b = tf.Variable([-.3], tf.float32)
# Model input and output
x = tf.placeholder(tf.float32)
linear_model = W * x + b
y = tf.placeholder(tf.float32)
# loss
loss = tf.reduce_sum(tf.square(linear_model - y)) # sum of the squares
# optimizer
optimizer = tf.train.GradientDescentOptimizer(0.01)
train = optimizer.minimize(loss)
# training data
x_train = []
for data in train_data:
	x_train.append(data[2])

#x_train = [.333,0,.250,.40]
print len(x_train)
y_train = []

for data in train_data:
	y_train.append(float(data[4]))
#y_train = [2,0,1,2]
print len(y_train)
# training loop
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init) # reset values to wrong
for i in range(1000):
  sess.run(train, {x:x_train, y:y_train})

# evaluate training accuracy
curr_W, curr_b, curr_loss  = sess.run([W, b, loss], {x:x_train, y:y_train})
print("W: %s b: %s loss: %s"%(curr_W, curr_b, curr_loss))

