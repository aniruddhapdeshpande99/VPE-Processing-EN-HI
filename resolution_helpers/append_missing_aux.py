def find_missing_aux_verb(final_vpe_list, structured_conversation):
    Indicator_To_Have = ["has", "hasn’t", "have", "had", "'d", "'ve"]
    Indicator_Modals = ["will", "wo", "would", "may", "might", "must", "can", "ca", "could", "should", "shall", "shan't", "'d", "'ll"]
    Indicator_To_Be = ["'s", "is", "isn’t","be", "been", "was", "wasn’t", "am", "ain’t", "are", "aren’t", "'m", "were", "weren't", "'re"]

    for vpe in final_vpe_list:
        
        # Step 1: IF Ellipsis is of 'To Have' or 'Modals' type then do the following
        if(vpe['category'] == 3 or vpe['category'] == 4) and vpe['resolved_head_verb'] is not None:
            resolution_sen_parsed = structured_conversation[0][vpe['resolved_head_verb_sen_index']]
            resolved_verb_index = vpe['resolved_head_verb_site']
            same_category_aux_index = None

            for curr_index, curr_token  in enumerate(resolution_sen_parsed):
                if (curr_token[0].casefold() in Indicator_To_Have or curr_token[0].casefold() in Indicator_Modals) and int(curr_token[1]) - 1 == resolved_verb_index and vpe['resolved_head_verb'] not in Indicator_To_Be:
                    same_category_aux_index = curr_index
                    break
            
            if same_category_aux_index is not None:
                for curr_index, curr_token in enumerate(resolution_sen_parsed):
                    if (curr_token[0] in Indicator_To_Be) and int(curr_token[1]) - 1 == resolved_verb_index and curr_token[2] == 'aux' and curr_index > same_category_aux_index:
                        vpe['resolved_aux'] = curr_token[0]

    
    return final_vpe_list