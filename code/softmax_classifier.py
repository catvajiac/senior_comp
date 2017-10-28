#!/usr/bin/env python2.7

import load_mnist as lm
import numpy as np

class SoftmaxClassifier(object):
  def __init__(self, num_classes):
    ''' initialize model parameters

        num_classes -- number of classes
    '''
    self.num_classes = num_classes
  
  def train(self, X, y, batch_size=128, num_iterations=1000, learning_rate=.01):
    ''' train classifier for given number of iterations

        X               -- entire set of training data
        y               -- labels for training data
        batch_size      -- number of training examples per batch
        num_iterations  -- number of iterations to train for
        learning_rate   -- how much we move with the gradient at each iteration
    '''
    self.learning_rate = learning_rate

    self.W = np.zeros((X.shape[1], self.num_classes))
    self.b = np.zeros((1, self.num_classes))
    
    for iteration in range(num_iterations):
      for batch in range(0, len(X), batch_size):
        X_batch = X[batch:batch + batch_size]
        y_batch = y[batch:batch + batch_size]
        self.train_batch(X_batch, y_batch)
  
  def train_batch(self, X, y):
    ''' perform gradient descent on batch. contains:
          - forward pass
          - backpropogation

        X -- batch of training data (size batch_size * num_features)
        y -- labels for X (size 1 * batch_size)
    '''

    # forward pass
    P = np.dot(X, self.W) + self.b

    # back-prop
    E = np.exp(P)
    D = E / E.sum(axis=1).reshape((y.size, 1)) # sum over rows, shape

    R = np.arange(y.size)
    Y = np.zeros((y.size, self.num_classes))
    Y[R, y] = 1

    gradient_P = (-Y + D) / len(X)
    gradient_W = np.dot(np.transpose(X), gradient_P)
    gradient_b = gradient_P.sum(axis=0) # sum over columns

    # update
    self.W -= self.learning_rate * gradient_W
    self.b -= self.learning_rate * gradient_b
  
  def predict(self, X):
    ''' predict using best score for all training examples in X

        X -- training dataset
    '''
    return np.argmax(np.dot(X, self.W) + self.b, axis=1)


# testing functions
def train(x_data, y_labels, num_classes, learning_rate=.01, num_iterations=1000):
  softmax = SoftmaxClassifier(num_classes)
  softmax.train(x_data, y_labels, learning_rate=learning_rate,
                num_iterations=num_iterations)

  predictions = softmax.predict(x_data).astype(int)
  results = (predictions == y_labels)
  print "I correclty classify {} / {} of training data!".format(results.sum(), len(x_data))
  return softmax

def test(classifier, test_data, labels):
  predictions = classifier.predict(test_data)
  results = (predictions == labels)
  print "I correctly classify {} / {} of testing data!".format(results.sum(),
  len(test_data))

def main():
  # test 1: linearly separable data
  print "Test 1"
  x_data = np.random.random(1000).reshape(1000, 1)
  labels = (x_data >.5).astype(int).flatten()
  train(x_data, labels, 2)
  print ""

  # test 2: linearly separable 2d data
  print "Test 2"
  x_data = np.random.random(1000)
  y_data = np.random.random(1000)
  labels = ((x_data + y_data) > 1).astype(int)
  X = np.array([x_data,y_data]).T
  train(X, labels, 2)
  print ""

  # test 3: MNIST dataset
  print "Test 3: MNIST Dataset"
  mnist_train, mnist_labels, mnist_test, mnist_test_labels = lm.load_mnist()
  print "Training..."
  classifier = train(mnist_train, mnist_labels, 10, learning_rate = .00001,
              num_iterations=30)
  test(classifier, mnist_test, mnist_test_labels)

if __name__ == "__main__":
  main()