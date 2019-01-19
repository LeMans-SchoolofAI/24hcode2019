from model import stop_sign_recognizer
from torchvision import datasets, transforms
import os
import torch
import torch.nn as nn
import torch.optim as optim

# Number of epochs to train for 
NUM_EPOCHS = 15

if __name__ == "__main__":
    model = stop_sign_recognizer()
    
    # Print the model we just instantiated
    print(f'Model created, input size is : {model.input_size}')

    # Data augmentation and normalization for training
    # Just normalization for validation
    data_transforms = {
        'train': transforms.Compose([
            transforms.RandomResizedCrop(model.input_size),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            transforms.Resize(model.input_size),
            transforms.CenterCrop(model.input_size),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }

    print("Initializing Datasets and Dataloaders...")

    # Create training and validation datasets
    image_datasets = {x: datasets.ImageFolder(os.path.join(model.data_dir, x), data_transforms[x]) for x in ['train', 'val']}
    # Create training and validation dataloaders
    dataloaders_dict = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=model.batch_size, shuffle=True, num_workers=4) for x in ['train', 'val']}


    # Gather the parameters to be optimized/updated in this run. If we are
    #  finetuning we will be updating all parameters. However, if we are 
    #  doing feature extract method, we will only update the parameters
    #  that we have just initialized, i.e. the parameters with requires_grad
    #  is True.
    params_to_update = model.model.parameters()
    print("Params to learn:")
    if model.feature_extract:
        params_to_update = []
        for name,param in model.model.named_parameters():
            if param.requires_grad == True:
                params_to_update.append(param)
                print("\t",name)
    else:
        for name,param in model_ft.named_parameters():
            if param.requires_grad == True:
                print("\t",name)

    # Observe that all parameters are being optimized
    optimizer_ft = optim.SGD(params_to_update, lr=0.001, momentum=0.9)

    # Setup the loss fxn
    criterion = nn.CrossEntropyLoss()

    # Train and evaluate
    model_ft, hist = model.train_model(dataloaders_dict, criterion, optimizer_ft, num_epochs=NUM_EPOCHS)

    # Save model
    model.save()
