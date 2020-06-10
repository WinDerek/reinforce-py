"""
TODO: Update the docs.
"""
import numpy as np


class TwoLayerNet(object):
    def __init__(self, input_size, hidden_size, output_size, std=1e-4, w1=None, b1=None, w2=None, b2=None):
        self.params = {}
        self.params['w1'] = std * np.random.randn(input_size, hidden_size) if w1 is None else w1
        self.params['b1'] = np.zeros(hidden_size) if b1 is None else b1
        self.params['w2'] = std * np.random.randn(hidden_size, output_size) if w2 is None else w2
        self.params['b2'] = np.zeros(output_size) if b2 is None else b2


    def predict(self, X):
        h = np.maximum(0, X.dot(self.params['w1']) + self.params['b1'])
        output = h.dot(self.params['w2']) + self.params['b2']

        return output
    

    def forward(self, X, requires_grad=True, oracle=None, a0=None, clamp=None):
        # Unpack variables from the params dictionary
        w1, b1 = self.params['w1'], self.params['b1']
        w2, b2 = self.params['w2'], self.params['b2']

        h = np.maximum(0, X.dot(w1) + b1)
        output = h.dot(w2) + b2

        if not requires_grad:
            return output

        # Compute gradients
        self.grads = {}
        # dscores = np.zeros(5, dtype=float)
        # dscores[index] = loss

        # td_error, doutput = loss_function(output)
        loss = np.zeros((1, 5), dtype=float)

        td_error = output[0][a0] - oracle

        # Clamp the TD error
        if td_error > clamp:
            td_error = clamp
        elif td_error < -clamp:
            td_error = -clamp
            
        loss[0][a0] = td_error

        doutput = loss

        # print(doutput.shape)
        # print(h.shape)
        # print(h.T.shape)
        self.grads['w2'] = h.T.dot(doutput)
        self.grads['b2'] = np.sum(doutput, axis=0)
        
        dh = doutput.dot(w2.T)
        dh_relu = (h > 0) * dh
        self.grads['w1'] = X.T.dot(dh_relu)
        self.grads['b1'] = np.sum(dh_relu, axis=0)

        return td_error


    # TODO: learning rate decay logic
    def backward(self, learning_rate=1e-2, learning_rate_decay=0.95):
        self.params['w2'] += - learning_rate * self.grads['w2']
        self.params['b2'] += - learning_rate * self.grads['b2']
        self.params['w1'] += - learning_rate * self.grads['w1']
        self.params['b1'] += - learning_rate * self.grads['b1']

        return { 'w1': self.params['w1'].tolist(), 'b1': self.params['b1'].tolist(), 'w2': self.params['w2'].tolist(), 'b2': self.params['b2'].tolist() }
