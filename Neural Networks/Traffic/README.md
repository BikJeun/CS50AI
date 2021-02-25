# Traffic

I first made a model based on the one in the lecture. It yielded an extremely low accuracy rate of only 41%.

Afterwhich, i experiemented with more layers and doubling the values:

## RESULTS:
1. Lecture notes model - loss: 2.0792 - accuracy: 0.4122
1. added another convolutional 32 layers - loss: 0.2564 - accuracy: 0.9370
1. added another max pooling layer - loss: 0.0985 - accuracy: 0.9741
1. changed number of hidden layers to 256 - loss: 0.1803 - accuracy: 0.9562
1. added another hidden layer, both 128 layers - loss: 0.1442 - accuracy: 0.9696
1. 2 hidden layers 256 layers - loss: 0.1405 - accuracy: 0.9661 and much slower
1. changed 2nd convolutional layer to 64 - loss: 0.1946 - accuracy: 0.9573
1. change dropout rate to 0.8 - loss: 0.1567 - accuracy: 0.9578

After adding additional convolutional layer, the accuracy sky-rocketed to above 90%.
Best result was obtained when another max pooling layer was added, reaching to 97%.
Though the other test stayed at above 90%, it was unable to be better than the above stated
test.
