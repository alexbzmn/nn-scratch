import numpy as np
from sklearn import datasets, linear_model
import matplotlib.pyplot as plt


# http://www.wildml.com/2015/09/implementing-a-neural-network-from-scratch/

def plot_decision_boundary(pred_func, X, y):
    # Set min and max values and give it some padding
    x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
    y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
    h = 0.01

    # Generate a grid of points with distance h between them
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    # Predict the function value for the whole gid
    Z = pred_func(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    # Plot the contour and training examples
    plt.contourf(xx, yy, Z, cmap=plt.cm.Spectral)
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Spectral)
    plt.show()


# Helper function to evaluate the total loss on the dataset
def calculate_loss(model):
    W1, b1, W2, b2, W3, b3 = model['W1'], model['b1'], model['W2'], model['b2'], model['W3'], model['b3']
    # Forward propagation to calculate our predictions

    z1 = X.dot(W1) + b1
    a1 = sigmoid(z1)

    z2 = a1.dot(W2) + b2
    a2 = sigmoid(z2)

    z3 = a2.dot(W3) + b3
    a3 = softmax(z3)

    # Calculating the loss
    corect_logprobs = -np.log(a3[range(num_examples), y])
    data_loss = np.sum(corect_logprobs)

    # Add regulatization term to loss (optional)
    data_loss += reg_lambda / 2 * (np.sum(np.square(W1)) + np.sum(np.square(W2) + np.sum(np.square(W3))))
    return 1. / num_examples * data_loss


# Helper function to predict an output (0 or 1)
def predict(model, x):
    W1, b1, W2, b2, W3, b3 = model['W1'], model['b1'], model['W2'], model['b2'], model['W3'], model['b3']
    # Forward propagation to calculate our predictions

    z1 = x.dot(W1) + b1
    a1 = sigmoid(z1)

    z2 = a1.dot(W2) + b2
    a2 = sigmoid(z2)

    z3 = a2.dot(W3) + b3
    a3 = softmax(z3)

    return np.argmax(a3, axis=1)


def softmax(z):
    exponent = np.exp(z)
    return exponent / np.sum(exponent, axis=1, keepdims=True)


def relu(x):
    return np.maximum(0, x)


def d_relu(x):
    derivative = np.zeros(x.shape)
    derivative[np.where(x > 0)] = 1
    return derivative


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def d_sigmoid(x):
    return (1 - x) * x


# This function learns parameters for the neural network and returns the model.
# - nn_hdim: Number of nodes in the hidden layer
# - num_passes: Number of passes through the training data for gradient descent
# - print_loss: If True, print the loss every 1000 iterations
def build_model(nn_hdim, num_passes=40000, print_loss=False):
    # Initialize the parameters to random values. We need to learn these.
    np.random.seed(0)

    W1 = np.random.randn(nn_input_dim, nn_hdim) / np.sqrt(nn_input_dim)
    b1 = np.zeros((1, nn_hdim))

    W2 = np.random.randn(nn_hdim, nn_hdim) / np.sqrt(nn_hdim)
    b2 = np.zeros((1, nn_hdim))

    W3 = np.random.randn(nn_hdim, nn_output_dim) / np.sqrt(nn_hdim)
    b3 = np.zeros((1, nn_output_dim))

    # This is what we return at the end
    model = {}

    # Gradient descent. For each batch...
    for i in range(0, num_passes):

        # Forward propagation
        z1 = X.dot(W1) + b1
        a1 = sigmoid(z1)

        z2 = a1.dot(W2) + b2
        a2 = sigmoid(z2)

        z3 = a2.dot(W3) + b3
        a3 = softmax(z3)

        # Backpropagation
        delta4 = a3
        delta4[range(num_examples), y] -= 1
        # todo something wrong here
        dW3 = (a1.T).dot(delta4)
        db3 = np.sum(delta4, axis=0, keepdims=True)

        delta3 = d_sigmoid(a1) * delta4.dot(W3.T)
        dW2 = (a2.T).dot(delta3)
        db2 = np.sum(delta3, axis=0, keepdims=True)

        delta2 = d_sigmoid(a2) * delta3.dot(W2.T)
        dW1 = np.dot(X.T, delta2)
        db1 = np.sum(delta2, axis=0)

        # Add regularization terms (b1 and B3 don't have regularization terms)
        dW3 += reg_lambda * W3
        dW2 += reg_lambda * W2
        dW1 += reg_lambda * W1

        # Gradient descent parameter update
        W1 += -epsilon * dW1
        b1 += -epsilon * db1
        W2 += -epsilon * dW2
        b2 += -epsilon * db2
        W3 += -epsilon * dW3
        b3 += -epsilon * db3

        # Assign new parameters to the model
        model = {'W1': W1, 'b1': b1, 'W2': W2, 'b2': b2, 'W3': W3, 'b3': b3}

        # Optionally print the loss.
        # This is expensive because it uses the whole dataset, so we don't want to do it too often.
        if print_loss and i % 1000 == 0:
            print("Loss after iteration %i: %f" % (i, calculate_loss(model)))

    return model


np.random.seed(0)

X, y = datasets.make_moons(200, noise=0.20)

# plt.scatter(X[:, 0], X[:, 1], s=40, c=y, cmap=plt.cm.Spectral)

num_examples = len(X)  # training set size
nn_input_dim = 2  # input layer dimensionality
nn_output_dim = 2  # output layer dimensionality

# Gradient descent parameters (I picked these by hand)
epsilon = 0.01  # learning rate for gradient descent
reg_lambda = 0.01  # regularization strength

# Build a model with a 3-dimensional hidden layer
model = build_model(6, print_loss=True)

# Plot the decision boundary
plot_decision_boundary(lambda x: predict(model, x), X, y)
plt.title("Decision Boundary for hidden layer size 3")

plt.show()
