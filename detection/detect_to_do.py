from helper_functions.sentence_type_categorizer import check_tag_question, check_question

# Function to check whether the Encountered 'To do' type helper verb in the sentence is an ellipsis licensor or not 
def To_Do(Parsed, row_index):
    
    Parsed_l = len(Parsed) # Length of Parsed array would essentially mean length of all tokens in the sentence (The code treats each line as a sentence, so if multiple sentences are in a line, this code fails)
    row = Parsed[row_index] # Word, Parent, Dependency Relation, POS Tag and Lemma details for the 'To Be' type helper verb is stored in 'row' variable
    ellipsis = True # We first assume the helper verb as an indicator of Ellipsis and then apply the rules to see if our assumption is True or not
    parent = (int)(row[1]) # Index of Parent Node. 
    
    sent_type = "normal"
    
    # RULE: If The sentence is a tag type question and the 'To Do' aux is at the third last or the fourth last position (negation cases) in the Tag question then it is a Licensor
    if check_tag_question(Parsed):
        sent_type = "tag"
        if row_index == len(Parsed)-3 or row_index == len(Parsed)-4:
            ellipsis = True
            return 1
    elif check_question(Parsed):
        sent_type = "question"
    
    # Note: 'parent-1' is done as Stanford Parser indexing starts from 1 (0th index is Root), but list's indexing starts from 0
    
    #NEW_CHANGE: New rule added:
    # RULE: If punctuations ',', '.', ';', '!', '?' occur right after the specific aux verb "Do" and there is no auxiliary child to it then it is a Licensor.
    # E.g. "I didn't <<>>.", "We did <<>>, but they didn't pick our calls."
    if ((row_index != Parsed_l-1) and (Parsed[row_index+1][0] in ['.', ',', ';', '?', '!'])):
        
        # This is specially done to to handle the only special case where do acts like an intransitive verb 
        # For e.g. "This dress will do.", "That hammer type should do."
        for i in range(0, row_index):
            if(row[0] == 'do' and Parsed[i][2] == 'aux' and int(Parsed[i][1]) - 1 == row_index): 
                ellipsis = False
        
        if ellipsis:
            return 1 # RULE: If above condition is not true only then apply the remaining rules below.
    
    # RULE: If the 'To do' verb has a relative clause dependency relation with it's parent verb then it is not a modifier.
    # E.g. 'Shall I learn the actions that Jet Li did in the movies ?'
    if 'relcl' in row[2]:
        ellipsis = False

    # RULE: If the 'To_Do' aux verb has an auxiliary child then it is a main verb and not a licensor E.g. - "What can I do for you?"
    for i in range(0, row_index):
            if(Parsed[i][2] == 'aux' and int(Parsed[i][1]) - 1 == row_index):
                ellipsis = False

    # RULE: If 'To do' verb's dependency relation with its parent is that of an auxiliary (i.e. It is not the main verb) and its parent is a Verb then it is not a Licensor.
    if(row[2]=='aux' and Parsed[parent-1][3].startswith('VB')): # Example Sentence where this rule applies: "does care"
        ellipsis = False

    # Looping on all tokens that occur after the 'To do' verb
    for i in range(0, Parsed_l):

        # RULE: If 'To do' verb is parent to an entity such that, the entity is an object to the 'To do' verb then it is not a Licensor.
        if('obj' in Parsed[i][2] and (int)(Parsed[i][1])-1 == row_index): # Example sentence where this rule applies: "does his homework."
            ellipsis = False

    # RULE: If 'To do' verb has POS Tag of 'VB' (i.e. Base form Verb) and it is parent to an entity (that occurs after it in the sentence) such that the entity has 'TO' POS tag (i.e. the entity itself is 'to') then it is not a Licensor.
    if(row[3] == 'VB'): # This is for cases with Infinitive form - "to do".
        
        # Looping on all tokens that occur after the 'To do' verb, the loop is also mentioned indirectly in the above condition.
        for i in range(row_index, Parsed_l):

            # Note: Above written rule encompasses this If condition
            if((int)(Parsed[i][1])-1 == row_index and Parsed[i][3].casefold() == 'TO'.casefold()):
                ellipsis = False
                
    # Return 0 if 'To be' verb is not a Licensor and 1 if it is a licensor.
    if(ellipsis): 
        return(1)
    return(0)