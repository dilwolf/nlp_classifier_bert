# NLP Classifier using BERT
## Introduction
This project focuses on training a BERT model for various NLP classification tasks and making predictions on new data using the batch_inference.py script. The architecture is designed to be easily extendable, allowing the incorporation of various other models.

## Installation
### Set up

1. Clone the repository

- $ git clone https://github.com/dilwolf/nlp_classifier_bert.git
- $ cd nlp_classifier_bert

### Python

2. Install required libraries

- `$ pip install -r requirements.txt`
- `$ Copy the training or testing dataset in the "data" folder `

3. Place the train.csv and test.csv files into the data folder.

4. Run train script

- $ python training.py

5. Run Inference script

- $ python batch_inference.py

### Docker
- `$ docker build . -t nlp_classifier`
- `$ docker run -it -v $DATA_FOLDER:/app/data -v $LOCAL_SAVED_MODEL_FOLDER:/app/saved_models nlp_classifier python batch_inference.py` or `python training.py`

## Extra options
### Manging Configurations
* Configuration settings are located in the conf folder. You can modify these files to change the data path, model path, and other parameters. 
* To customize configurations directly via the command line, use the --help flag to see available options:
- $ python3 batch_inference.py --help
This will display the configurable parameters and their usage.
