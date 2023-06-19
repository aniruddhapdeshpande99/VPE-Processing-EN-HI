def clean_verb_list_same_sen(Parsed, Verb_list, row_index):
    
    # REMOVE THE LICENSOR FROM VERB LIST
    if(row_index in Verb_list):
        del Verb_list[row_index]
    
    ##<NEW> REMOVING IMPERATIVE LET
    imperative_let_list = []
    for curr_verb_index in Verb_list.keys():
        if Parsed[curr_verb_index][4] == 'let'.casefold():
            let_subject_flag = False
            for i in range(0,len(Parsed)):
                if Parsed[i][2] == 'nsubj' and int(Parsed[i][1])-1 == curr_verb_index:
                    let_subject_flag = True
                    break
            
            if let_subject_flag == False:
                imperative_let_list.append(curr_verb_index)
    
    for let_index in imperative_let_list:
        del Verb_list[let_index]
    ##</NEW>
    
    ##<NEW> REMOVING AUX FROM VERB LIST
    aux_verbs_list = []
    for curr_verb_index in Verb_list.keys():
        if Parsed[curr_verb_index][2] == 'aux':
            aux_verbs_list.append(curr_verb_index)
    
    for aux_index in aux_verbs_list:
        del Verb_list[aux_index]
    ##</NEW>
    
    # REMOVING VERBS THAT COME AFTER THE LICENSOR IN THE SENTENCE
    verbs_after_ellipsis = []
    for key in Verb_list:
        if key > row_index:
            verbs_after_ellipsis.append(key)
    
    for token_index in verbs_after_ellipsis:
        del Verb_list[token_index]
    
    return Verb_list