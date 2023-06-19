import re

# Function to recursively find child tokens of the object tokens found for the resolved head verb. 
# The function will recursively look for children before the current object's index and then after the current object's index
# and it does so separately. These are both combined in the child_tokens array and are then returned.
def obj_children_recursive(obj_index, parsed_resolution_sentence, child_tokens):
    
    curr_index = 0
    
    while curr_index < obj_index:
        if int(parsed_resolution_sentence[curr_index][1])-1 == obj_index and (parsed_resolution_sentence[curr_index][2] == 'amod' or parsed_resolution_sentence[curr_index][2] == 'nmod' or parsed_resolution_sentence[curr_index][2] == 'nummod' or parsed_resolution_sentence[curr_index][2] == 'det' or parsed_resolution_sentence[curr_index][2] == 'compound' or parsed_resolution_sentence[curr_index][2] == 'compound:prt' or parsed_resolution_sentence[curr_index][2] == 'prt' or parsed_resolution_sentence[curr_index][2] == 'poss'):
            child_tokens = [curr_index] + obj_children_recursive(curr_index, parsed_resolution_sentence, child_tokens)
        curr_index += 1
    
    curr_index += 1
    
    while curr_index > obj_index and curr_index < len(parsed_resolution_sentence):
        if int(parsed_resolution_sentence[curr_index][1])-1 == obj_index and (parsed_resolution_sentence[curr_index][2] == 'amod' or parsed_resolution_sentence[curr_index][2] == 'nmod' or parsed_resolution_sentence[curr_index][2] == 'nummod' or parsed_resolution_sentence[curr_index][2] == 'prep' or parsed_resolution_sentence[curr_index][2] == 'compound' or parsed_resolution_sentence[curr_index][2] == 'compound:prt' or parsed_resolution_sentence[curr_index][2] == 'prt' or parsed_resolution_sentence[curr_index][2] == 'pobj'):
            child_tokens = obj_children_recursive(curr_index, parsed_resolution_sentence, child_tokens) + [curr_index]
        curr_index += 1
        
    return child_tokens    

# Function to extract the objects for the resolved head verb. 
def extract_head_verb_object(final_vpe_list, structured_conversation):

    parsed_conversation = structured_conversation[0]
    speakers = structured_conversation[1]
    
    first_to_second_person_pronouns = {
        "me": "you",
        "we": "you",
        "us":"you",
        "mine":"yours",
        "ours":"yours",
        "myself":"yourself",
        "ourselves":"yourselves",
        "my": "your",
        "your":"my",
        "yours": "mine"
    }
    
    for vpe_index, vpe in enumerate(final_vpe_list):
        
        resolution_site = None
        resolution_sen_index = None

        # Do the following only if it is a pure case of ellipsis and not an object only ellipsis case
        if vpe['resolved_head_verb'] is None and vpe['ellided_obj_child_parent_verb'] is None:
            continue

        elif vpe['resolved_head_verb'] is None and vpe['ellided_obj_child_parent_verb'] is not None:
            
            resolution_site = vpe['ellided_obj_child_parent_verb']
            if vpe['sen_type'] == 4 or vpe['sen_type'] == 1:
                resolution_sen_index = vpe['sen_index']
         
            elif vpe['sen_type'] == 2 or vpe['sen_type'] == 3:
                resolution_sen_index = vpe['sen_index']-1
        
        elif vpe['resolved_head_verb'] is not None and vpe['ellided_obj_child_parent_verb'] is None:
            resolution_site = vpe['resolved_head_verb_site']
            resolution_sen_index = vpe['resolved_head_verb_sen_index']

        parsed_resolution_sen = parsed_conversation[resolution_sen_index]
        vpe_sen_index = vpe['sen_index']
        
        obj_list = []
        obj_indices = []
        
        # Finding direct objects to the resolved head verb 
        for token_index, parsed_token in enumerate(parsed_resolution_sen):
            if int(parsed_token[1])-1 == resolution_site and (parsed_token[2] == 'cop' or parsed_token[2] == 'dobj' or parsed_token[2] == 'attr' or parsed_token[2] == 'prt' or parsed_token[2] == 'prep' or parsed_token[2] == 'acomp'):
                if parsed_token[0].casefold() in first_to_second_person_pronouns:
                    if speakers[vpe_sen_index] != speakers[resolution_sen_index]:
                        obj_list.append(first_to_second_person_pronouns[parsed_token[0].casefold()])
                        obj_indices.append(token_index)
                    else:
                        obj_list.append(parsed_token[0])
                        obj_indices.append(token_index)
                else:
                    obj_list.append(parsed_token[0])
                    obj_indices.append(token_index)
        
        combined_list = []
        combined_list.extend(x for x in obj_indices if x not in combined_list)
        
        # Recursively finding children to the direct object tokens from within the sentence
        # Combining both the direct objects and their child dependents into a list and then sorting them to get them in the right order
        # We also remove duplicates if in case they are there
        for i in range(0, len(obj_list)):
            combined_list.extend(x for x in obj_children_recursive(obj_indices[i], parsed_resolution_sen, []) if x not in combined_list)
        
        combined_list.sort()
        resolved_object = ""
        
        # Combining the object tokens into a single string using their indices
        for i in combined_list:
            if parsed_resolution_sen[i][0].casefold() in first_to_second_person_pronouns and speakers[vpe_sen_index] != speakers[resolution_sen_index]:
                resolved_object = resolved_object + " " + first_to_second_person_pronouns[parsed_resolution_sen[i][0].casefold()]
            else:
                resolved_object = resolved_object + " " + parsed_resolution_sen[i][0]
                
        final_vpe_list[vpe_index]['resolved_object'] = re.sub(" +", " ", resolved_object.strip())
        
        # Combining the head verb with the object to make the verb phrase
        combined_list.append(resolution_site)
        combined_list.sort()
        resolved_verb_phrase = ""
        
        for i in combined_list:
            if parsed_resolution_sen[i][0].casefold() in first_to_second_person_pronouns and speakers[vpe_sen_index] != speakers[resolution_sen_index]:
                resolved_verb_phrase = resolved_verb_phrase + " " + first_to_second_person_pronouns[parsed_resolution_sen[i][0].casefold()]
            else:
                resolved_verb_phrase = resolved_verb_phrase + " " + parsed_resolution_sen[i][0]
                
        final_vpe_list[vpe_index]['resolved_verb_phrase'] = re.sub(" +", " ", resolved_verb_phrase.strip())
        
        
    return final_vpe_list