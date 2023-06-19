from helper_functions.sentence_type_categorizer import check_tag_question, check_question

# Function to check whether the Encountered 'To' in the sentence is an ellipsis licensor or not 
def To(Parsed, row_index):
    Parsed_l = len(Parsed) # Length of Parsed array would essentially mean length of all tokens in the sentence (The code treats each line as a sentence, so if multiple sentences are in a line, this code fails)
    row = Parsed[row_index] # Word, Parent, Dependency Relation, POS Tag and Lemma details for the 'To Be' type helper verb is stored in 'row' variable
    ellipsis = True # We first assume the helper verb as an indicator of Ellipsis and then apply the rules to see if our assumption is True or not
    parent = (int)(row[1]) # Index of Parent Node.
    
    sent_type = "normal"
    
    # RULE: If The sentence is a tag type question and the 'To' aux is at the third last or the fourth last position (negation cases) in the Tag question then it is a Licensor
    if check_tag_question(Parsed):
        sent_type = "tag"
        if row_index == len(Parsed)-3 or row_index == len(Parsed)-4:
            ellipsis = True
            return 1
    elif check_question(Parsed):
        sent_type = "question"
    
    #NEW_CHANGE: New rule added:
    # RULE: If punctuations ',', '.', ';', '!', '?' occur right after 'To' aux verb then the 'To' aux verb is a Licensor
    if (row_index != Parsed_l-1) and (Parsed[row_index+1][0] in ['.', ',', ';', '?', '!']):
        ellipsis = True
        return 1 # RULE: If above condition is not true only then apply the remaining rule below.

    # RULE: If a conjunction occurs right after 'to' it is a licensor
    if (row_index != Parsed_l-1) and (Parsed[row_index+1][2] == 'cc'):
        ellipsis = True
        return 1
    
    # RULE: If the dependency relation of 'To' with its parent is not that of an Open Clausal Complement then it is not a Licensor.
    if(row[2] != 'xcomp'):
        ellipsis = False
    
    # Return 0 if 'To be' verb is not a Licensor and 1 if it is a licensor.
    if(ellipsis): 
        return(1)
    return(0)