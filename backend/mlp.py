"""
TODO: Update the docs.
"""
import numpy as np


class TwoLayerNet(object):
  def __init__(self, input_size, hidden_size, output_size, std=1e-4, w1=None, b1=None, w2=None, b2=None):
    self.params = {}
    self.params['W1'] = std * np.random.randn(input_size, hidden_size) if w1 is None else w1
    self.params['b1'] = np.zeros(hidden_size) if b1 is None else b1
    self.params['W2'] = std * np.random.randn(hidden_size, output_size) if w2 is None else w2
    self.params['b2'] = np.zeros(output_size) if b2 is None else b2


  def forward(self, X):
    h = np.maximum(0, X.dot(self.params['W1']) + self.params['b1'])
    scores = h.dot(self.params['W2']) + self.params['b2']

    return scores


  def backward(self, X, loss, index):
    # Unpack variables from the params dictionary
    W1, b1 = self.params['W1'], self.params['b1']
    W2, b2 = self.params['W2'], self.params['b2']
    N, D = X.shape

    # # Compute the forward pass
    # scores = None
    # h_output = np.maximum(0, X.dot(W1) + b1)
    # scores = h_output.dot(W2) + b2

    # Compute the loss
    # loss = None
    # shift_scores = scores - np.max(scores, axis = 1).reshape(-1,1)
    # softmax_output = np.exp(shift_scores)/np.sum(np.exp(shift_scores), axis = 1).reshape(-1,1)
    # loss = -np.sum(np.log(softmax_output[range(N), list(y)]))
    # loss /= N

    # Compute gradients
    grads = {}
    # dscores = softmax_output.copy()
    # dscores[range(N), list(y)] -= 1
    # dscores /= N
    dscores = np.zeros(5, dtype=float)
    dscores[index] = loss
    grads['W2'] = h_output.T.dot(dscores)
    grads['b2'] = np.sum(dscores, axis = 0)
    
    dh = dscores.dot(W2.T)
    dh_ReLu = (h_output > 0) * dh
    grads['W1'] = X.T.dot(dh_ReLu)
    grads['b1'] = np.sum(dh_ReLu, axis = 0)

    return loss, grads
