import copy
from helper_functions.helpers import structure_conversation, structure_conversation_spacy, get_srl, get_verb_list
from helper_functions.sentence_type_categorizer import check_question, check_tag_question
from resolution_helpers.main_verb_resolution import resolve_ellided_object_child_ellipsis_parent
from resolution_helpers.verb_details_extractors import extract_licensor_details
from detection.detect_to_be import To_Be
from detection.detect_to_do import To_Do
from detection.detect_to_have import To_Have
from detection.detect_modals import Modals
from detection.detect_to import To
from resolution.to_do_resolution.final_scoring import resolve_to_do
from resolution.to_be_resolution.final_scoring import resolve_to_be
from resolution.to_have_resolution.final_scoring import resolve_to_have
from resolution.modals_resolution.final_scoring import resolve_modals
from resolution.to_resolution.final_scoring import resolve_to


# Main Function to detect and resolve verbal ellipsis
def detect_resolve_vpe_sentence(All_words, sents_arr, Parsed, sen_index, structured_conversation, sentence_speakers_list, output_file, temp_entry_output_storage_file):
    
    #Retrieving SRL for the sentence
    sen_srl = get_srl(sents_arr[sen_index])
    
    # Creating separate lists of the potential licensors of Ellipsis. 
    # Each list consists of helper/aux verbs of a different class. These occur mosyt frequently at the site of Ellipsis
    Indicator_To_Be = ["is", "isn’t","be", "been", "was", "wasn’t", "am", "ain’t", "are", "aren’t", "'m", "were", "weren't", "'re"] #NEW_CHANGE - Added 'm
    Indicator_To_Have = ["has", "hasn’t", "have", "had", "'d", "'ve"] #NEW_CHANGE - Added 'd and 've
    Indicator_To_Do = ["does", "doesn’t", "do", "don’t", "did"]
    Indicator_Modals = ["will", "wo", "would", "may", "might", "must", "can", "ca", "could", "should", "shall", "shan't", "'d", "'ll"] #NEW_CHANGE - Added shall, 'd and 'll
    Indicator_To = ["to"]

    first_person_pronouns = ["i", "me", "we", "us", "mine", "ours", "myself", "ourselves", "'s"]
    second_person_pronouns = ["you", "yours", "yourself", "yourselves"]
    non_permission_modals = ["will", "wo", "would", "'d", "'ll"]
    
    # Creating a copy of list of tokens of the sentence
    Output_sentence = copy.copy(All_words)
    
    added_words = 0
    row_index = -1
    elliptical_verb = []
    
    all_sen_vpe = []
    
    # Looping through all the tokenized words in the sentence
    for index, word in enumerate(All_words):
        ellipsis = 0
        row_index += 1

        # Condition to check if the token is part of list of 'To Be' Type Helper Verbs
        if(word.casefold() in Indicator_To_Be and Parsed[index][4] in Indicator_To_Be): #NEW_CHANGE - Added "Parsed[index][4] in Indicator_To_Be" to consider the contracted aux verbs
            # If 'To be' verb is encountered in the sentence then we check if that 'To be' verb is a licensor or not using the To_Be() function containing the rules that determine if the 'To be' verb is a licensor or not
            if(To_Be(Parsed, row_index, sen_srl)):
                ellipsis = 1
                print("Ellipsis Type - 'Be' | Ellipsis at sentence number %d and token number - %d | Licensor - %s" % (sen_index + 1, row_index+1, All_words[row_index]), file = output_file)
        
        # Condition to check if the token is part of list of 'To have' Type Helper Verbs
        if(word in Indicator_To_Have and Parsed[index][4] in Indicator_To_Have): #NEW_CHANGE - Added "Parsed[index][4] in Indicator_To_Have" to consider the contracted aux verbs
            
            # If 'To have' verb is encountered in the sentence then we check if that 'To have' verb is a licensor or not using the To_Have() function containing the rules that determine if the 'To have' verb is a licensor or not
            if(To_Have(Parsed, row_index)):
                ellipsis = 3
                print("Ellipsis Type - 'Have' | Ellipsis at sentence number %d and token number - %d | Licensor - %s" % (sen_index + 1, row_index+1, All_words[row_index]), file = output_file)
                

        # Condition to check if the token is part of list of 'To do' Type Helper Verbs
        if(word.casefold() in Indicator_To_Do):
            
            # If 'To do' verb is encountered in the sentence then we check if that 'To do' verb is a licensor or not using the To_Do() function containing the rules that determine if the 'To do' verb is a licensor or not
            if(To_Do(Parsed, row_index)):
                ellipsis = 2
                print("Ellipsis Type - 'Do' | Ellipsis at sentence number %d and token number - %d | Licensor - %s" % (sen_index + 1, row_index+1, All_words[row_index]), file = output_file)
                
        
        # Condition to check if the token is part of list of 'Modals'
        if(word.casefold() in Indicator_Modals and Parsed[index][4] in Indicator_Modals): #NEW_CHANGE - Added "Parsed[index][4] in Indicator_Modals" to consider the contracted aux verbs
            
            # If a 'Modal' is encountered in the sentence then we check if that 'Modal' is a licensor or not using the Modals() function containing the rules that determine if the 'Modal' is a licensor or not
            if(Modals(Parsed, row_index)):
                ellipsis = 4
                print("Ellipsis Type - 'Modal' | Ellipsis at sentence number %d and token number - %d | Licensor - %s" % (sen_index + 1, row_index+1, All_words[row_index]), file = output_file)

        
        # Condition to check if the token is part of list of 'To' Type Helper Verbs
        if(word.casefold() in Indicator_To):
            
            # If 'To' verb is encountered in the sentence then we check if that 'To' verb is a licensor or not using the To() function containing the rules that determine if the 'To' verb is a licensor or not
            if(To(Parsed, row_index)):
                ellipsis = 5
                print("Ellipsis Type - 'To' | Ellipsis at sentence number %d and token number - %d | Licensor - %s" % (sen_index + 1, row_index+1, All_words[row_index]), file = output_file)
    
        if ellipsis:
            
            # Creating A Dictionary with VPE Details
            vpe_sent_dict = dict()
            vpe_sent_dict['category'] = ellipsis
            vpe_sent_dict['site'] = row_index
            vpe_sent_dict['licensor'] = Parsed[row_index][0]
            vpe_sent_dict['lemmatized_licensor'] = Parsed[row_index][4].casefold()
            vpe_sent_dict['sen_index'] = sen_index
            vpe_sent_dict['parsed_vpe_sent'] = Parsed

            licensor_details = extract_licensor_details(vpe_sent_dict['parsed_vpe_sent'], vpe_sent_dict['site'], vpe_sent_dict['category'], sentence_speakers_list[vpe_sent_dict['sen_index']])

            # Retrieving initial verb candidate list from same sentence
            Verb_list_same_sen = get_verb_list(vpe_sent_dict['parsed_vpe_sent'])

            # Retrieving initial verb candidate lists from previous sentences
            if sen_index == 0:
                Verb_lists_previous_sens = []
                Parsed_prev_sents = []
                sen_indices = []
            elif sen_index == 1:
                Verb_lists_previous_sens = [get_verb_list(structured_conversation[sen_index-1])]
                Parsed_prev_sents = [structured_conversation[sen_index-1]]
                sen_indices = [sen_index-1]
            elif sen_index == 2:
                Verb_lists_previous_sens = [get_verb_list(structured_conversation[sen_index-2]), get_verb_list(structured_conversation[sen_index-1])]
                Parsed_prev_sents = [structured_conversation[sen_index-2], structured_conversation[sen_index-1]]
                sen_indices = [sen_index-2, sen_index-1]
            else:
                Verb_lists_previous_sens = [get_verb_list(structured_conversation[sen_index-3]), get_verb_list(structured_conversation[sen_index-2]), get_verb_list(structured_conversation[sen_index-1])]
                Parsed_prev_sents = [structured_conversation[sen_index-3], structured_conversation[sen_index-2], structured_conversation[sen_index-1]]
                sen_indices = [sen_index-3, sen_index-2, sen_index-1]
            
            # Category wise resolution
            if ellipsis ==  1:
                vpe_sent_dict['resolved_head_verb'], vpe_sent_dict['ellided_obj_child_parent_verb'], vpe_sent_dict['sen_type'] = resolve_to_be(vpe_sent_dict['parsed_vpe_sent'], Verb_list_same_sen, all_sen_vpe, vpe_sent_dict, Parsed_prev_sents, Verb_lists_previous_sens, sentence_speakers_list, sen_indices, structured_conversation, temp_entry_output_storage_file)
            
            elif ellipsis == 2:        
                vpe_sent_dict['resolved_head_verb'], vpe_sent_dict['ellided_obj_child_parent_verb'], vpe_sent_dict['sen_type'] = resolve_to_do(vpe_sent_dict['parsed_vpe_sent'], Verb_list_same_sen, all_sen_vpe, vpe_sent_dict, Parsed_prev_sents, Verb_lists_previous_sens, sentence_speakers_list, sen_indices, structured_conversation, temp_entry_output_storage_file)
            
            elif ellipsis == 3:        
                vpe_sent_dict['resolved_head_verb'], vpe_sent_dict['ellided_obj_child_parent_verb'], vpe_sent_dict['sen_type'] = resolve_to_have(vpe_sent_dict['parsed_vpe_sent'], Verb_list_same_sen, all_sen_vpe, vpe_sent_dict, Parsed_prev_sents, Verb_lists_previous_sens, sentence_speakers_list, sen_indices, structured_conversation, temp_entry_output_storage_file)            
            
            elif ellipsis == 4:        
                vpe_sent_dict['resolved_head_verb'], vpe_sent_dict['ellided_obj_child_parent_verb'], vpe_sent_dict['sen_type'] = resolve_modals(vpe_sent_dict['parsed_vpe_sent'], Verb_list_same_sen, all_sen_vpe, vpe_sent_dict, Parsed_prev_sents, Verb_lists_previous_sens, sentence_speakers_list, sen_indices, structured_conversation, temp_entry_output_storage_file)

            elif ellipsis == 5:        
                vpe_sent_dict['resolved_head_verb'], vpe_sent_dict['ellided_obj_child_parent_verb'], vpe_sent_dict['sen_type'] = resolve_to(vpe_sent_dict['parsed_vpe_sent'], Verb_list_same_sen, all_sen_vpe, vpe_sent_dict, Parsed_prev_sents, Verb_lists_previous_sens, sentence_speakers_list, sen_indices, structured_conversation, temp_entry_output_storage_file)

            if ellipsis != 0:
                
                # Adding resolution information to the VPE Details dictionary 
                if type(vpe_sent_dict['resolved_head_verb']) is list:
                    vpe_sent_dict['resolved_head_verb_sen_index'] = vpe_sent_dict['resolved_head_verb'][1]
                    vpe_sent_dict['resolved_head_verb_site'] = vpe_sent_dict['resolved_head_verb'][2]
                    vpe_sent_dict['resolved_head_verb'] = vpe_sent_dict['resolved_head_verb'][0]
                
                # This removes some cases where the resolved verb is same as the licensor which comes up because 
                # there are times when 'have' and 'do' can act as main verbs and not as licensors. Therefore, it implies that
                # in the sentence in which it acts as a licensor, there only the object child is ellided but the head verb is actually present
                if vpe_sent_dict['resolved_head_verb'] is not None and vpe_sent_dict['resolved_head_verb'].strip().lower() == vpe_sent_dict['licensor'].strip().lower():
                    vpe_sent_dict['resolved_head_verb'] = None
                    vpe_sent_dict['ellided_obj_child_parent_verb'], vpe_sent_dict['sen_type'] = resolve_ellided_object_child_ellipsis_parent(vpe_sent_dict, structured_conversation)
                    
                vpe_sent_dict['vpe_sent'] = sents_arr[sen_index]
                
                if check_tag_question(Parsed):
                    vpe_sent_dict['sen_type'] = 4
                elif check_question(Parsed):
                    vpe_sent_dict['sen_type'] = 3


                # <NEW> 07/04/23
                # Adding Final Check for Resolution for Tag Question Special Case.
                # RULE: If the sentence type is a Tag Question and if the site of ellipsis comes as part of the tag question then do not use the resolution used from above scoring system. Only resolve in cases wherein either the sentence before the tag question is an imperative construction or it is asking for permission and the licensor is a modal type licensor
                if vpe_sent_dict['sen_type'] == 4 and vpe_sent_dict['site'] == int(vpe_sent_dict['parsed_vpe_sent'][-2][1])-1:

                    if ellipsis != 4:
                        vpe_sent_dict['resolved_head_verb'], vpe_sent_dict['ellided_obj_child_parent_verb'], vpe_sent_dict['resolved_head_verb_site'], vpe_sent_dict['resolved_head_verb_sen_index'] = None, None, None, None
                    
                    else:

                        # print("MODAL TAG")
                        
                        # Checking if the sentence preceding the modal tag question is imperative or not.
                        imperative_phrase_flag = True
                        for token_index in range(0, int(vpe_sent_dict['parsed_vpe_sent'][-2][1])-2):
                            if vpe_sent_dict['parsed_vpe_sent'][token_index][2] == 'nsubj':
                                imperative_phrase_flag = False
                                
                        
                        # RULE: If the sentence preceding the modal tag question is not imperative then we check if it is an imperative let type sentence, or if it is asking for permission. If it is neither then we do not resolve anything.
                        if imperative_phrase_flag ==  False:
                            
                            # print("NON IMPERATIVE MODAL TAG")
                            # RULE: Check if there is a first person imperative "Let" before the modal tag question or not. Unlike normal imperatives where there is no nomainal subject, here a first person pronoun is present. E.g. "Let us go shopping, shall we <<go shopping>>?"
                            if vpe_sent_dict['parsed_vpe_sent'][0][-1].casefold() == 'let' and vpe_sent_dict['parsed_vpe_sent'][1][-1].casefold() in first_person_pronouns and vpe_sent_dict['parsed_vpe_sent'][1][2] == 'nsubj':
                                
                                if 'VB' in vpe_sent_dict['parsed_vpe_sent'][int(vpe_sent_dict['parsed_vpe_sent'][1][1])-1][3]:
                                    antecedent_index = int(vpe_sent_dict['parsed_vpe_sent'][1][1])-1
                                    vpe_sent_dict['resolved_head_verb_sen_index'] = vpe_sent_dict['sen_index']
                                    vpe_sent_dict['resolved_head_verb_site'] = antecedent_index
                                    vpe_sent_dict['resolved_head_verb'], vpe_sent_dict['ellided_obj_child_parent_verb'] = vpe_sent_dict['parsed_vpe_sent'][antecedent_index][0], None

                                    # print("LET IMPERATIVE TAG")
                            
                            # RULE: Here we check for the case as to whether the sentence preceding the modal tag question is asking for permission or not. E.g. "I want to go swimming, can I <<go swimming>>?", "I aspire to be a dancer after graduation, may I <<be a dancer>>?"

                            elif vpe_sent_dict['licensor'].casefold() not in non_permission_modals and licensor_details['nominal_subject'] != -1 and licensor_details['nominal_subject'] not in second_person_pronouns:

                                # print("PERMISSION TYPE TAG")

                                ability_modal_presence = False
                                to_aux_presence = False
                                preceding_to_aux = None

                                for token_index in range(0, int(vpe_sent_dict['parsed_vpe_sent'][-2][1])-2):
                                    if vpe_sent_dict['parsed_vpe_sent'][token_index][0].casefold() == 'to'.casefold() and vpe_sent_dict['parsed_vpe_sent'][token_index][2] == 'aux':
                                        to_aux_presence = True
                                        preceding_to_aux = token_index
                                        # print("FOUND TO AUX IN PERMISSION TYPE TAG CHECK")
                                    
                                    # Special Case example that signifies ability over permission when modal is used which needs to be taken into consideration: E.g. "He will be able to drive us to the hotel, can he?"
                                    if vpe_sent_dict['parsed_vpe_sent'][token_index][0].casefold() in non_permission_modals and vpe_sent_dict['parsed_vpe_sent'][token_index][2] == 'aux' and vpe_sent_dict['parsed_vpe_sent'][int(vpe_sent_dict['parsed_vpe_sent'][token_index][1]) - 1][0].casefold() == 'be':
                                        ability_modal_presence = True
                                
                                if not ability_modal_presence and to_aux_presence:
                                    antecedent_index = int(vpe_sent_dict['parsed_vpe_sent'][preceding_to_aux][1])-1
                                    vpe_sent_dict['resolved_head_verb_sen_index'] = vpe_sent_dict['sen_index']
                                    vpe_sent_dict['resolved_head_verb_site'] = antecedent_index
                                    vpe_sent_dict['resolved_head_verb'], vpe_sent_dict['ellided_obj_child_parent_verb'] = vpe_sent_dict['parsed_vpe_sent'][antecedent_index][0], None
    
                            else:
                                vpe_sent_dict['resolved_head_verb'], vpe_sent_dict['ellided_obj_child_parent_verb'], vpe_sent_dict['resolved_head_verb_site'], vpe_sent_dict['resolved_head_verb_sen_index'] = None, None, None, None
                        
                vpe_dict_copy = vpe_sent_dict
                del vpe_dict_copy['parsed_vpe_sent']
                
                print(vpe_dict_copy, end = "\n\n", file = output_file)
                
                all_sen_vpe.append(vpe_sent_dict)
    
    return all_sen_vpe

def detect_resolve_vpe_conversation(conversation, output_file, temp_entry_output_storage_file):
    structured_conversation, sentence_speakers_list, sents_arr = structure_conversation(conversation)
    
    all_conversation_vpe = []
    
    for sen_index, parsed_sentence in enumerate(structured_conversation):
        
        sent_words = []
        for row in parsed_sentence:
            sent_words.append(row[0])
        sent_words_copy = copy.copy(sent_words)

        # Passing the sentence to function that detects and resolves Ellipsis
        all_conversation_vpe.extend(detect_resolve_vpe_sentence(sent_words_copy, sents_arr, parsed_sentence, sen_index, structured_conversation, sentence_speakers_list, output_file, temp_entry_output_storage_file))
        
    return all_conversation_vpe

def detect_resolve_vpe_conversation_spacy(conversation, output_file, temp_entry_output_storage_file):
    structured_conversation, sentence_speakers_list, sents_arr = structure_conversation_spacy(conversation)
    
    all_conversation_vpe = []
    
    for sen_index, parsed_sentence in enumerate(structured_conversation):
        
        sent_words = []
        for row in parsed_sentence:
            sent_words.append(row[0])
        sent_words_copy = copy.copy(sent_words)

        # Passing the sentence to function that detects and resolves Ellipsis
        all_conversation_vpe.extend(detect_resolve_vpe_sentence(sent_words_copy, sents_arr, parsed_sentence, sen_index, structured_conversation, sentence_speakers_list, output_file, temp_entry_output_storage_file))
        
    return all_conversation_vpe