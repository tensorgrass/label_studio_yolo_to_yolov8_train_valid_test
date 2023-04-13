import os
from pathlib import Path, PurePath, PurePosixPath
import shutil

from icecream import ic
import random
import yaml
import json

INDENTATION = 2

TRAIN_DIRECTORY = r"train"
VALID_DIRECTORY = r"valid"
TEST_DIRECTORY = r"test"
IMAGES_DIRECTORY = r"images"
LABELS_DIRECTORY = r"labels"


def convert(path_source_raw, path_destination_raw, path_google_collab_raw, perc_train=70, perc_valid=20, perc_test=10):
    # Starting with the file resulting from label-studio annotated images with YOLO, it is converted to YOLOv8.
    # The images are separated into three folders (train, valid, test) based on their percentage.
    # The general YOLO configuration file is converted to YOLOv8.

    path_source = Path(path_source_raw)
    path_destination = Path(path_destination_raw)
    path_google_collab = PurePosixPath(path_google_collab_raw)
    # Create directories
    path_dst_with_number = \
        create_destination_directory(path_destination)
    dst_train_images_path, dst_train_labels_path = \
        create_destination_subdirectory(path_dst_with_number, TRAIN_DIRECTORY)
    dst_valid_images_path, dst_valid_labels_path = \
        create_destination_subdirectory(path_dst_with_number, VALID_DIRECTORY)
    dst_test_images_path, dst_test_labels_path = \
        create_destination_subdirectory(path_dst_with_number, TEST_DIRECTORY)

    # Copy images
    org_images_path = path_source / IMAGES_DIRECTORY
    org_labels_path = path_source / LABELS_DIRECTORY
    name_images_test, name_images_train, name_images_valid = \
        get_name_images_by_type(org_images_path, perc_test, perc_train, perc_valid)
    copy_images_to(name_images_train, dst_train_images_path, dst_train_labels_path, org_images_path, org_labels_path)
    copy_images_to(name_images_valid, dst_valid_images_path, dst_valid_labels_path, org_images_path, org_labels_path)
    copy_images_to(name_images_test, dst_test_images_path, dst_test_labels_path, org_images_path, org_labels_path)

    convert_label_studio_yolo_to_roboflow_yolov8(path_dst_with_number, path_source, path_google_collab)


def create_destination_directory(path_destination):
    num_path_dst = 0;
    path_dst_with_number = path_destination
    while os.path.exists(path_dst_with_number):
        num_path_dst += 1
        path_dst_with_number = path_destination.parent / f"{path_destination.name}_{num_path_dst:02}"
    os.makedirs(path_dst_with_number)
    return path_dst_with_number


def create_destination_subdirectory(path_dst_with_number, type_directory):
    dst_train_path = path_dst_with_number / type_directory
    dst_train_images_path = dst_train_path / IMAGES_DIRECTORY
    dst_train_labels_path = dst_train_path / LABELS_DIRECTORY
    os.makedirs(dst_train_path)
    os.makedirs(dst_train_images_path)
    os.makedirs(dst_train_labels_path)
    return dst_train_images_path, dst_train_labels_path


def get_name_images_by_type(org_images_path, perc_test, perc_train, perc_valid):
    name_images = [f for f in os.listdir(org_images_path) if os.path.isfile(os.path.join(org_images_path, f))]
    total_images = len(name_images)
    random.shuffle(name_images)
    perc_train_val = int(perc_train * total_images / 100)
    perc_valid_val = int(perc_valid * total_images / 100)
    perc_test_val = int(perc_test * total_images / 100)
    name_images_test = name_images[0:perc_test_val]
    name_images_valid = name_images[perc_test_val: perc_test_val + perc_valid_val]
    name_images_train = name_images[perc_test_val + perc_valid_val: total_images]
    ic(len(name_images))
    ic(len(name_images_test) + len(name_images_valid) + len(name_images_train))
    return name_images_test, name_images_train, name_images_valid


def copy_images_to(name_images, dst_images_path, dst_labels_path, org_images_path, org_labels_path):
    for image_name in name_images:
        ic(dst_images_path)
        path_image = org_images_path / image_name
        ic(path_image)
        path_label = org_labels_path / image_name.replace('.jpg', '.txt');
        ic(path_label)
        shutil.copy(path_image, dst_images_path)
        shutil.copy(path_label, dst_labels_path)

def convert_label_studio_yolo_to_roboflow_yolov8(path_dst_with_number, path_source, path_google_collab):
    # Read json
    path_json = path_source / f"notes.json"
    file_json = open(path_json)
    data = json.load(file_json)
    labels = []
    for category in data['categories']:
        ic(category)
        labels.append({category["id"]: category["name"]})
    ic(labels)

    # Create data.yaml
    path_yaml = path_dst_with_number / f"data.yaml"
    train_images_path = PurePosixPath().joinpath(path_dst_with_number.name, TRAIN_DIRECTORY, IMAGES_DIRECTORY)
    valid_images_path = PurePosixPath().joinpath(path_dst_with_number.name, VALID_DIRECTORY, IMAGES_DIRECTORY)
    test_images_path = PurePosixPath().joinpath(path_dst_with_number.name, TEST_DIRECTORY, IMAGES_DIRECTORY)
    data = {'path': path_google_collab.__str__(),
            'train': train_images_path.__str__(),
            'val': valid_images_path.__str__(),
            'test=': test_images_path.__str__(),
            'nc': len(labels),
            'names': labels
            }
    ic(data)
    with open(path_yaml, 'w') as file:
        outputs = yaml.dump(data, file, sort_keys=False)
        ic(outputs)

if __name__ == '__main__':
    # convert(r"C:\Python\Dataset\Videos02\yolo", # path_origin  raw string sin bara final
    #         r"C:\Python\GDrive\Datasets\Pigeons01",  # path_destination  raw string sin bara final,
    #         r"/content/drive/MyDrive/Datasets/",
    #         perc_train=70, perc_valid=20, perc_test=10
    #         )
    convert(r"C:\Python\Ultralytics\VideoDetection\01_YoloV8_yaml_train_valid_test\yolo", # path_origin  raw string sin bara final
            r"C:\Python\Ultralytics\VideoDetection\01_YoloV8_yaml_train_valid_test\yolo8",  # path_destination  raw string sin bara final
            r"/content/drive/MyDrive/Datasets/"
            )