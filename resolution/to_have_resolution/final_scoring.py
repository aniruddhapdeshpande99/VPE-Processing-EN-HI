from resolution_helpers.verb_details_extractors import extract_licensor_details, extract_candidate_details
from resolution.to_have_resolution.nominal_subject_scoring import nsubj_same_sen_scoring, nsubj_prev_sen_scoring
from resolution.to_have_resolution.complement_clause_scoring import score_complement_clause_same_sen, score_complement_clause_prev_sen
from resolution.to_have_resolution.aux_scoring import aux_scoring_same_sen, aux_scoring_prev_sen
from resolution.to_have_resolution.verb_list_cleaners import verb_list_cleaner_same_sen, verb_list_cleaner_prev_sen
from resolution_helpers.main_verb_resolution import resolve_head_verb

def backtracking_score_same_sen(vpe_sent_dict, Verb_list_same_sentence):
    
    # Step 16: Scoring by Backtracking up the dependency tree
    # [I THINK THIS MODULE ASSIGNS HIGHER SCORE TO THE NEAREST/FIRST VERB FOUND BY BACKTRACKING UP THE
    # DEPENDENCY TREE WITH THE STARTING POINT AS THE lICENSOR. THIS VERB WILL THEN BE AWARDED HIGHER SCORE FROM 
    # WITHIN THE VERB LIST.]
    
    Parsed = vpe_sent_dict['parsed_vpe_sent']
    ellipsis = vpe_sent_dict['category']
    row_index = vpe_sent_dict['site']
    
    Verb_list = Verb_list_same_sentence

    # Step 16.1: Initializing variables for scoring. Storing the parent of the Licensor in variable 'parent'.
    default = -1
    backtracking_verb = -1
    parent = int(Parsed[row_index][1]) - 1

    if len(Verb_list) == 0:
        return Verb_list, default
    
    # Step 16.3.2: Loop WHILE value of 'parent' is not initial value -1 
    # AND WHILE POS Tag of token at 'parent' index is not Verb
    # AND WHILE value of 'parent' is not same as licensor's parent in the dependency relation
    # then Change the value of 'parent' to its parent in the dependency relation
    while(parent != -1 and (Parsed[parent][3].startswith('VB') == False)): 
        if(parent == (int)(Parsed[parent][1]) - 1):
            break
        parent = (int)(Parsed[parent][1]) - 1
    
    # Step 16.3.3: IF POS Tag of token at 'parent' index is Verb type POS then assign 
    # value of 'parent' to the variable 'backtracking_verb' 
    if(Parsed[parent][3].startswith('VB')):
        backtracking_verb = parent
    
    # Step 16.4: Award 1 point to the score of the backtracked nearest verb in the verb list.
    # Step 16.5: Default antecedent is the nearest verb from the licensor in the dependency tree.
    if(backtracking_verb in Verb_list):
        Verb_list[backtracking_verb] += 1
        default = backtracking_verb
    
    # Step 17: Print the final scores of the Verb List after Finding the nearest backtracked verb to that of the licensor
    
    return Verb_list, default


def resolve_to_have(Parsed_vpe_sen, Verb_list_same_sen, all_sen_vpe, vpe_sent_dict, Parsed_prev_sents, Verb_lists_previous_sens, sentence_speakers_list, sen_indices, parsed_conversation, temp_entry_output_storage_file):
       
    ellipsis_site = vpe_sent_dict['site']
    ellipsis_category = vpe_sent_dict['category']
    vpe_sen_index = vpe_sent_dict['sen_index']

    # Extracting Licensor Details
    licensor_details = extract_licensor_details(Parsed_vpe_sen, ellipsis_site, ellipsis_category, sentence_speakers_list[vpe_sen_index])
    

    print("BEFORE VERB LIST FILTERING", file = temp_entry_output_storage_file)
    print(sen_indices, file = temp_entry_output_storage_file)
    print(Verb_list_same_sen, file = temp_entry_output_storage_file)
    print(Verb_lists_previous_sens, file = temp_entry_output_storage_file)
    print("\n", file = temp_entry_output_storage_file)

    # Cleaning list of verb candidates in the same sentence
    Verb_list_same_sen = verb_list_cleaner_same_sen(Parsed_vpe_sen, ellipsis_site, Verb_list_same_sen, all_sen_vpe, vpe_sen_index)

    # Cleaning list of verb candidates in previous sentences
    Verb_lists_previous_sens_cleaned = []
    for i in range(0, len(Verb_lists_previous_sens)):
        Verb_lists_previous_sens_cleaned.append(verb_list_cleaner_prev_sen(Parsed_prev_sents[i], Verb_lists_previous_sens[i]))

    Verb_lists_previous_sens = Verb_lists_previous_sens_cleaned

    print("AFTER VERB LIST FILTERING", file = temp_entry_output_storage_file)
    print(sen_indices, file = temp_entry_output_storage_file)
    print(Verb_list_same_sen, file = temp_entry_output_storage_file)
    print(Verb_lists_previous_sens, file = temp_entry_output_storage_file)
    print("\n", file = temp_entry_output_storage_file)
    
    # Extracting Candidate's details (Nominal Subject, AUX, Complement Clause Depth) from same sentence
    verb_details_same_sen = {}

    if len(Verb_list_same_sen) > 0:

        for each_key in Verb_list_same_sen:
            real_index = each_key
            parent_index = (int)(Parsed_vpe_sen[each_key][1]) - 1
            
            if(Parsed_vpe_sen[each_key][4] == 'be'.casefold()) and Parsed_vpe_sen[parent_index][3].startswith("VB"):
                real_index = parent_index
            
            verb_details_same_sen[each_key] = extract_candidate_details(Parsed_vpe_sen, real_index, vpe_sen_index, sentence_speakers_list[vpe_sen_index])
    
    # Extracting Candidate's details (Nominal Subject, AUX, Complement Clause Depth) from previous sentences
    verb_details_prev_sents = []
    for i in range(0,len(sen_indices)):
        
        verb_details_previous = {}
        
        if len(Verb_lists_previous_sens[i]) > 0:
            
            for each_key in Verb_lists_previous_sens[i]:
                real_index = each_key
                parent_index = (int)(Parsed_prev_sents[i][each_key][1]) - 1
                
                if(Parsed_prev_sents[i][each_key][4] == 'be'.casefold()) and Parsed_prev_sents[i][parent_index][3].startswith("VB"):
                    real_index = parent_index
                
                verb_details_previous[each_key] = extract_candidate_details(Parsed_prev_sents[i], real_index, sen_indices[i], sentence_speakers_list[sen_indices[i]])

        verb_details_prev_sents.append(verb_details_previous)
    
    # Nominal Subject based scoring
    Verb_list_same_sen = nsubj_same_sen_scoring(Verb_list_same_sen, licensor_details, verb_details_same_sen, temp_entry_output_storage_file)
    Verb_lists_previous_sens = nsubj_prev_sen_scoring(Verb_lists_previous_sens, licensor_details, verb_details_prev_sents, Parsed_prev_sents, temp_entry_output_storage_file)

    print("AFTER NOMINAL SUBJECT BASED SCORING", file = temp_entry_output_storage_file)
    print(sen_indices, file = temp_entry_output_storage_file)
    print(Verb_list_same_sen, file = temp_entry_output_storage_file)
    print(Verb_lists_previous_sens, file = temp_entry_output_storage_file)
    print("\n", file = temp_entry_output_storage_file)

    # Scoring based on complement clause depth in the same sentence
    Verb_list_same_sen = score_complement_clause_same_sen(vpe_sent_dict, Verb_list_same_sen)
    Verb_lists_previous_sens = score_complement_clause_prev_sen(Verb_lists_previous_sens, licensor_details, verb_details_prev_sents, Parsed_prev_sents, temp_entry_output_storage_file)

    print("AFTER COMP CLAUSE BASED SCORING", file = temp_entry_output_storage_file)
    print(sen_indices, file = temp_entry_output_storage_file)
    print(Verb_list_same_sen, file = temp_entry_output_storage_file)
    print(Verb_lists_previous_sens, file = temp_entry_output_storage_file)
    print("\n", file = temp_entry_output_storage_file)

    # Scoring based on AUX
    Verb_list_same_sen = aux_scoring_same_sen(vpe_sent_dict, Verb_list_same_sen, verb_details_same_sen)
    Verb_lists_previous_sens = aux_scoring_prev_sen(Verb_lists_previous_sens, licensor_details, verb_details_prev_sents, Parsed_prev_sents)

    print("AFTER AUX BASED SCORING", file = temp_entry_output_storage_file)
    print(sen_indices, file = temp_entry_output_storage_file)
    print(Verb_list_same_sen, file = temp_entry_output_storage_file)
    print(Verb_lists_previous_sens, file = temp_entry_output_storage_file)
    print("\n", file = temp_entry_output_storage_file)

    # Scoring based on backtracking
    Verb_list_same_sen, default_resolution_same_sen = backtracking_score_same_sen(vpe_sent_dict, Verb_list_same_sen)

    print("AFTER BACKTRACKING BASED SCORING", file = temp_entry_output_storage_file)
    print(sen_indices, file = temp_entry_output_storage_file)
    print(Verb_list_same_sen, file = temp_entry_output_storage_file)
    print(Verb_lists_previous_sens, file = temp_entry_output_storage_file)
    print("\n", file = temp_entry_output_storage_file)

    return resolve_head_verb(vpe_sent_dict, Verb_list_same_sen, default_resolution_same_sen, Verb_lists_previous_sens, sen_indices, parsed_conversation, temp_entry_output_storage_file)
