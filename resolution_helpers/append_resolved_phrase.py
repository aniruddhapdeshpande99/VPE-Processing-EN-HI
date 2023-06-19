from helper_functions.helpers import structure_conversation_spacy, Parse_spacy
import re

def append_resolved_vp(final_vpe_list, conversation):
    structured_conversation, sentence_speakers_list, sents_arr = structure_conversation_spacy(conversation)
    sents_arr_copy = sents_arr
    structured_conversation_copy = structured_conversation

    for vpe in final_vpe_list:
        
        if vpe['resolved_head_verb'] is None and vpe['ellided_obj_child_parent_verb'] is None:
            continue
        
        if vpe['resolved_head_verb'] is not None and vpe['ellided_obj_child_parent_verb'] is None:
            
            site = vpe['site']
            sen_index = vpe['sen_index']
            Parsed_vpe_sen = structured_conversation[sen_index]
            tokens  = []

            if vpe['sen_type'] < 3:

                for index, curr_token in enumerate(Parsed_vpe_sen):
                    if index == site + 1 and curr_token[2] != 'neg':

                        if 'resolved_aux' in vpe:
                            tokens.append(vpe['resolved_aux'])

                        tokens.append(vpe['resolved_head_verb'].casefold())
                        tokens.append(vpe['resolved_object'])
                        tokens.append(curr_token[0])
                    elif index == site + 1 and curr_token[2] == 'neg':
                        tokens.append(curr_token[0])
                        
                        if 'resolved_aux' in vpe:
                            tokens.append(vpe['resolved_aux'])
                        
                        tokens.append(vpe['resolved_head_verb'].casefold())
                        tokens.append(vpe['resolved_object'])
                    else:
                        tokens.append(curr_token[0])

            else:
                for index, curr_token in enumerate(Parsed_vpe_sen):
                    if index == site + 2 and Parsed_vpe_sen[index - 1][2] != 'neg' :
                        tokens.append(vpe['resolved_head_verb'].casefold())
                        tokens.append(vpe['resolved_object'])
                        tokens.append(curr_token[0])
                    elif index == site + 2 and Parsed_vpe_sen[index - 1][2] == 'neg' :
                        tokens.append(curr_token[0])
                        tokens.append(vpe['resolved_head_verb'].casefold())
                        tokens.append(vpe['resolved_object'])
                    else:
                        tokens.append(curr_token[0])
            
            vpe_resolved_sen = " ".join(tokens).strip()
            sents_arr[sen_index] = re.sub(' +', ' ', vpe_resolved_sen)
            structured_conversation[sen_index] = Parse_spacy(vpe_resolved_sen)
        
        elif vpe['resolved_head_verb'] is None and vpe['ellided_obj_child_parent_verb'] is not None:
            site = vpe['site']
            sen_index = vpe['sen_index']
            Parsed_vpe_sen = structured_conversation[sen_index]
            tokens  = []

            if vpe['sen_type'] < 3:

                for index, curr_token in enumerate(Parsed_vpe_sen):
                    if index == site + 1 and curr_token[2] != 'neg':
                        tokens.append(vpe['resolved_object'])
                        tokens.append(curr_token[0])
                    elif index == site + 1 and curr_token[2] == 'neg':
                        tokens.append(curr_token[0])
                        tokens.append(vpe['resolved_object'])
                    else:
                        tokens.append(curr_token[0])

            else:
                for index, curr_token in enumerate(Parsed_vpe_sen):
                    if index == site + 2 and Parsed_vpe_sen[index - 1][2] != 'neg' :
                        tokens.append(vpe['resolved_object'])
                        tokens.append(curr_token[0])
                    elif index == site + 2 and Parsed_vpe_sen[index - 1][2] == 'neg' :
                        tokens.append(curr_token[0])
                        tokens.append(vpe['resolved_object'])
                    else:
                        tokens.append(curr_token[0])
            
            vpe_resolved_sen = " ".join(tokens).strip()
            sents_arr[sen_index] = re.sub(' +', ' ', vpe_resolved_sen)
            structured_conversation[sen_index] = Parse_spacy(vpe_resolved_sen)
        
    final_resolved_conversation = " ".join(sents_arr).strip()
    final_resolved_conversation = re.sub(' +', ' ', final_resolved_conversation)
    final_resolved_conversation = re.sub(r"\sn't", "n't", final_resolved_conversation)

    return final_resolved_conversation, structured_conversation
                

