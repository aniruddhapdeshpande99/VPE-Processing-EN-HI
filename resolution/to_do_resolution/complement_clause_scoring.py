def score_complement_clause_same_sen(vpe_sent_dict, Verb_list_same_sentence):
    
    Verb_list = Verb_list_same_sentence
    Parsed = vpe_sent_dict['parsed_vpe_sent']
    ellipsis_category = vpe_sent_dict['category']
    row_index = vpe_sent_dict['site']
    but_conj_flag = 0

    if len(Verb_list) == 0:
        return Verb_list

    # Step 12: Scoring based on Clausal Complement type relation (i.e. ccomp or xcomp) 
    # [I THINK WE ARE PENALIZING VERBS IF THE LICENSOR IS A PARENT TO ANOTHER VERB FROM THE VERB LIST
    # WITH THE RELATION BETWEEN THE TWO BEING THAT OF A CLAUSAL COMPLEMENT TYPE]

    # Step 12.1: Start with the index of the current Licensor. Store it in variable 'key'
    key = row_index

    # Step 12.2: Check if the current token (with index 'key') is related to its parent by a 
    # Complement type relation and loop on it until the condition is true.
    while(Parsed[key][2].endswith('comp')):
        parent = int(Parsed[key][1]) - 1

        # Step 12.2.1: If the parent to the Licensor which is linked by a Complement Clause type relation 
        # is part of the verb list then penalize and reduce its score by 3.

        if(parent in Verb_list):
            Verb_list[parent] -= 3

        # Step 12.2.2: Update 'key' with the index of the parent to the current token.
        key = parent
    
    # Award points to candidate if the To_Do licensor is a 'conj' child of the candidate such that the conjunction 
    # is 'but' which is a child of the licensor and there is a negation child to the licensor
    # Eg. "I always use a recipe but my grandmother never did <<use>>." 
    negation_flag = 0
    but_parent = None
    
    for token in Parsed:
        if int(token[1])-1 == vpe_sent_dict['site'] and token[2] == 'neg':
            negation_flag = 1
        
        if token[-1] == 'but' and token[2] == 'cc':
            if int(token[1]) - 1 == vpe_sent_dict['site'] or int(Parsed[vpe_sent_dict['site']][1]) - 1 == int(token[1]) - 1:
                but_conj_flag = 1
    
    licensor_parent = int(Parsed[vpe_sent_dict['site']][1]) - 1
    if negation_flag and but_conj_flag and licensor_parent != -1 and Parsed[licensor_parent][3] != 'VBD':
        Verb_list[licensor_parent] += 1
        
    # </NEW>

    # Step 12.3: For additional scoring for xcomp type relation (Open clausal complement),
    # we loop across each verb in verb list (using index variable 'each_key') and do the following:
    for each_key in Verb_list:

        # Step 12.3.1: Assign Index (i.e. Index within the original sentence) of the current verb from Verb List
        # to variable 'ancestor'
        ancestor = each_key

        # Step 12.3.2: Check if the current verb (with index 'ancestor') is related to its parent by a 
        # xcomp type relation and LOOP on it until the condition is true.
        while(Parsed[ancestor][2] == 'xcomp'):

            # Step 12.3.3: Within the LOOP we see IF current verb (with index 'ancestor') is same as the Licensor
            # OR IF current verb is 'not' and its parent is the Licensor
            # Then penalize and reduce score of the current verb from verb list by 3.
            if(ancestor == row_index or (Parsed[ancestor][4]=='not' and int(Parsed[ancestor][1]) - 1) == row_index):
                Verb_list[each_key] -= 3
                break

            # Step 12.3.4: Within the LOOP now we assign variable 'ancestor' with the index of its parent
            # [I think The while loop exists as multiple deeper levels of xcomp type relations might be there]
            ancestor = int(Parsed[ancestor][1]) - 1
    
    # <NEW> 03/01/23
    # STEP: If the ellipsis category is 'To_Do' then we need to give higher preference to the candidate that is the oldest
    # ancestor in the list of verbs that are connected by a CCOMP or XCOMP type of relation. There might be independent
    # lists of verbs connected by such a relation, and scoring them will be independent of other similar lists too,
    # but amongst them, the oldest ancestor should be preferred. Amongst all the oldest ancestors, the one nearest to the
    # licensor will then be considered in cases of tying scores.
    # E.g. In "You like to go to these places , don ’ t you ?", "like" should be preferred over "go"
    # if but_conj_flag == 0:
    #     for each_key in Verb_list:
    #         if Parsed[each_key][2].endswith('comp') and each_key > int(Parsed[each_key][1])-1:
    #             Verb_list[each_key] -= 1
    # </NEW>
    
    # Step 13: Print the scores assigned to potential antecedent verbs after disfavouring complement clauses
    
    return Verb_list

def score_complement_clause_prev_sen(Verb_lists_previous_sens, licensor_details, verb_details_prev_sents, Parsed_prev_sents, temp_entry_output_storage_file):
    
    licensor_comp_depth = licensor_details["comp_clause_depth"]

    for i in range(0, len(Verb_lists_previous_sens)):

        Parsed = Parsed_prev_sents[i]

        if len(Verb_lists_previous_sens[i]) > 0:
        
            # <NEW> 03/01/23
            # STEP: If the ellipsis category is 'To_Do' then we need to give higher preference to the candidate that is the oldest
            # ancestor in the list of verbs that are connected by a CCOMP or XCOMP type of relation. There might be independent
            # lists of verbs connected by such a relation, and scoring them will be independent of other similar lists too,
            # but amongst them, the oldest ancestor should be preferred. Amongst all the oldest ancestors, the one nearest to the
            # licensor will then be considered in cases of tying scores.
            # E.g. In "Laura told me today that she has a friend with a car for sale . __eou__ Oh , she did ?", "told" should be 
            # preferred over "has"
            for each_key in Verb_lists_previous_sens[i]:
                if Parsed[each_key][2].endswith('comp') and Parsed[each_key][3] != 'VBG' and each_key > int(Parsed[each_key][1])-1:
                    Verb_lists_previous_sens[i][each_key] -= 1
                
                if Parsed[each_key][2] == ('acl'):
                    Verb_lists_previous_sens[i][each_key] += 2
                    
            # </NEW>
            
            if licensor_comp_depth == 0:
                continue
            
            clausal_comp_childrens_list = []

            for index in range(len(Parsed)-1, -1, -1):
                
                if Parsed[index][2].endswith('comp'):
                    
                    comp_parent_flag = 0
                    
                    for clausal_comp_childrens in clausal_comp_childrens_list:
                        if index in clausal_comp_childrens:
                            comp_parent_flag = 1
                            break
                    
                    if comp_parent_flag == 0:
                        curr_clausal_comp = [index]
                        key = index
                        while(Parsed[key][2].endswith('comp')):
                            parent = int(Parsed[key][1]) - 1
                            curr_clausal_comp.append(parent)
                            key = parent
                        
                        curr_clausal_comp.reverse()
                        clausal_comp_childrens_list.append(curr_clausal_comp)
            
            for clausal_comp_childrens in clausal_comp_childrens_list:
                if licensor_comp_depth < len(clausal_comp_childrens):
                    
                    for penalty_index in range(1, licensor_comp_depth+1):
                        if penalty_index-1 < len(clausal_comp_childrens) and clausal_comp_childrens[penalty_index-1] in Verb_lists_previous_sens[i]:
                            Verb_lists_previous_sens[i][clausal_comp_childrens[penalty_index-1]] -= 1
    
    # Step 13: Print the scores assigned to potential antecedent verbs after disfavouring complement clauses
    
    return Verb_lists_previous_sens