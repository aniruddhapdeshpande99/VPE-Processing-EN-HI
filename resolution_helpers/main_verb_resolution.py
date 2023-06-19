from helper_functions.sentence_type_categorizer import check_tag_question
from resolution_helpers.candidate_score_evaluators import evaluate_scores, evaluate_scores_same_sen

def resolve_ellided_object_child_ellipsis_parent(vpe_sent_dict, parsed_conversation):
    
    Indicator_To_Be = ["'s", "is", "isn’t","be", "been", "was", "wasn’t", "am", "ain’t", "are", "aren’t", "'m", "were", "weren't", "'re"] #NEW_CHANGE - Added 'm
    Indicator_To_Have = ["has", "hasn’t", "have", "had", "'d", "'ve"] #NEW_CHANGE - Added 'd and 've
    Indicator_To_Do = ["does", "doesn’t", "do", "don’t", "did"]
    Indicator_Modals = ["will", "wo", "would", "may", "might", "must", "can", "ca", "could", "should", "shall", "shan't", "'d", "'ll"] #NEW_CHANGE - Added shall, 'd and 'll
    Indicator_To = ["to"]
    
    Parsed = vpe_sent_dict['parsed_vpe_sent']
    
    if check_tag_question(Parsed):

        object_antecedent_parent_index = -1
        object_children_list = []
        
        if vpe_sent_dict['category'] == 1:
            
            for i in range(0, vpe_sent_dict['site']):
                if(Parsed[i][0].casefold() in Indicator_To_Be):
                    object_antecedent_parent_index = i
        
        elif vpe_sent_dict['category'] == 2:

            for i in range(0, vpe_sent_dict['site']):
                if(Parsed[i][0].casefold() in Indicator_To_Do):
                    object_antecedent_parent_index = i
        
        elif vpe_sent_dict['category'] == 3:
            
            for i in range(0, vpe_sent_dict['site']):
                if(Parsed[i][0].casefold() in Indicator_To_Have):
                    object_antecedent_parent_index = i
        
        elif vpe_sent_dict['category'] == 4:
            
            for i in range(0, vpe_sent_dict['site']):
                if(Parsed[i][0].casefold() in Indicator_Modals):
                    object_antecedent_parent_index = i
        
        return object_antecedent_parent_index, 4
    
    else:
        
        object_antecedent_parent_index = -1
        object_children_list = []
        Parsed_prev = parsed_conversation[vpe_sent_dict['sen_index']-1]
        prev_sen_len = len(Parsed_prev)
        
        if vpe_sent_dict['category'] == 1:
            
            for i in range(0, prev_sen_len):
                if(Parsed_prev[i][0].casefold() in Indicator_To_Be):
                    object_antecedent_parent_index = i
            
            if object_antecedent_parent_index == -1:
                for i in range(0, prev_sen_len):
                    if(Parsed_prev[i][3] == 'VBZ' or Parsed_prev[i][3] == 'VB'):
                        object_antecedent_parent_index = i
                
        
        elif vpe_sent_dict['category'] == 2:

            for i in range(0, prev_sen_len):
                if(Parsed_prev[i][0].casefold() in Indicator_To_Do):
                    object_antecedent_parent_index = i
        
        elif vpe_sent_dict['category'] == 3:
            
            for i in range(0, prev_sen_len):
                if(Parsed_prev[i][0].casefold() in Indicator_To_Have):
                    object_antecedent_parent_index = i
        
        elif vpe_sent_dict['category'] == 4:
            
            for i in range(0, prev_sen_len):
                if(Parsed_prev[i][0].casefold() in Indicator_Modals):
                    object_antecedent_parent_index = i
        
        return object_antecedent_parent_index, 2


def resolve_head_verb(vpe_sent_dict, Verb_list_same_sen, default, Verb_lists_previous_sens, sen_indices, parsed_conversation, temp_entry_output_storage_file):
    
    sen_index = vpe_sent_dict['sen_index']

    if (check_tag_question(vpe_sent_dict['parsed_vpe_sent']) and vpe_sent_dict['site'] > int(vpe_sent_dict['parsed_vpe_sent'][-2][1])-2):
        evaluated_value = evaluate_scores_same_sen(Verb_list_same_sen, vpe_sent_dict, default)
        # If Main verb not resolved look for Object Child Only Ellipsis
        if evaluated_value == -1:
            resolved_object_child, sentence_type = resolve_ellided_object_child_ellipsis_parent(vpe_sent_dict, parsed_conversation)
            if resolved_object_child != "":
                return None, resolved_object_child, sentence_type
            else:
                return None, None, -1
        else:
            main_verb = vpe_sent_dict['parsed_vpe_sent'][evaluated_value][0]
            resolution_site = evaluated_value
            return [main_verb, sen_index, resolution_site], None, 4 # Returning 4 for Tag question sentence type as the resolution comes from the same sentence
    
    
    # Evaluating Scores for VPE Cases where VPE doesn't occur in a Tag Question Type Sentence. 
    # For Question type sentence, the respective change in Sentence type is made later on in the function detect_resolve_vpe_sentence()
    
    evaluated_value = evaluate_scores(Verb_list_same_sen, Verb_lists_previous_sens, sen_indices, vpe_sent_dict,  default, temp_entry_output_storage_file)
    
    if type(evaluated_value) == list:
        main_verb = parsed_conversation[evaluated_value[0]][evaluated_value[1]][0]
        resolution_sen_index = evaluated_value[0]
        resolution_site = evaluated_value[1]
        return [main_verb, resolution_sen_index, resolution_site], None, 2 # Returning 2 for sentence type as the resolution comes from the previous sentence
    
    # If Main verb not resolved look for Object Child Only Ellipsis
    elif evaluated_value == -1:
        resolved_object_child, sentence_type = resolve_ellided_object_child_ellipsis_parent(vpe_sent_dict, parsed_conversation)
        if resolved_object_child != "":
            return None, resolved_object_child, sentence_type
        else:
            return None, None, -1
    else:
        main_verb = vpe_sent_dict['parsed_vpe_sent'][evaluated_value][0]
        resolution_site = evaluated_value
        return [main_verb, sen_index, resolution_site], None, 1