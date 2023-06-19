from resolution_helpers.verb_list_cleaners import clean_verb_list_same_sen

def verb_list_cleaner_same_sen(Parsed_vpe_sen, ellipsis_site, Verb_list_same_sen, all_sen_vpe, vpe_sen_index):
    Indicator_To_Be = ["is", "isn’t","be", "been", "was", "wasn’t", "am", "ain’t", "are", "aren’t", "'m", "were", "weren't", "'re"]
    Indicator_Modals = ["will", "wo", "would", "may", "might", "must", "can", "ca", "could", "should", "shall", "shan't", "'d", "'ll"] #NEW_CHANGE - Added shall, 'd and 'll

    Verb_list_same_sen = clean_verb_list_same_sen(Parsed_vpe_sen, Verb_list_same_sen, ellipsis_site)
    
    # Removing parent of "To" licensor from verb list
    parent_key = int(Parsed_vpe_sen[ellipsis_site][1]) - 1
    if(parent_key in Verb_list_same_sen):
        del Verb_list_same_sen[parent_key]

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
    
def verb_list_cleaner_prev_sen(Parsed_prev_sen, Verb_list_prev_sen, Parsed_vpe_sen, ellipsis_site):
    
    Indicator_To_Be = ["is", "isn’t","be", "been", "was", "wasn’t", "am", "ain’t", "are", "aren’t", "'m", "were", "weren't", "'re"]
    Indicator_Modals = ["will", "wo", "would", "may", "might", "must", "can", "ca", "could", "should", "shall", "shan't", "'d", "'ll"] #NEW_CHANGE - Added shall, 'd and 'll

    # Removing all Imperative 'Let's from list of candidates
    imperative_lets = []
    for key in Verb_list_prev_sen:
        if Parsed_prev_sen[key][0].casefold() == 'let':
            imperative_flag = True
            for curr_index in range(0,key):
                if int(Parsed_prev_sen[curr_index][1])-1 == key and Parsed_prev_sen[curr_index][2].startswith('nsubj'):
                    imperative_flag = False
                    break
            if imperative_flag == True:
                imperative_lets.append(key)
    
    for key in imperative_lets:
        del Verb_list_prev_sen[key]


    # RULE: If the aux 'to' is attached to another head verb with adverbial modifier 'when' or 'whenever'
    # remove verb candidates that aren't connected with 'if' mark from previous sentences.

    # to_parent = int(Parsed_vpe_sen[ellipsis_site][1]) - 1

    # if_wh_list = ['if', 'whenever']
    
    # if Parsed_vpe_sen[to_parent][3].startswith('VB'): # Continue only if the parent to 'to' licensor is a verb
    #     if_wh_presence_flag_vpe = False
    #     for curr_index in range(0,to_parent):
    #         if Parsed_vpe_sen[curr_index][0].casefold() in if_wh_list and int(Parsed_vpe_sen[curr_index][1]) - 1 == to_parent:
    #             if_wh_presence_flag_vpe = True
    #             break
        
    #     # If the parent verb to the licensor 'to' has a child which is 'if' then we only keep verb candidates from the previous sentence with a 'when' or a 'whenever' child.
    #     if if_wh_presence_flag_vpe == True:
    #         non_if_wh_child_verb_candidates = []
    #         for key in Verb_list_prev_sen:
    #             if_wh_presence_candidate = False
    #             for curr_index in range(0, key):
    #                 if int(Parsed_prev_sen[curr_index][1]) -1 == key and Parsed_prev_sen[curr_index][0].casefold() in if_wh_list:
    #                     if_wh_presence_candidate = True
    #                     break

    #             if not if_wh_presence_candidate:
    #                 non_if_wh_child_verb_candidates.append(key)

    #         for key in non_if_wh_child_verb_candidates:
    #             del Verb_list_prev_sen[key]

    # Removing gerunds and past participles from previous sentence verb candidates
    gerunds = []
    for key in Verb_list_prev_sen:
        if(Parsed_prev_sen[key][3] == 'VBG'):
            gerunds.append(key)

    for key in gerunds:
        del Verb_list_prev_sen[key]

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