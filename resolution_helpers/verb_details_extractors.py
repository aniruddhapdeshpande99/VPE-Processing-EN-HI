from resolution_helpers.nominal_subject_helpers import *
from resolution_helpers.comp_aux_helpers import *

def extract_licensor_details(Parsed, row_index, ellipsis, speaker):
    
    # Step 8: Find out the nominal subject (if it exists) for the current ellipsis licensor verb.
    
    # Step 8.1: Initializing few variables related to subject. We are storing the index of the licensor
    # to that of the variable name 'real_index'
    real_index = row_index
    
    # Step 8.1.1: IF Ellipsis is triggered by 'To' then we work on the index of the parent of 'To', else we work with
    # the index of the verb where ellipsis is detected. 
    if(ellipsis == 5):
        real_index = int(Parsed[row_index][1]) - 1
    # Step 8.2 : IF the relation of the parent to the licensor is marked as complement (Clausal or Open Clausal)
    # or is marked as a conjunction then we mark subject_exists as True. (i.e. Clausal Subject Exists)
    
    noun_subject, noun_subject_row = extract_nominal_subject_verb(Parsed, real_index)
    number, person, pronoun_flag, passive, proper = extract_nominal_subject_details(Parsed, noun_subject_row, noun_subject, row_index)    
    comp_clause_depth = extract_verb_comp_depth(Parsed, row_index)
    
    licensor_details_dictionary = {
        "nominal_subject_parsed": noun_subject_row,
        "lemmatized_licensor": Parsed[row_index][4],
        "proper_noun": proper,
        "plurality":number,
        "passivity":passive,
        "person": person,
        "pronoun_flag": pronoun_flag,
        "ellipsis_category": ellipsis,
        "comp_clause_depth": comp_clause_depth,
        "speaker": speaker
    }

    if noun_subject_row != -1:
        licensor_details_dictionary["nominal_subject"] = noun_subject.casefold()
    else:
        licensor_details_dictionary["nominal_subject"] = noun_subject
    
    return licensor_details_dictionary

def extract_candidate_details(Parsed, row_index, sen_index, speaker):
    
    # Step 8: Find out the nominal subject (if it exists) for the current ellipsis licensor verb.
    
    # Step 8.1: Initializing few variables related to subject. We are storing the index of the licensor
    # to that of the variable name 'real_index'
    real_index = row_index
    
    noun_subject, noun_subject_row = extract_nominal_subject_verb(Parsed, real_index)
    number, person, pronoun_flag, passive, proper = extract_nominal_subject_details(Parsed, noun_subject_row, noun_subject, row_index)    
    comp_clause_depth = extract_verb_comp_depth(Parsed, row_index)
    auxiliary, aux_class, lemmatized_auxiliary = extract_verb_aux(Parsed, row_index)
    
    candidate_details_dictionary = {
        "nominal_subject_parsed": noun_subject_row,
        "proper_noun": proper,
        "plurality":number,
        "passivity":passive,
        "person": person,
        "pronoun_flag": pronoun_flag,
        "aux": auxiliary,
        "aux_class": aux_class,
        "lemmatized_auxiliary": lemmatized_auxiliary,
        "comp_clause_depth": comp_clause_depth,
        "sen_index": sen_index,
        "speaker": speaker
    }
    
    if noun_subject_row != -1:
        candidate_details_dictionary["nominal_subject"] = noun_subject.casefold()
    else:
        candidate_details_dictionary["nominal_subject"] = noun_subject
        
    return candidate_details_dictionary