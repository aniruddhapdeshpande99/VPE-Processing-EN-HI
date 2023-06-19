from resolution_helpers.verb_list_cleaners import clean_verb_list_same_sen

def verb_list_cleaner_same_sen(Parsed_vpe_sen, ellipsis_site, Verb_list_same_sen, all_sen_vpe, vpe_sen_index):
    Indicator_To_Be = ["is", "isn’t","be", "been", "was", "wasn’t", "am", "ain’t", "are", "aren’t", "'m", "were", "weren't", "'re"]
    Indicator_Modals = ["will", "wo", "would", "may", "might", "must", "can", "ca", "could", "should", "shall", "shan't", "'d", "'ll"] #NEW_CHANGE - Added shall, 'd and 'll


    Verb_list_same_sen = clean_verb_list_same_sen(Parsed_vpe_sen, Verb_list_same_sen, ellipsis_site)
    
    
    gerunds_and_participles = []
    for key in Verb_list_same_sen:
        if(Parsed_vpe_sen[key][3] != 'VBG' and Parsed_vpe_sen[key][3] != 'VBN'):
            gerunds_and_participles.append(key)
    for key in gerunds_and_participles:
        del Verb_list_same_sen[key]

    
    # REMOVING VERBS FROM THE SAME CATEGORY (TO_DO) FROM THE LIST
    same_class_candidates = []
    for key in Verb_list_same_sen:
        if(Parsed_vpe_sen[key][0].casefold() in Indicator_To_Be):
            same_class_candidates.append(key)
    for candidate in same_class_candidates:
        del Verb_list_same_sen[candidate]

    # See if there are any To_be type verbs in verb list. (Confusion here as I think it has to be Either To_be or modals 
    # based on the variable name but in the IF statement the conditions before and after OR are the same, so I am not sure)
    # If there are then store their indices in a list. Now in that list if the verb is an AUX verb and isn't a verb
    # that starts with 'be' then remove it from the list.
    be_or_modals = []
    for key in Verb_list_same_sen:
        if(Parsed_vpe_sen[key][4] in Indicator_To_Be or Parsed_vpe_sen[key][4] in Indicator_To_Be):
            be_or_modals.append(key)
    for v in be_or_modals:
        if(Parsed_vpe_sen[v][0].casefold().startswith('be') and not Parsed_vpe_sen[v][2].startswith('aux')):
            continue
        del Verb_list_same_sen[v]
    

    # RULE: We only keep those gerunds and past participles that have a to_be aux attached to them
    
    # This loop checks what remaining candidates have a To_be AUX attached to it
    candidates_to_keep_list = []
    for token in Parsed_vpe_sen:
        if token[-1].casefold() in Indicator_To_Be:
            parent_index = int(token[1])-1

            if parent_index in Verb_list_same_sen:
                candidates_to_keep_list.append(parent_index)
    
    # This loop finds the candidates that do not have To_be AUX attached to it from the list of verb candidates using the above made candidates_to_keep_list 
    candidates_to_remove_list = []
    for key in Verb_list_same_sen:
        if key not in candidates_to_keep_list:
            candidates_to_remove_list.append(key)
    
    # This loop will remove the gerund and past participle candidates that do not have To_be AUX as an auxiliary child
    for candidate_index in candidates_to_remove_list:
        del Verb_list_same_sen[candidate_index]

    return Verb_list_same_sen
    
def verb_list_cleaner_prev_sen(Parsed_prev_sen, Verb_list_prev_sen):
    
    Indicator_To_Be = ["is", "isn’t","be", "been", "was", "wasn’t", "am", "ain’t", "are", "aren’t", "'m", "were", "weren't", "'re", "'s"]

    ############
    # Step 4: IF There is 'To_be' ellipsis, keep only gerunds and past participles in the verbs list
    
    gerunds_and_participles = []
    for key in Verb_list_prev_sen:
        if(Parsed_prev_sen[key][3] != 'VBG' and Parsed_prev_sen[key][3] != 'VBN'):
            gerunds_and_participles.append(key)
    for key in gerunds_and_participles:
        del Verb_list_prev_sen[key]
    
    
    ############

    same_class_candidates = []
    for key in Verb_list_prev_sen:
        if(Parsed_prev_sen[key][0].casefold() in Indicator_To_Be):
            same_class_candidates.append(key)
    for candidate in same_class_candidates:
        del Verb_list_prev_sen[candidate]
    
    ###########


    # See if there are any To_be type verbs in verb list. (Confusion here as I think it has to be Either To_be or modals 
    # based on the variable name but in the IF statement the conditions before and after OR are the same, so I am not sure)
    # If there are then store their indices in a list. Now in that list if the verb is an AUX verb and isn't a verb
    # that starts with 'be' then remove it from the list.
    be_or_modals = []
    for key in Verb_list_prev_sen:
        if(Parsed_prev_sen[key][4] in Indicator_To_Be or Parsed_prev_sen[key][4] in Indicator_To_Be):
            be_or_modals.append(key)
    for v in be_or_modals:
        if(Parsed_prev_sen[v][0].casefold().startswith('be') and not Parsed_prev_sen[v][2].startswith('aux')):
            continue
        del Verb_list_prev_sen[v]
    

    # RULE: We only keep those gerunds and past participles that have a to_be aux attached to them
    
    # This loop checks what remaining candidates have a To_be AUX attached to it
    candidates_to_keep_list = []
    for token in Parsed_prev_sen:
        if token[-1].casefold() in Indicator_To_Be:
            parent_index = int(token[1])-1

            if parent_index in Verb_list_prev_sen:
                candidates_to_keep_list.append(parent_index)
    
    # This loop finds the candidates that do not have To_be AUX attached to it from the list of verb candidates using the above made candidates_to_keep_list 
    candidates_to_remove_list = []
    for key in Verb_list_prev_sen:
        if key not in candidates_to_keep_list:
            candidates_to_remove_list.append(key)
    
    # This loop will remove the gerund and past participle candidates that do not have To_be AUX as an auxiliary child
    for candidate_index in candidates_to_remove_list:
        del Verb_list_prev_sen[candidate_index]

    return Verb_list_prev_sen

    return Verb_list_prev_sen