"""
Programmed by Behnaaz Fakhar <fakhar.behnaz@gmail.com>
*    2019-04-28 Initial coding

"""

import numpy as np
import matplotlib.pyplot as plt

class LogisticRegression:
  """
  Logistic regression classifier.

  Parameters:
  -----------
  learning_rate : float, default=0.01
      Learning rate for gradient descent optimization.

  max_iteration : int, default=1000
      Maximum number of iterations for gradient descent.

  threshold : float, default=0.5
      Threshold for class prediction.

  Attributes:
  -----------
  weights : numpy.ndarray
      Coefficients for the features.

  bias : float
      Intercept.

  Methods:
  --------
  sigmoid(Z: numpy.ndarray) -> numpy.ndarray:
      Sigmoid activation function.

  fit(X_train: numpy.ndarray, y_true: numpy.ndarray) -> None:
      Fit the logistic regression model to the training data.

  predict(X_test: numpy.ndarray) -> numpy.ndarray:
      Predict class labels for test data.

  """
  def __init__(self, learning_rate=0.01, max_iteration=1000, patience = None, threshold=0.5):
      self.weights = None
      self.bias = None
      self.threshold = threshold
      self.learning_rate = learning_rate
      self.max_iteration = max_iteration
      self.patience = patience

  @staticmethod
  def sigmoid(Z: np.ndarray) -> np.ndarray:
      """
      Sigmoid activation function.

      Parameters:
      -----------
      Z : numpy.ndarray
          Input to the sigmoid function.

      Returns:
      --------
      numpy.ndarray
          Output of the sigmoid function.
      """
      return 1 / (1 + np.exp(-Z))

  def fit(self, X_train: np.ndarray, y_train: np.ndarray, X_val=None, y_val=None, patience=None, print_loss = True, plot_loss=True):
    """
    Fit the logistic regression model to the training data with early stopping.

    Parameters:
    -----------
    X_train : numpy.ndarray
      Training input samples.

    y_train : numpy.ndarray
      Target values for training.

    X_val : numpy.ndarray, optional
      Validation input samples.

    y_val : numpy.ndarray, optional
      Target values for validation.

    patience : int, optional
      Number of iterations to wait for improvement on the validation loss before stopping early.

    Returns:
    --------
    None
    """
    num_samples, num_features = X_train.shape
    self.weights = np.zeros(num_features)
    self.bias = 0

    train_losses = []  # Store training losses for plotting
    val_losses = [] if (X_val is not None and y_val is not None) else None   # Store validation losses for plotting

    best_loss = float('inf')
    no_improvement_count = 0

    for i in range(self.max_iteration):
      Z = np.dot(X_train, self.weights) + self.bias
      y_pred = self.sigmoid(Z)
      log_loss = -(np.multiply(y_train, np.log(y_pred)) + np.multiply((1 - y_train), np.log(1 - y_pred)))
      loss = np.mean(log_loss)

      if print_loss and i % 100 == 0:
        print ("Loss after iteration %i: %f" %(i, loss))
        train_losses.append(loss)  # Append training loss

      # Calculate validation loss if validation data provided
      if X_val is not None and y_val is not None:
          Z_val = np.dot(X_val, self.weights) + self.bias
          y_pred_val = self.sigmoid(Z_val)
          log_loss_val = -(np.multiply(y_val, np.log(y_pred_val)) + np.multiply((1 - y_val), np.log(1 - y_pred_val)))
          val_loss = np.mean(log_loss_val)
          if print_loss and i % 100 == 0:
            val_losses.append(val_loss)  # Append validation loss

          # Check for improvement in validation loss
          if val_loss < best_loss:
              best_loss = val_loss
              no_improvement_count = 0
          else:
              no_improvement_count += 1

          # If no improvement for 'patience' iterations, stop training
          if patience and no_improvement_count >= patience:
              print(f"Stopped early at iteration {i+1} due to no improvement in validation loss.")
              break

      # Gradient Descend
      dw = (1 / num_samples) * (np.dot(X_train.T, (y_pred - y_train)))
      db = (1 / num_samples) * (np.sum(y_pred - y_train))

      self.weights -= self.learning_rate * dw
      self.bias -= self.learning_rate * db

    if plot_loss:
        # Plot the training and validation losses
        plt.plot(train_losses, label='Training Loss')
        plt.title('Training Loss')
        if X_val is not None and y_val is not None:
            plt.plot(val_losses, label='Validation Loss')
            plt.title('Training and Validation Loss')
        plt.xlabel('Iteration')
        plt.ylabel('Loss')
        plt.legend()
        plt.show()

  def predict(self, X_test: np.ndarray) -> np.ndarray:
    """
    Predict class labels for test data.

    Parameters:
    -----------
    X_test : numpy.ndarray
        Test input samples.

    Returns:
    --------
    numpy.ndarray
        Predicted class labels.
    """
    Z = np.dot(X_test, self.weights) + self.bias
    y_pred = self.sigmoid(Z)
    y_pred_cls = [1 if i > self.threshold else 0 for i in y_pred]
    return np.array(y_pred_cls)
