from model import stop_sign_recognizer
from torchvision import datasets, transforms
import os
import torch


if __name__ == "__main__":
    model = stop_sign_recognizer()
    model.load()
    
    # Print the model we just instantiated
    print(f'Model created, input size is : {model.input_size}')

    result = model.stop_sign_or_not(["data\\train\\no_stop_sign\\1.jpg",
                                    "data\\train\\no_stop_sign\\2.jpg",
                                    "data\\train\\no_stop_sign\\3.jpg",
                                    "data\\train\\no_stop_sign\\4.jpg",
                                    "data\\train\\no_stop_sign\\6.jpg",
                                    "data\\train\\no_stop_sign\\8.jpg",
                                    "data\\train\\no_stop_sign\\9.jpg",
                                    "data\\train\\no_stop_sign\\10.jpg",
                                    "data\\train\\no_stop_sign\\11.jpg"])
