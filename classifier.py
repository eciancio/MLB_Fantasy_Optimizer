import mlb_parser
import tensorflow as tf
import os 
import urllib
import numpy as np
import tempfile
import urllib
train_file = tempfile.NamedTemporaryFile()
test_file = tempfile.NamedTemporaryFile()

data = mlb_parser.main()

testing_data = data[:100]
train_data = data[100:]

#read in av data
x_train = []
for data in train_data:
	x_train.append(data[2])

x_test = []
for data in testing_data:
	x_test.append(data[2])


#read in hit data 
y_train = []
for data in train_data:
    if data[4] > 0:
        data[4] = 1
    y_train.append(int(data[4]))
y_test = []
for data in testing_data:
    if data[4] > 0:
        data[4] = 1
    y_test.append(int(data[4]))


#make columns 
COLUMNS= ['avg','hits']
test_continious_cols = []
test_labels = []

#avg column 
avg = tf.contrib.layers.real_valued_column("avg")


model_dir = tempfile.mkdtemp()
m = tf.contrib.learn.LinearClassifier(feature_columns=[avg],
          model_dir=model_dir)

def input_fn_traint():
    #make cols
    continuous_cols = {'avg': tf.constant(x_train)}
    labels = tf.constant(y_train)
    return continuous_cols, labels

def input_fn_test():
    test_continuous_cols = {'avg': tf.constant(x_test)}
    test_labels = tf.constant(y_test)
    return test_continuous_cols, test_labels

m.fit(input_fn=input_fn_traint, steps=200)
results = m.evaluate(input_fn=input_fn_test, steps=1)
for key in sorted(results):
        print("%s: %s" % (key, results[key]))


def input_fn(df):
    # Creates a dictionary mapping from each continuous feature column name (k) to
    # the values of that column stored in a constant Tensor.
    continuous_cols = {k: tf.constant(df[k].values)
            for k in CONTINUOUS_COLUMNS}
    # Creates a dictionary mapping from each categorical feature column name (k)
    # to the values of that column stored in a tf.SparseTensor.
    categorical_cols = {k: tf.SparseTensor(
        indices=[[i, 0] for i in range(df[k].size)],
        values=df[k].values,
        dense_shape=[df[k].size, 1])
        for k in CATEGORICAL_COLUMNS}
    # Merges the two dictionaries into one.
    feature_cols = dict(continuous_cols.items() + categorical_cols.items())
    # Converts the label column into a constant Tensor.
    label = tf.constant(df[LABEL_COLUMN].values)
    # Returns the feature columns and the label.
    return feature_cols, label







