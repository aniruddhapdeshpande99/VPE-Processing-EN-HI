def check_tag_question(Parsed):
    len_sen = len(Parsed)
    
    # Creating separate lists of the potential licensors of Ellipsis. 
    # Each list consists of helper/aux verbs of a different class. These occur mosyt frequently at the site of Ellipsis
    Indicator_To_Be = ["is", "isn’t","be", "been", "was", "wasn’t", "am", "ain’t", "are", "aren’t", "'m", "were", "weren't", "'re"] 
    Indicator_To_Have = ["has", "hasn’t", "have", "had", "'d", "'ve"] 
    Indicator_To_Do = ["does", "doesn’t", "do", "don’t", "did"]
    Indicator_Modals = ["will", "wo", "would", "may", "might", "must", "can", "ca", "could", "should", "shall", "shan't", "'d", "'ll"]
    
    aux_licensors = Indicator_To_Be
    aux_licensors.extend(Indicator_To_Have)
    aux_licensors.extend(Indicator_To_Do)
    aux_licensors.extend(Indicator_Modals)
    
    # RULE: If the sentence ends with a question mark/exclamation mark and the the second last token is a Pronoun/'There' such that its parent is one of the AUX licensors AND that AUX occurs after a comma such that the AUX doesn't have an object/attribute like child then the sentence is a Tag Question.
    if (Parsed[-1][0] == '?' or Parsed[-1][0] == '!') and (Parsed[-2][3] == 'PRP' or Parsed[-2][-1] == 'there') and Parsed[int(Parsed[-2][1])-1][0] in aux_licensors and Parsed[int(Parsed[-2][1])-2][0] == ',':
        
        # This eliminates the questions with just an interjection followed by a comma and the short question that resembles a tag question
        # E.g. "Oh, must I?" and "Ah, is it?"
        if Parsed[0][3] == 'UH' and int(Parsed[-2][1])-2 == 1:
            return False
        
        # Checking if the AUX has a child object/attribute or not
        # E.g. "Holly, Is that you?" is not a tag question even if it fits the above pattern because 'that' is an attribute child of 'Is'
        aux_index = int(Parsed[-2][1])-1
        for i in range(aux_index, len_sen):
            if (int)(Parsed[i][1]) - 1 == aux_index and (Parsed[i][2] == 'attr' or 'obj' in Parsed[i][2]):
                return False
        
        # If no child object/attribute found for the AUX then it is a Tag question
        return True
    else:
        return False

def check_question(Parsed):
    if (Parsed[-1][0] == '?'):
        return True
    else:
        return False

def check_wh_question(Parsed):
    if (Parsed[-1][0] == '?') and Parsed[0][3] == 'WRB':
        return True
    else:
        return False