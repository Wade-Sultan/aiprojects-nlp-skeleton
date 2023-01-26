import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm


def starting_train(train_dataset, val_dataset, model, hyperparameters, n_eval):
    """
    Trains and evaluates a model.

    Args:
        train_dataset:   PyTorch dataset containing training data.
        val_dataset:     PyTorch dataset containing validation data.
        model:           PyTorch model to be trained.
        hyperparameters: Dictionary containing hyperparameters.
        n_eval:          Interval at which we evaluate our model.
    """

    # Get keyword arguments
    batch_size, epochs = hyperparameters["batch_size"], hyperparameters["epochs"]

    # Initialize dataloaders
    train_loader = torch.utils.data.DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True
    )
    val_loader = torch.utils.data.DataLoader(
        val_dataset, batch_size=batch_size, shuffle=True
    )

    # Initalize optimizer (for gradient descent) and loss function
    optimizer = optim.Adam(model.parameters())
    loss_fn = nn.BCEWithLogitsLoss()

    step = 0
    for epoch in range(epochs):
        print(f"Epoch {epoch + 1} of {epochs}")

        # Loop over each batch in the dataset
        for batch in tqdm(train_loader):
            inputs, labels = batch

            # TODO: Forward propagate
            outputs = model(inputs).squeeze()

            print(labels.shape)
            print(type(labels[0]))
            # TODO: Backpropagation and gradient descent
            loss = loss_fn(outputs, labels.float())
            loss.backward()       # Compute gradients
            optimizer.step()      # Update all the weights with the gradients you just calculated
            optimizer.zero_grad() # Clear gradients before next iteration

            # Periodically evaluate our model + log to Tensorboard
            if step % n_eval == 0:
                model.eval()
                # TODO:
                # Compute training loss and accuracy.
                # Log the results to Tensorboard.
                compute_accuracy(outputs, labels)
                ### Log results

                # TODO:
                # Compute validation loss and accuracy.
                # Log the results to Tensorboard. 
                # Don't forget to turn off gradient calculations!
                evaluate(val_loader, model, loss_fn)
                model.train()

            step += 1

        print()


def compute_accuracy(outputs, labels):
    """
    Computes the accuracy of a model's predictions.

    Example input:
        outputs: [0.7, 0.9, 0.3, 0.2]
        labels:  [1, 1, 0, 1]

    Example output:
        0.75
    """

    n_correct = (torch.round(outputs) == labels).sum().item()
    n_total = len(outputs)
    return n_correct / n_total


def evaluate(val_loader, model, loss_fn):
    """
    Computes the loss and accuracy of a model on the validation dataset.
    """
    pass
    with torch.no_grad():
        for batch in tqdm(val_loader):
            inputs, labels = batch
            
            output = model(inputs)

            prediction = output.item()

            print(compute_accuracy(prediction, labels))
            
            # if prediction > 0.5:
            #     print(f'{prediction:0.3}: Positive sentiment')
            # else:
            #     print(f'{prediction:0.3}: Negative sentiment')
