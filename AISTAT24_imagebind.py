from imagebind import data
import torch
from imagebind.models import imagebind_model
from imagebind.models.imagebind_model import ModalityType


import glob
import os
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns


text_list=['tench',
 'English springer',
 'cassette player',
 'chain saw',
 'church',
 'French horn',
 'garbage truck',
 'gas pump',
 'golf ball',
 'parachute']




root = '/home/montasir/Desktop/Montasir/Fall 2023/Research and Experiments/imagenette2/val/'


all_class_dirs = sorted(glob.glob(os.path.join(root, '*')))

device = "cpu"
#threshold = 0.80
class_results = {}

class_labels = text_list



def process_data(all_class_dirs,text_list,device):
    for class_index, class_dir in enumerate(all_class_dirs):
        actual_label = text_list[class_index]  
    
        image_paths = glob.glob(os.path.join(class_dir, '*.JPEG'))
    
        if len(image_paths) >= 50:
            image_paths = image_paths[:50]

    # Load data
        inputs = {
            ModalityType.TEXT: data.load_and_transform_text(text_list, device),
            ModalityType.VISION: data.load_and_transform_vision_data(image_paths, device)
        }
    return inputs




def calculate_confusion_matrix(class_labels, all_class_dirs, device):
    n = len(class_labels)
    conf_matrix = np.zeros((n, n), dtype=int)

    for class_index, class_dir in enumerate(all_class_dirs):
        actual_label = class_labels[class_index]

        inputs = process_data(class_dir, class_labels, device)

        with torch.no_grad():
            embeddings = model(inputs)

        sm_score = torch.softmax(embeddings[ModalityType.VISION] @ embeddings[ModalityType.TEXT].T, dim=-1)

        for i in range(len(inputs[ModalityType.VISION])):
            predicted_index = sm_score[i].argmax().item()
            predicted_label = class_labels[predicted_index]

            if predicted_label == actual_label:
                conf_matrix[class_index][predicted_index] += 1
            else:
                inc = class_labels.index(predicted_label)
                conf_matrix[class_index][inc] += 1

    return conf_matrix
    
    
    
    def plot_confusion_matrix(conf_matrix, class_labels):
        plt.figure(figsize=(10, 8))
        sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_labels, yticklabels=class_labels)
        plt.xlabel('Predicted', fontsize=14)
        plt.ylabel('Actual', fontsize=14)
        plt.title('Confusion Matrix', fontsize=16)
        plt.show()
