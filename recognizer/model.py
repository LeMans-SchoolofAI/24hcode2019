"""
Finetuned model for recognizing if a photo has a stop sign in it or not

Greatly inspired from https://pytorch.org/tutorials/beginner/finetuning_torchvision_models_tutorial.html

"""

from __future__ import print_function 
from __future__ import division
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import time
import os
import copy
from PIL import Image


# Top level data directory. Here we assume the format of the directory conforms 
#   to the ImageFolder structure
DATA_DIR = "./data"
# Models to choose from [resnet, alexnet, vgg, squeezenet, densenet, inception]
MODEL_NAME = "squeezenet"
# Number of classes in the dataset
NUM_CLASSES = 2
# Batch size for training (change depending on how much memory you have)
BATCH_SIZE = 8
# Flag for feature extracting. When False, we finetune the whole model, 
#   when True we only update the reshaped layer params
FEATURE_EXTRACT = True
# Default file for saved model
DEFAULT_FILE = "saved_model.save"

class stop_sign_recognizer(object):
    def __init__(self, use_gpu = False):
        self.data_dir = DATA_DIR
        self.model_name = MODEL_NAME
        self.is_inception = (self.model_name=="inception")
        self.num_classes = NUM_CLASSES
        self.batch_size = BATCH_SIZE
        self.feature_extract = FEATURE_EXTRACT
        self.model, self.input_size = self.__initialize_model__(use_pretrained=True)
        if use_gpu:
            self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
            self.model = self.model.to(self.device)
        else:
            self.device = "cpu"

    def save(self, path=DEFAULT_FILE):
        torch.save(self.model.state_dict(), path)

    def load(self, path=DEFAULT_FILE):
        self.model.load_state_dict(torch.load(path))

    def set_eval(self):
        # Set the model in eval mode
        self.model.eval()
    
    def train_model(self, dataloaders, criterion, optimizer, num_epochs=25):
        since = time.time()

        val_acc_history = []
        
        best_model_wts = copy.deepcopy(self.model.state_dict())
        best_acc = 0.0

        for epoch in range(num_epochs):
            print('Epoch {}/{}'.format(epoch, num_epochs - 1))
            print('-' * 10)

            # Each epoch has a training and validation phase
            for phase in ['train', 'val']:
                if phase == 'train':
                    self.model.train()  # Set model to training mode
                else:
                    self.model.eval()   # Set model to evaluate mode

                running_loss = 0.0
                running_corrects = 0

                # Iterate over data.
                for inputs, labels in dataloaders[phase]:
                    inputs = inputs.to(self.device)
                    labels = labels.to(self.device)

                    # zero the parameter gradients
                    optimizer.zero_grad()

                    # forward
                    # track history if only in train
                    with torch.set_grad_enabled(phase == 'train'):
                        # Get model outputs and calculate loss
                        # Special case for inception because in training it has an auxiliary output. In train
                        #   mode we calculate the loss by summing the final output and the auxiliary output
                        #   but in testing we only consider the final output.
                        if self.is_inception and phase == 'train':
                            # From https://discuss.pytorch.org/t/how-to-optimize-inception-model-with-auxiliary-classifiers/7958
                            outputs, aux_outputs = self.model(inputs)
                            loss1 = criterion(outputs, labels)
                            loss2 = criterion(aux_outputs, labels)
                            loss = loss1 + 0.4*loss2
                        else:
                            outputs = self.model(inputs)
                            loss = criterion(outputs, labels)

                        _, preds = torch.max(outputs, 1)

                        # backward + optimize only if in training phase
                        if phase == 'train':
                            loss.backward()
                            optimizer.step()

                    # statistics
                    running_loss += loss.item() * inputs.size(0)
                    running_corrects += torch.sum(preds == labels.data)

                epoch_loss = running_loss / len(dataloaders[phase].dataset)
                epoch_acc = running_corrects.double() / len(dataloaders[phase].dataset)

                print('{} Loss: {:.4f} Acc: {:.4f}'.format(phase, epoch_loss, epoch_acc))

                # deep copy the model
                if phase == 'val' and epoch_acc > best_acc:
                    best_acc = epoch_acc
                    best_model_wts = copy.deepcopy(self.model.state_dict())
                if phase == 'val':
                    val_acc_history.append(epoch_acc)

            print()

        time_elapsed = time.time() - since
        print('Training complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
        print('Best val Acc: {:4f}'.format(best_acc))

        # load best model weights
        self.model.load_state_dict(best_model_wts)
        return self.model, val_acc_history


    ######################################################################
    # Set Model Parameters’ .requires_grad attribute
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # 
    # This helper function sets the ``.requires_grad`` attribute of the
    # parameters in the model to False when we are feature extracting. By
    # default, when we load a pretrained model all of the parameters have
    # ``.requires_grad=True``, which is fine if we are training from scratch
    # or finetuning. However, if we are feature extracting and only want to
    # compute gradients for the newly initialized layer then we want all of
    # the other parameters to not require gradients. This will make more sense
    # later.
    # 

    @staticmethod
    def set_parameter_requires_grad(model, feature_extracting):
        if feature_extracting:
            for param in model.parameters():
                param.requires_grad = False


    def __initialize_model__(self, use_pretrained=True):
        # Initialize these variables which will be set in this if statement. Each of these
        #   variables is model specific.
        model_ft = None
        input_size = 0

        if self.model_name == "resnet":
            """ Resnet18
            """
            model_ft = models.resnet18(pretrained=use_pretrained)
            self.set_parameter_requires_grad(model_ft, self.feature_extract)
            num_ftrs = model_ft.fc.in_features
            model_ft.fc = nn.Linear(num_ftrs, self.num_classes)
            input_size = 224

        elif self.model_name == "alexnet":
            """ Alexnet
            """
            model_ft = models.alexnet(pretrained=use_pretrained)
            self.set_parameter_requires_grad(model_ft, self.feature_extract)
            num_ftrs = model_ft.classifier[6].in_features
            model_ft.classifier[6] = nn.Linear(num_ftrs, self.num_classes)
            input_size = 224

        elif self.model_name == "vgg":
            """ VGG11_bn
            """
            model_ft = models.vgg11_bn(pretrained=use_pretrained)
            self.set_parameter_requires_grad(model_ft, self.feature_extract)
            num_ftrs = model_ft.classifier[6].in_features
            model_ft.classifier[6] = nn.Linear(num_ftrs, self.num_classes)
            input_size = 224

        elif self.model_name == "squeezenet":
            """ Squeezenet
            """
            model_ft = models.squeezenet1_0(pretrained=use_pretrained)
            self.set_parameter_requires_grad(model_ft, self.feature_extract)
            model_ft.classifier[1] = nn.Conv2d(512, self.num_classes, kernel_size=(1,1), stride=(1,1))
            model_ft.num_classes = self.num_classes
            input_size = 224

        elif self.model_name == "densenet":
            """ Densenet
            """
            model_ft = models.densenet121(pretrained=use_pretrained)
            self.set_parameter_requires_grad(model_ft, self.feature_extract)
            num_ftrs = model_ft.classifier.in_features
            model_ft.classifier = nn.Linear(num_ftrs, self.num_classes) 
            input_size = 224

        elif self.model_name == "inception":
            """ Inception v3 
            Be careful, expects (299,299) sized images and has auxiliary output
            """
            model_ft = models.inception_v3(pretrained=use_pretrained)
            self.set_parameter_requires_grad(model_ft, self.feature_extract)
            # Handle the auxilary net
            num_ftrs = model_ft.AuxLogits.fc.in_features
            model_ft.AuxLogits.fc = nn.Linear(num_ftrs, self.num_classes)
            # Handle the primary net
            num_ftrs = model_ft.fc.in_features
            model_ft.fc = nn.Linear(num_ftrs, self.num_classes)
            input_size = 299

        else:
            print("Invalid model name, exiting...")
            exit()
        
        return model_ft, input_size


    def stop_sign_or_not(self, photos):
        """
        Analyse a list of images and return if there is a stop sign or not in each
        Parameters
        ----------
        photos :a list of images' path
        Returns
        -------
        a list of float (one for each image from input) : confidence that there is a stop sign (1 : yes, 0 : no)
        """
        data_transforms = transforms.Compose([  transforms.Resize(self.input_size),
                                                transforms.CenterCrop(self.input_size),
                                                transforms.ToTensor(),
                                                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
                                            ])

        results = []
        for i in range(0, len(photos), self.batch_size):
            if i + self.batch_size > len(photos):
                photo_batch = photos[i:]
            else:
                photo_batch = photos[i:i + self.batch_size]

            photo_batch_tensor = [data_transforms(Image.open(x)) for x in photo_batch]

            # Check tensor shape (some images can have more than 3 channels for example)
            for a in photo_batch_tensor:
                if a.shape != torch.Size([3, 224, 224]):
                    raise Exception(f'Invalid image file : {a.shape}')
            
            photo_batch_tensor = torch.stack(photo_batch_tensor)
            photo_batch_tensor = photo_batch_tensor.to(self.device)
            outputs = self.model(photo_batch_tensor)
            _, preds = torch.max(outputs, 1)
            results += preds.tolist()
        return results
