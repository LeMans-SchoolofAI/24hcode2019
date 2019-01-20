from model import stop_sign_recognizer
from torchvision import datasets, transforms
import os
import torch
import argparse

DEFAULT_TEST_FILE = "data\\val\\stop_sign\\70.jpg"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default=DEFAULT_TEST_FILE,
                        help='Image file to evaluate.')
    args = parser.parse_args()
    filename = args.file

    model = stop_sign_recognizer(use_gpu=True)
    model.load()
    
    result = model.stop_sign_or_not([filename])
    if result[0]:
        print(f'{filename} has a stop sign.')
    else:
        print(f'{filename} does not have a stop sign.')
