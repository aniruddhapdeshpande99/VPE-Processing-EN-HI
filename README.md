# Processing English Verb Phrase Ellipsis for Conversational English-Hindi Machine Translation
This repository contains the code to the rule-based system and the annotated VPE data from the paper **"Processing English Verb Phrase Ellipsis for Conversational English-Hindi Machine Translation"** accepted at the **International Conference on Human-Informed Translation and Interpreting Technology (HiT-IT 2023)**. 

## Data
The annotated data for Verb Phrase Ellipsis in conversational English can be found in the ```Data``` directory. It is divided into two Excel files titled ```train.xlsx``` and ```test.xlsx```. 

## Setup
* The code is in Python 3.8.10.
* We suggest that you utilize a virtual environment while setting up the code by either setting up a [Virtual Environment](https://docs.python.org/3/library/venv.html) or a [Conda Environment](https://docs.conda.io/projects/conda/en/latest/user-guide/index.html).
* Install pandas using the following command : ```pip install pandas```
* Install Jupyter Notebook using ```pip install notebook```
* Install NLTK using the following command: ```pip install nltk==3.7```
* Install pycorenlp using the following command: ```pip install pycorenlp==0.3.0```
* Setup Spacy using the following commands:
  * ```pip install -U pip setuptools wheel```
  * ``` pip install -U spacy```
  * ```python -m spacy download en_core_web_sm```
* Setup for AllenNLP:
  * Install AllenNLP using ```pip install allennlp==2.1.0 allennlp-models==2.1.0```
  * Download AllenNLP SRL Model from this [link](https://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15.tar.gz).
  * Move the downloaded model to the **Models** directory of this repository using the following:
  * ```mv structured-prediction-srl-bert.2020.12.15.tar.gz your_local_directory_path/VPE-Processing-EN-HI/Models```

* Install StanfordCoreNLP using the steps from the following [link]([https://stanfordnlp.github.io/CoreNLP/download.html](https://stanfordnlp.github.io/CoreNLP/download.html#steps-to-setup-from-the-official-release)).

## Running the Rule-Based System
* Go to the folder where you installed StanfordCoreNLP and run the following command:
  * ```java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators "tokenize,ssplit,pos,lemma,parse,sentiment" -port 9002 -timeout 30000```
* In a new terminal tab, run Jupyter Notebook using ```jupyter notebook --port 8888```. You can use a port of your choice.
* Open your browser and go to [localhost:8888](localhost:8888) or [localhost:YOUR_PORT](localhost:YOUR_PORT).
* Run ```vpe_main.ipynb``` to run the rule-based system on the annotated Train Data.
* Run ```vpe_main_test.ipynb``` to run the rule-based system on the annotated Test Data.
* If you wish to run the model on your own conversations, do as follows:
  * In a terminal tab, run ```cd your_local_directory_path/VPE-Processing-EN-HI/Test_Data```.
  * Open the file titled ```new_convo_test_cases.txt``` and add your conversations
  * Ensure each conversation is in one single line.
  * The rule-based system is designed for two-person English conversations. In your conversation string, you must ensure that you use ```__eou__``` to indicate a switch of the speaker between sentences. Make sure you add a space before and after ```__eou__```. You can refer to the already existing conversations in the file to ensure whether your new conversation is correctly formatted or not.
  * Run ```vpe_main_test_new_convo.ipynb``` on your Jupyter Notebook in the browser.

## Authors (LTRC IIIT-Hyderabad)
* **Aniruddha Prashant Deshpande** [(Github)](https://github.com/aniruddhapdeshpande99)
* **Dr. Dipti Misra Sharma** [(Personal Faculty Page)](https://www.iiit.ac.in/people/faculty/dipti/)

## License
This project is licensed under the MIT License - [LICENSE.md](LICENSE.md)


