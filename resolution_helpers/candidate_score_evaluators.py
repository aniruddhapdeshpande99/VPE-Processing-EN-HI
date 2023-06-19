# Function to Find the Final Antecedent using the list of scores assigned to the 
# list of potential antecedent verb candidates
def evaluate_scores(Verb_list_same_sen, Verb_lists_previous_sens, sen_indices, vpe_sent_dict,  default, temp_entry_output_storage_file):
    
    # Step 1: Disadvantage backward gapping i.e. penalize by 1 point 
    # IF the index of the verb from the list of potential antecedent verbs is MORE THAN the index of the licensor
    # [i.e. The verb is ahead in the sentence and hence 1 point must be deducted from that.]
    
    row_index = vpe_sent_dict['site']
    
    for key in Verb_list_same_sen:
        if(key > row_index):
            Verb_list_same_sen[key] -= 1
            
    
    ## <NEW>
    if len(Verb_lists_previous_sens) == 3:

        if vpe_sent_dict['category'] == 5:
            Verb_lists_previous_sens[0].update((x, y*0.2) for x, y in Verb_lists_previous_sens[0].items())
            Verb_lists_previous_sens[1].update((x, y*0.5) for x, y in Verb_lists_previous_sens[1].items())

        else:
            Verb_lists_previous_sens[0].update((x, y*0.65) for x, y in Verb_lists_previous_sens[0].items())
            Verb_lists_previous_sens[1].update((x, y*0.8) for x, y in Verb_lists_previous_sens[1].items())
    
    elif len(Verb_lists_previous_sens) == 2:
        if vpe_sent_dict['category'] == 5:
            Verb_lists_previous_sens[0].update((x, y*0.5) for x, y in Verb_lists_previous_sens[0].items())
        else:
            Verb_lists_previous_sens[0].update((x, y*0.8) for x, y in Verb_lists_previous_sens[0].items())
    
    
    print("AFTER ADDING SCORE MULTIPLIERS", file = temp_entry_output_storage_file)
    print(sen_indices, file = temp_entry_output_storage_file)
    print(Verb_list_same_sen, file = temp_entry_output_storage_file)
    print(Verb_lists_previous_sens, file = temp_entry_output_storage_file)
    print("-----------------------------\n\n", file = temp_entry_output_storage_file)
    ## </NEW>
    
    # Step 2: Print the scores after Disadvantaging backward gapping
    
    max_score = 0
    
    for key in Verb_list_same_sen:
        if Verb_list_same_sen[key] > max_score:
            max_score = Verb_list_same_sen[key]
    
    for Verb_list_prev in Verb_lists_previous_sens:
        for key in Verb_list_prev:
            if Verb_list_prev[key] > max_score:
                max_score = Verb_list_prev[key]
    
    clashing_verbs_same_sen = []
    for key in Verb_list_same_sen:
        if Verb_list_same_sen[key] == max_score:
            clashing_verbs_same_sen.append(key)
    
    #Checking if all the verb lists for previous sentences are empty or not
    verb_lists_empty_flag = 1
    
    for verb_list in Verb_lists_previous_sens:
        if len(verb_list) > 0:
            verb_lists_empty_flag = 0
            break
    
    
    # If Verb with max score is in the same sentence then the closest antecedent candidate must be within the same sentence
    # where VPE occurs
    if len(clashing_verbs_same_sen) > 0:

        # Step 6: IF there are clashes in the same sentence then 
        # Find verb at minimum distance before in the same sentence,
        # if none, then look after Site of Ellipsis (i.e. Index of Licensor) 
        closest_verb_before = -1
        closest_verb_after = -1
        for v in clashing_verbs_same_sen:
            # Step 6.1: Looking for the nearest verb that occurs BEFORE the licensor from the list of clashing verbs
            if(v < row_index and v > closest_verb_before):
                closest_verb_before = v
            # Step 6.2: Looking for the nearest verb that occurs AFTER the licensor from the list of clashing verbs
            if(v > row_index and v > closest_verb_after):
                closest_verb_after = v
        
        # Step 7: IF there is No nearest verb that occurs BEFORE the licensor 
        # then RETURN the nearest verb that occurs AFTER the licensor
        # ELSE do vice versa
        if(closest_verb_before != -1):
            return closest_verb_before
        else:
            return closest_verb_after
    
    elif verb_lists_empty_flag:
        return -1
    # i.e we look for the nearest verb with the highest score from the previous sentences
    else:
        clashing_verbs_prev_sents = {}
        for index, Verb_list_prev in enumerate(Verb_lists_previous_sens):
            clashing_verbs_prev_sents[index] = []
            for key in Verb_list_prev:
                if Verb_list_prev[key] == max_score:
                    clashing_verbs_prev_sents[index].append(key)
                  
            if clashing_verbs_prev_sents[index] == []:
                del clashing_verbs_prev_sents[index]
            else:
                clashing_verbs_prev_sents[index] = max(clashing_verbs_prev_sents[index])
        
        # Nearest Sentence with max score needs to be chosen. We choose the verb with the highest index from this sentence 
        # because we want the verb furthest within that sentence for it to be closest to the site of ellipsis
        
        if len(clashing_verbs_prev_sents.keys()) > 0:
            nearest_prev_sen = sen_indices[max(clashing_verbs_prev_sents.keys())]
            return [nearest_prev_sen, clashing_verbs_prev_sents[max(clashing_verbs_prev_sents.keys())]]
        else:
            return -1

def evaluate_scores_same_sen(Verb_list_same_sen, vpe_sent_dict, default):
    
    # Step 1: If The verb list is empty then return -1 (Mostly only object part of the Verb phrase is ellided in this case)
    if len(Verb_list_same_sen) == 0:
        return -1
    
    # Step 2: Disadvantage backward gapping i.e. penalize by 1 point 
    # IF the index of the verb from the list of potential antecedent verbs is MORE THAN the index of the licensor
    # [i.e. The verb is ahead in the sentence and hence 1 point must be deducted from that.]
    
    row_index = vpe_sent_dict['site']
    
    for key in Verb_list_same_sen:
        if(key > row_index):
            Verb_list_same_sen[key] -= 1
    
    # Step 3: Find the Index of the Verb with the highest score
    optimal_verb = list(Verb_list_same_sen.keys())[0]
    for key in Verb_list_same_sen:
        if(Verb_list_same_sen[key] > Verb_list_same_sen[optimal_verb]):
            optimal_verb = key
    
    # Step 4: Collect clashes i.e. collect other Verbs from the list of potential antecedent verb candidates with 
    # the same score and store it in a list 'clashing_verbs'
    clashing_verbs = []
    for key in Verb_list_same_sen:
        if(Verb_list_same_sen[key] == Verb_list_same_sen[optimal_verb]):
            clashing_verbs.append(key)
    
    # Step 5: IF there are no other clashing Verbs then return the Verb with Highest score as the Final Antecedent
    if(len(clashing_verbs) == 1):
        return optimal_verb
    
    # Step 6: IF there are clashes then 
    # Find verb at minimum distance before, if none, then look after Site of Ellipsis (i.e. Index of Licensor) 
    closest_verb_before = -1
    closest_verb_after = -1
    for v in clashing_verbs:
        # Step 6.1: Looking for the nearest verb that occurs BEFORE the licensor from the list of clashing verbs
        if(v < row_index and v > closest_verb_before):
            closest_verb_before = v
        # Step 6.2: Looking for the nearest verb that occurs AFTER the licensor from the list of clashing verbs
        if(v > row_index and v > closest_verb_after):
            closest_verb_after = v
    
    # Step 7: IF there is No nearest verb that occurs BEFORE the licensor 
    # then RETURN the nearest verb that occurs AFTER the licensor
    # ELSE do vice versa
    if(closest_verb_before != -1):
        return(closest_verb_before)
    else:
        return(closest_verb_after)