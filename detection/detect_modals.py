from helper_functions.sentence_type_categorizer import check_tag_question, check_question

# Function to check whether the Encountered 'Modals' in the sentence is an ellipsis licensor or not 
def Modals(Parsed, row_index):
    
    # List of 'To be' type helper verbs
    # NOTE: "'m", "were", "weren't" ADDED LATER (MOSTLY SHOULDN"T AFFECT THE RULES AS WE MOSTLY NEED ONLY BE AND BEEN FOR THE RULE)
    Indicator_To_Be = ["is", "isn’t","be", "been", "was", "wasn’t", "am", "ain’t", "are", "aren’t", "'m", "were", "weren't", "'re"] #NEW_CHANGE - Added 'm
    
    Parsed_l = len(Parsed) # Length of Parsed array would essentially mean length of all tokens in the sentence (The code treats each line as a sentence, so if multiple sentences are in a line, this code fails)
    row = Parsed[row_index] # Word, Parent, Dependency Relation, POS Tag and Lemma details for the 'To Be' type helper verb is stored in 'row' variable
    ellipsis = True # We first assume the helper verb as an indicator of Ellipsis and then apply the rules to see if our assumption is True or not
    parent = (int)(row[1]) # Index of Parent Node. 
    
    sent_type = "normal"
    
    # RULE: If The sentence is a tag type question and the Modal aux is at the third last or the fourth last position (negation cases) in the Tag question then it is a Licensor
    if check_tag_question(Parsed):
        sent_type = "tag"
        if row_index == len(Parsed)-3 or row_index == len(Parsed)-4:
            ellipsis = True
            return 1
    elif check_question(Parsed):
        sent_type = "question"
    
    # Note: 'parent-1' is done as Stanford Parser indexing starts from 1 (0th index is Root), but list's indexing starts from 0
    
    # RULE: If a 'Modal' verb is immediately followed by a punctuation mark then it is a licensor of Ellipsis because it would imply that it is acting as an auxilliary for an ellided verb within that clause and hence would prove that the 'Modal' verb is acting as a licensor
    # Reason: Modals exist as independent verbs only in cases when they are licensors of Ellipsis
    # NOTE: This rule was also added to tackle the inconsistencies of Parsers E.g. "Yes, I would, thank you." - Here, there is an ellipsis after 'would' but it is undetected by Spacy as it incorrectly marks 'would' as an aux to 'thank'
    if ((row_index != Parsed_l-1) and (Parsed[row_index+1][0] in ['.', ',', ';', '?', '!'])) or ((row_index != Parsed_l-2) and (Parsed[row_index+2][0] in ['.', ',', ';', '?', '!']) and (Parsed[row_index+1][-1] == 'not')): # Second part after OR is added because we need to handle cases with negation in it.
        ellipsis = True
        return 1
    
    # RULE: If POS Tag of the 'Modal' is a Noun it is not a Licensor. {{DOUBT: Ask about cases wherein a Modal would be given a Noun type POS Tag.}}
    if(row[3].startswith('NN')):
        ellipsis = False
    
    # RULE: If the dependency relation of the 'Modal' with its parent is that of an auxiliary and [its parent is either a Verb (VB) or an adjective (JJ) or a preposition (IN) or a subordinating conjunction (IN) or a cardinal (CD - i.e. numerals)] then it is not a Licensor.
    if(row[2].startswith('aux') and (Parsed[parent-1][3].startswith('VB') or Parsed[parent-1][3].startswith('JJ') or Parsed[parent-1][3].startswith('IN') or Parsed[parent-1][3].startswith('CD'))): # does care, would be no fight #removed parent RB condition
        ellipsis = False
    
    # RULE: If the dependency relation of the 'Modal' with its parent is that of an auxiliary and its parent is a 'To be' type helper verb then it is not a Licensor.
    if(row[2]=='aux' and Parsed[parent-1][0] in Indicator_To_Be): # Example sentence where this rule applies: "would be no fight" cases where aux is child of noun
        ellipsis = False
    
    # RULE: If 'To_be' type aux occurs right after the current 'Modal' type aux and If they both share a parent which is a Noun then the 'Modal' aux is not a licensor. 
    if (row_index != Parsed_l-1) and (Parsed[row_index+1][0] in Indicator_To_Be) and (parent == int(Parsed[row_index + 1][1])) and (Parsed[parent-1][3].startswith('NN')): #Example: "For the last one,  black and white, all the rest should be color ."
        ellipsis = False
    
    # Looping on all tokens that occur after the 'Modal'
    for i in range(row_index, Parsed_l):

        # RULE: If 'Modal' is parent to an entity (that occurs after it in the sentence) such that, the entity is an object to the 'Modal' then it is not a Licensor. {{DOUBT - Can Modals have the dependency relation OBJ (i.e. direct or indirect object) with its children?}}
        if('obj' in Parsed[i][2] and (int)(Parsed[i][1])-1 == row_index): # Example sentence where this rule applies: "does his homework."
            ellipsis = False     
    
    # Return 0 if 'To be' verb is not a Licensor and 1 if it is a licensor.
    if(ellipsis): 
        return(1)
    return(0)