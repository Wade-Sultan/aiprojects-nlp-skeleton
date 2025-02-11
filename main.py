import os
import torch
import constants
from data.LSTMDataset import LSTMDataset
from networks.LSTMNetwork import LSTMNetwork
from data.StartingDataset import StartingDataset
from data.ValDataset import ValidationDataset
from networks.StartingNetwork import StartingNetwork
from train_functions.starting_train import starting_train


def main():
    # Get command line arguments
    hyperparameters = {"epochs": constants.EPOCHS, "batch_size": constants.BATCH_SIZE}

    # TODO: Add GPU support. This line of code might be helpful.
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print("Epochs:", constants.EPOCHS)
    print("Batch size:", constants.BATCH_SIZE)

    # Initalize dataset and model. Then train the model!
    data_path = "train_80.csv" #TODO: make sure you have train.csv downloaded in your project! this assumes it is in the project's root directory (ie the same directory as main) but you can change this as you please
    data_path_val = "train_val_20.csv"

    # train_dataset = StartingDataset(data_path)
    # val_dataset = ValidationDataset(data_path_val)
    # model = StartingNetwork()
    # starting_train(
    #     train_dataset=train_dataset,
    #     val_dataset=val_dataset,
    #     model=model,
    #     hyperparameters=hyperparameters,
    #     n_eval=constants.N_EVAL,
    # )

    
    train_dataset = LSTMDataset(data_path, "train_glove.csv")
    val_dataset = LSTMDataset(data_path_val, "val_glove.csv")
    model = LSTMNetwork(train_dataset.getEmbs())
    starting_train(
        train_dataset=train_dataset,
        val_dataset=val_dataset,
        model=model,
        hyperparameters=hyperparameters,
        n_eval=constants.N_EVAL,
    )


if __name__ == "__main__":
    main()
