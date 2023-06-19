from resolution_helpers.verb_list_cleaners import clean_verb_list_same_sen

def verb_list_cleaner_same_sen(Parsed_vpe_sen, ellipsis_site, Verb_list_same_sen, all_sen_vpe, vpe_sen_index):
    Indicator_To_Be = ["is", "isn’t","be", "been", "was", "wasn’t", "am", "ain’t", "are", "aren’t", "'m", "were", "weren't", "'re"]
    Indicator_To_Do = ["does", "doesn’t", "do", "don’t", "did"]
    Indicator_Modals = ["will", "wo", "would", "may", "might", "must", "can", "ca", "could", "should", "shall", "shan't", "'d", "'ll"] #NEW_CHANGE - Added shall, 'd and 'll

    Verb_list_same_sen = clean_verb_list_same_sen(Parsed_vpe_sen, Verb_list_same_sen, ellipsis_site)

    #<NEW> 
    # REMOVING GERUND VERBS FROM VERB LIST
    # gerunds = []
    # for key in Verb_list_same_sen:
    #     if(Parsed_vpe_sen[key][3] == 'VBG'):
    #         gerunds.append(key)

    # for key in gerunds:
    #     del Verb_list_same_sen[key]

    # REMOVING VERBS FROM THE SAME CATEGORY (TO_DO) FROM THE LIST
    same_class_candidates = []
    for key in Verb_list_same_sen:
        if(Parsed_vpe_sen[key][0].casefold() in Indicator_Modals):
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

    return Verb_list_same_sen
    
def verb_list_cleaner_prev_sen(Parsed_prev_sen, Verb_list_prev_sen):
    
    Indicator_To_Be = ["is", "isn’t","be", "been", "was", "wasn’t", "am", "ain’t", "are", "aren’t", "'m", "were", "weren't", "'re"]
    Indicator_To_Do = ["does", "doesn’t", "do", "don’t", "did"]
    Indicator_Modals = ["will", "wo", "would", "may", "might", "must", "can", "ca", "could", "should"]

    ############

    # gerunds = []
    # for key in Verb_list_prev_sen:
    #     if(Parsed_prev_sen[key][3] == 'VBG' and Parsed_prev_sen[key][2] != "xcomp"):
    #         gerunds.append(key)
    
    # for key in gerunds:
    #     del Verb_list_prev_sen[key]
    
    ############
    same_class = Indicator_Modals
    same_class_candidates = []
    for key in Verb_list_prev_sen:
        if(Parsed_prev_sen[key][0].casefold() in same_class):
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

    return Verb_list_prev_sen