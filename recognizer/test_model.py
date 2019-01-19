from model import stop_sign_recognizer
from torchvision import datasets, transforms
import os
import torch


if __name__ == "__main__":
    model = stop_sign_recognizer()
    model.load("saved_model.save")
    
    # Print the model we just instantiated
    print(f'Model created, input size is : {model.input_size}')

    result = model.stop_sign_or_not("data\\train\\stop_sign\\2.jpg")
