# Label-studio Yolo to YoloV8

This project converts YOLO export format in Label-studio to YOLOv8 and splits the result into three directories - train, valid and test and generate a `data.yaml` file

## Installation

To use this project, follow these steps:

1. Clone this repository to your local machine.
2. Install the necessary packages using `pip install -r requirements.txt`
3. Move the Label-studio exported files into the main directory.
4. Run the `yolo_yaml_train_valid_test.py` file using `python yolo_yaml_train_valid_test.py`

## Directory Structure

After you run the main.py file, the converted YOLOv8 format files will be saved in the following directories:

- `train` directory for training dataset
- `valid` directory for validation dataset
- `test` directory for test dataset 

Each of the directories will include the converted files along with corresponding image files.

## Usage

To use the converted dataset for YOLOv8 training, you can follow the steps outlined in the official YOLOv8 documentation.

## Contact

If you have any questions or suggestions, please feel free to open an issue on GitHub or contact TensorGrass directly through their GitHub profile.

## Credits

This project was created by TensorGrass.