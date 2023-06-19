import re
import spacy
from pycorenlp import StanfordCoreNLP
from nltk.tokenize import sent_tokenize, word_tokenize
import os

# SRL predictors
from allennlp.predictors import Predictor
from allennlp_models import pretrained

# Loading Spacy Parser
nlp_spacy = spacy.load("en_core_web_sm")
# Loading Stanford NLP Parser
nlp = StanfordCoreNLP('http://0.0.0.0:9002')
#Loading AllenNLP SRL Model
srl_predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15.tar.gz") 


# Function to clean the text 
# The function removes spaces within words which use an apostrophe
def clean(text):
    text = text.replace("’", "'")
    text = text.replace(" ' ", "'") #NEW_CHANGE (Removed specific conditions and added one condition for cases with apostrophe)
    text = text.replace("Mr .", "Mr.")
    text = text.replace("Ms .", "Ms.")
    text = text.replace("Dr .", "Dr.")
    text = text.replace("Mrs .", "Mrs.")
    text = text.replace(" . . . ", " ...")
    text = re.sub(r'\b(OK|Ok|ok|O.K.|okay|Okay)\b', 'okay', text)
    text = re.sub(r'\b(gonna|Gonna)\b', 'going to', text)
    text = re.sub(' +', ' ', text)
    return(text.strip())

# This function sends each input sentence as an input to Stanford NLP Parser
# From the parser's output, we store the following:
#   1. Tokenized Word.
#   2. Parent Node in Dependency Graph Tree.
#   3. Dependency Relation.
#   4. POS Tag.
#   5. Lemmatized Word.
def Parse(S):
    whole_text = S
    sentences = [whole_text]
    Parsed = []
    for text in sentences:
        result = nlp.annotate(text,properties = {'annotaters': 'pos', 'outputFormat': 'conll', 'timeout': '50000',})
        Parsing = open("Parsing_test.txt", "w+")
        print(result, file = Parsing)
        Parsing.close()
        readParsing = open("Parsing_test.txt", "r")
        for line in readParsing:
            A = line.split()
            if(len(A) != 0):
                Parsed_Row = []
                Parsed_Row.append(A[1]) # Word
                Parsed_Row.append(A[5]) # Parent/Root
                Parsed_Row.append(A[6]) # Dependency relation
                Parsed_Row.append(A[3]) # POS tag
                Parsed_Row.append(A[2]) # Lemma
                Parsed.append(Parsed_Row)
        readParsing.close()
        os.remove("Parsing_test.txt")
    return(Parsed)

# This function sends each input sentence as an input to Spacy NLP Parser
# From the parser's output, we store the following:
#   1. Tokenized Word.
#   2. Parent Node in Dependency Graph Tree.
#   3. Dependency Relation.
#   4. POS Tag.
#   5. Lemmatized Word.
def Parse_spacy(S):
    whole_text = S
    sentences = [whole_text]
    Parsed = []
    
    for text in sentences:
        doc = nlp_spacy(text)

        for token in doc:

            Parsed_Row = []
            Parsed_Row.append(token.text) # Word
            ancestors = [t.i for t in token.ancestors]
            if len(ancestors) > 0:
                Parsed_Row.append(str(ancestors[0]+1)) # Parent
            else:
                Parsed_Row.append(str(0)) # Root
            Parsed_Row.append(token.dep_) # Dependency relation
            Parsed_Row.append(token.tag_) # POS tag
            Parsed_Row.append(token.lemma_) # Lemma
            Parsed.append(Parsed_Row)
    
    return Parsed

# Function to return all the tokens that are verbs from the parsed sentence
def get_verb_list(Parsed):
    Verb_list = {}
    for r in range(0, len(Parsed)):
        if(Parsed[r][3].startswith('VB')):
            Verb_list[r] = 0
    return(Verb_list)

# Function to return SRL for an input sentence
def get_srl(sentence):
    srl_result = srl_predictor.predict(sentence)
    return srl_result
    
def structure_conversation(conversation):
    speaker_wise_split = conversation.split("__eou__")
    speaker_switch_flags = []
    parsed_conversation = []
    sents_arr = []
    
    for text in speaker_wise_split:
        sents = sent_tokenize(text)
        for sent in sents:
            sents_arr.append(sent)
        for index,sent in enumerate(sents):
            parsed_conversation.append(Parse(clean(sent).strip()))
            if index < len(sents) - 1: 
                speaker_switch_flags.append(0)
            else:
                speaker_switch_flags.append(1)

    speaker_switch_flags = speaker_switch_flags[:-1]
    sentence_speakers_list = [None]*len(parsed_conversation)
    sentence_speakers_list[0] = "A"
    curr_speaker = "A"
    
    for i in range(0,len(speaker_switch_flags)):
        if speaker_switch_flags[i]:
            if curr_speaker == "A":
                sentence_speakers_list[i+1] = "B"
                curr_speaker = "B"
            else:
                sentence_speakers_list[i+1] = "A"
                curr_speaker = "A"
        else:
            if curr_speaker == "A":
                sentence_speakers_list[i+1] = "A"
                curr_speaker = "A"
            else:
                sentence_speakers_list[i+1] = "B"
                curr_speaker = "B"
    
    
    return parsed_conversation, sentence_speakers_list, sents_arr

def structure_conversation_spacy(conversation):
    speaker_wise_split = conversation.split("__eou__")
    speaker_switch_flags = []
    parsed_conversation = []
    sents_arr = []
    
    for text in speaker_wise_split:
        sents = sent_tokenize(text)
        for sent in sents:
            sents_arr.append(sent)
        for index,sent in enumerate(sents):
            parsed_conversation.append(Parse_spacy(clean(sent).strip()))
            if index < len(sents) - 1: 
                speaker_switch_flags.append(0)
            else:
                speaker_switch_flags.append(1)

    speaker_switch_flags = speaker_switch_flags[:-1]
    sentence_speakers_list = [None]*len(parsed_conversation)
    sentence_speakers_list[0] = "A"
    curr_speaker = "A"
    
    for i in range(0,len(speaker_switch_flags)):
        if speaker_switch_flags[i]:
            if curr_speaker == "A":
                sentence_speakers_list[i+1] = "B"
                curr_speaker = "B"
            else:
                sentence_speakers_list[i+1] = "A"
                curr_speaker = "A"
        else:
            if curr_speaker == "A":
                sentence_speakers_list[i+1] = "A"
                curr_speaker = "A"
            else:
                sentence_speakers_list[i+1] = "B"
                curr_speaker = "B"
    
    return parsed_conversation, sentence_speakers_list, sents_arr