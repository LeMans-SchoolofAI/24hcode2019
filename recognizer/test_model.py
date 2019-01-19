from model import stop_sign_recognizer
from torchvision import datasets, transforms
import os
import torch


if __name__ == "__main__":
    model = stop_sign_recognizer()
    
    # Print the model we just instantiated
    print(f'Model created, input size is : {model.input_size}')

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

    # Set the model to evaluation mode
    model.set_eval()
    model.send_to_gpu()

    # Run the model on validation inputs
    for inputs, _ in dataloaders_dict['val']:
        outputs = model.model(inputs)
        #print(f'inputs = {inputs}')
        print(f'outputs = {outputs}')
