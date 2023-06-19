def aux_scoring_same_sen(vpe_sent_dict, Verb_list_same_sen, verb_candidate_details_dict):
    # Step 14: Scoring after comparing the class of Auxiliary Verbs of the Potential Antecedent Verbs and the ellipsis class (to_be, to_do, modals, to, to_have) 
    Indicator_Modals = ["will", "wo", "would", "may", "might", "must", "can", "ca", "could", "should"]
    Verb_list = Verb_list_same_sen
    Parsed = vpe_sent_dict['parsed_vpe_sent']
    ellipsis = vpe_sent_dict['category']

    if len(Verb_list) == 0:
        return Verb_list

    for each_key in Verb_list:
        if(vpe_sent_dict['lemmatized_licensor'] == verb_candidate_details_dict[each_key]["lemmatized_auxiliary"] and verb_candidate_details_dict[each_key]["lemmatized_auxiliary"] in Indicator_Modals):
            Verb_list[each_key] += 1
    
    # Step 15: Print the scores assigned to potential antecedent verbs after comparing auxiliary verbs.
    
    return Verb_list

def aux_scoring_prev_sen(Verb_lists_previous_sens, licensor_details, verb_details_prev_sents, Parsed_prev_sents):

    Indicator_Modals = ["will", "wo", "would", "may", "might", "must", "can", "ca", "could", "should"]

    for i in range(0, len(Verb_lists_previous_sens)):
        
        if len(Verb_lists_previous_sens[i]) > 0:
            
            for each_key in Verb_lists_previous_sens[i]:
                key = each_key
                
                if(verb_details_prev_sents[i][each_key]["lemmatized_auxiliary"] == licensor_details["lemmatized_licensor"] and verb_details_prev_sents[i][each_key]["lemmatized_auxiliary"] in Indicator_Modals):
                    Verb_lists_previous_sens[i][each_key] += 1
    
    return Verb_lists_previous_sens