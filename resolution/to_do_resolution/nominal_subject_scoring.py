from helper_functions.sentence_type_categorizer import check_wh_question, check_question

def nsubj_same_sen_scoring(Verb_list_same_sen, licensor_details, verb_candidate_details_dict, temp_entry_output_storage_file):
    
    if len(Verb_list_same_sen) == 0:
        return Verb_list_same_sen

    for each_key in Verb_list_same_sen:
        
        if(licensor_details["nominal_subject"] == verb_candidate_details_dict[each_key]["nominal_subject"]):
            print("%s SAME SUBJECT EXACT MATCH + 2" % (each_key), file = temp_entry_output_storage_file)
            Verb_list_same_sen[each_key] += 2
        else:
            # Step 10.9.2: -2 If the passivity (active/passive voice) of the nominal subject is different
            if(licensor_details["passivity"] != -1 and verb_candidate_details_dict[each_key]["passivity"] != -1 and licensor_details["passivity"] != verb_candidate_details_dict[each_key]["passivity"]):
                print("%s PASSIVITY - 2" % (each_key), file = temp_entry_output_storage_file)
                Verb_list_same_sen[each_key] -= 2 #the idea is to disadvantage the non-equal guys, not advantage the rest, because some may not have nsubj
            # Step 10.9.3: +1 If the plurality (singular/plural) of the nominal subject is same
            if(licensor_details["plurality"] == verb_candidate_details_dict[each_key]["plurality"]):
                print("%s NUMBER + 1" % (each_key), file = temp_entry_output_storage_file)
                Verb_list_same_sen[each_key] += 1
            # Step 10.9.4: +1 If the both nominal subjects are proper nouns
            if(licensor_details["proper_noun"] == 1 and verb_candidate_details_dict[each_key]["proper_noun"] == 1):
                print("%s PROPER NOUN + 1" % (each_key), file = temp_entry_output_storage_file)
                Verb_list_same_sen[each_key] += 1
    
    return Verb_list_same_sen

def nsubj_prev_sen_scoring(Verb_lists_previous_sens, licensor_details, verb_details_prev_sents, Parsed_prev_sents, temp_entry_output_storage_file):

    # NEW - ADDING LIST OF FIRST AND SECOND PERSON PRONOUNS FOR NOMINAL SUBJECT'S PERSON COMPARISON 
    # DURING CASES WHEN A PRONOUN IS USED
    first_person_pronouns = ["i", "me", "we", "us", "mine", "ours", "myself", "ourselves"]
    second_person_pronouns = ["you", "yours", "yourself", "yourselves"]
    third_person_pronouns = ["he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves"]
    
    noun_subject = licensor_details["nominal_subject"]
    noun_subject_row = licensor_details["nominal_subject_parsed"]
    ellipsis_sen_speaker = licensor_details["speaker"]
    passive = licensor_details["passivity"]
    number = licensor_details["plurality"]
    proper = licensor_details["proper_noun"]

    for i in range(0, len(Verb_lists_previous_sens)):

        verb_candidate_details_dict = verb_details_prev_sents[i]
        # Checking if the current previous sentence is a Yes/No Question or not
        prev_sen_yes_no_question_flag = False
        if check_question(Parsed_prev_sents[i]) and not check_wh_question(Parsed_prev_sents[i]):
            prev_sen_yes_no_question_flag = True
        
        # We can only add scores and use Details dictionary for comparison if the verb list has any
        # candidates
        if len(Verb_lists_previous_sens[i]) > 0:
            
            for each_key in Verb_lists_previous_sens[i]:

                verb_noun_subject = verb_candidate_details_dict[each_key]["nominal_subject"]
                prev_sen_rank = verb_candidate_details_dict[each_key]["sen_index"]
                prev_sen_speaker = verb_candidate_details_dict[each_key]["speaker"]
                verb_passive = verb_candidate_details_dict[each_key]["passivity"]
                verb_number = verb_candidate_details_dict[each_key]["plurality"]
                verb_proper = verb_candidate_details_dict[each_key]["proper_noun"]

                if (noun_subject == verb_noun_subject):
                        
                    if (noun_subject in first_person_pronouns or noun_subject in second_person_pronouns) and ellipsis_sen_speaker == prev_sen_speaker:
                        print("Prev %s - %s SAME SUBJECT FP SP NO SWITCH + 2" % (prev_sen_rank, each_key), file = temp_entry_output_storage_file)
                        Verb_lists_previous_sens[i][each_key] += 2

                        #Penalising for same subject even when speaker has changed
            #             elif (noun_subject in first_person_pronouns or noun_subject in second_person_pronouns) and ellipsis_sen_speaker != prev_sen_speaker:
            #                 print("Prev %s - %s SAME SUBJECT FP SP SWITCH - 1" % (prev_sen_rank, each_key), file = temp_entry_output_storage_file)
            #                 Verb_list[each_key] -= 1
                    
                    #Awarding +2 if the subject is in third person and if they completely match
                    elif (noun_subject not in first_person_pronouns and noun_subject not in second_person_pronouns):
                        print("Prev %s - %s SAME SUBJECT TP + 2" % (prev_sen_rank, each_key), file = temp_entry_output_storage_file)
                        Verb_lists_previous_sens[i][each_key] += 2
                else:
                    # Step 10.9.2: -2 If the passivity (active/passive voice) of the nominal subject is different then penalise by 2 points 
                    # if the ellipsis licensor isn't 'To_Be' type verb and the current previous sentence isn't a Yes/No Question 
                    if(passive != -1 and verb_passive != -1 and passive != verb_passive and not prev_sen_yes_no_question_flag):
                        print("Prev %s - %s PASSIVITY - 2" % (prev_sen_rank, each_key), file = temp_entry_output_storage_file)
                        Verb_lists_previous_sens[i][each_key] -= 2 #the idea is to disadvantage the non-equal guys, not advantage the rest, because some may not have nsubj
                    # Step 10.9.3: +1 If the plurality (singular/plural) of the nominal subject is same
                    if(number == verb_number):
                        print("Prev %s - %s NUMBER + 1" % (prev_sen_rank, each_key), file = temp_entry_output_storage_file)
                        Verb_lists_previous_sens[i][each_key] += 1
                    # Step 10.9.4: +1 If the both nominal subjects are proper nouns
                    if(proper ==1 and verb_proper == 1):
                        print("Prev %s - %s PROPER NOUN + 1" % (prev_sen_rank, each_key), file = temp_entry_output_storage_file)
                        Verb_lists_previous_sens[i][each_key] += 1
                    
                    # NEW - COMPARING PRONOUNS AT NOMINAL SUBJECT POSITION BASED ON WHETHER SPEAKER HAS SWITCHED OR NOT.
                    # STEP 10.9.5: IF SPEAKER HAS SWITCHED THEN 
                    # AWARD 1 POINT IF THE ANTECEDENT CANDIDATE'S NOMINAL SUBJECT PRONOUN'S PERSON IS OPPOSITE TO THAT OF LICENSOR'S NOMINAL SUBJECT PRONOUN'S PERSON
                    # (NOTE: HERE OPPOSITE MEANS 1ST VS 2ND PERSON)
                    # DEDUCT 1 POINT IF THE ANTECEDENT CANDIDATE'S NOMINAL SUBJECT PRONOUN'S PERSON IS SAME AS THAT OF LICENSOR'S NOMINAL SUBJECT PRONOUN'S PERSON
                    # ELSE DO VICE-A-VERSA
                    if noun_subject_row != -1 and noun_subject_row[3] == 'PRP' and (verb_noun_subject in first_person_pronouns or verb_noun_subject in second_person_pronouns) :
                        if ellipsis_sen_speaker != prev_sen_speaker:
                            if (noun_subject in first_person_pronouns and verb_noun_subject in second_person_pronouns) or (noun_subject in second_person_pronouns and verb_noun_subject in first_person_pronouns):
                                print("Prev %s - %s FP SP SWITCH + 1" % (prev_sen_rank, each_key), file = temp_entry_output_storage_file)
                                Verb_lists_previous_sens[i][each_key] += 1
            #                     else:
            #                         print("Prev %s - %s FP SP SWITCH - 1" % (prev_sen_rank, each_key), file = temp_entry_output_storage_file)
            #                         Verb_list[each_key] -= 1
                        else:
                            if (noun_subject in first_person_pronouns and verb_noun_subject in first_person_pronouns) or (noun_subject in second_person_pronouns and verb_noun_subject in second_person_pronouns):
                                print("Prev %s - %s FP SP NONSWITCH + 1" % (prev_sen_rank, each_key), file = temp_entry_output_storage_file)
                                Verb_lists_previous_sens[i][each_key] += 1
            #                     else:
            #                         print("Prev %s - %s FP SP NONSWITCH - 1" % (prev_sen_rank, each_key), file = temp_entry_output_storage_file)
            #                         Verb_list[each_key] -= 1
                    
                    # NEW STEP 10.9.6: If both the nominal subject of the potential candidate is in third person the licensor's nominal subject is a third person pronoun, then we award one point. 
                    elif verb_noun_subject != -1 and noun_subject_row != -1 and (noun_subject in third_person_pronouns) and (verb_noun_subject not in first_person_pronouns and verb_noun_subject not in second_person_pronouns):
                        print("Prev %s - %s TP + 1" % (prev_sen_rank, each_key), file = temp_entry_output_storage_file)
                        Verb_lists_previous_sens[i][each_key] += 1
                    
                    #NEW STEP 10.9.7 If the nominal subject of the licensor is a first or second person pronoun and the nominal subject of the candidate is a third person pronoun/noun, but not the third person wh-pronoun who then penalise by one point
                    elif verb_noun_subject != -1 and noun_subject_row != -1 and (noun_subject in second_person_pronouns or noun_subject in first_person_pronouns) and (verb_noun_subject in third_person_pronouns or (verb_noun_subject not in second_person_pronouns or verb_noun_subject not in first_person_pronouns) and verb_noun_subject != 'who'):
                        print("Prev %s - %s TP - 1" % (prev_sen_rank, each_key), file = temp_entry_output_storage_file)
                        Verb_lists_previous_sens[i][each_key] -= 1
    
    return Verb_lists_previous_sens