from helper_functions.sentence_type_categorizer import check_tag_question, check_question

# Function to check whether the Encountered 'To have' type helper verb in the sentence is an ellipsis licensor or not 
def To_Have(Parsed, row_index):

    # List of 'To be' type helper verbs
    # NOTE: "'m", "were", "weren't" ADDED LATER (MOSTLY SHOULDN"T AFFECT THE RULES AS WE MOSTLY NEED ONLY BE AND BEEN FOR THE RULE)
    Indicator_To_Be = ["is", "isn’t","be", "been", "was", "wasn’t", "am", "ain’t", "are", "aren’t", "'m", "were", "weren't", "'re"] #NEW_CHANGE - Added 'm
    
    Parsed_l = len(Parsed) # Length of Parsed array would essentially mean length of all tokens in the sentence (The code treats each line as a sentence, so if multiple sentences are in a line, this code fails)
    row = Parsed[row_index] # Word, Parent, Dependency Relation, POS Tag and Lemma details for the 'To Be' type helper verb is stored in 'row' variable
    ellipsis = True # We first assume the helper verb as an indicator of Ellipsis and then apply the rules to see if our assumption is True or not
    parent = (int)(row[1]) # Index of Parent Node.
    
    sent_type = "normal"
    
    # RULE: If The sentence is a tag type question and the 'To have' aux is at the third last or the fourth last position (negation cases) in the Tag question then it is a Licensor
    if check_tag_question(Parsed):
        sent_type = "tag"
        if row_index == len(Parsed)-3 or row_index == len(Parsed)-4:
            ellipsis = True
            return 1
    elif check_question(Parsed):
        sent_type = "question"
        
    # PARSER ERROR RULE: Both spacy and Stanford parsers are sometimes marking subjects of a 'To Have' verb as objects in cases of a Tag question and therefore those 'To have' verbs are not detected as licensors
    # and in fact, even the sentence is not detected as a Tag question. A separate Fix rule below is being added to handle these Parser errors.
    
    # PARSER ERROR FIX RULE: Check for Tag Question manually. If the 'To have' licensor within the tag question has an object like child but doesn't have a subject, it mostly means that the parser has erroneously marked the subject as an object and the 'To have' verb in the tag question is a licensor.
    # RULE: If the sentence ends with a question mark/exclamation mark and the the second last token is a Pronoun/'There' such that its parent is one of the AUX licensors AND that AUX occurs after a comma such that the AUX doesn't have an object/attribute like child then the sentence is a Tag Question.
    if (Parsed[-1][0] == '?' or Parsed[-1][0] == '!') and Parsed[-2][3] == 'PRP' and int(Parsed[-2][1])-1 == row_index and Parsed[int(Parsed[-2][1])-2][0] == ',':
        sent_type = "tag"
        
        if row_index > int(Parsed[-2][1])-2:
            tag_subj_flag = False
            tag_obj_flag = False
            
            for i in range(int(Parsed[-2][1])-2, Parsed_l):
                if 'obj' in Parsed[i][2]:
                    tag_obj_flag = True
                if 'subj' in Parsed[i][2]:
                    tag_subj_flag = True
        
        if not(tag_obj_flag and tag_subj_flag):
            ellipsis = True
            return 1

    # Note: 'parent-1' is done as Stanford Parser indexing starts from 1 (0th index is Root), but list's indexing starts from 0
    
    # RULE: If ['To have' verb's dependency relation with its parent is that of an auxiliary (i.e. It is not the main verb)] and ['To have' verb's parent is either a Verb or an Adjective or an Adverb] then it is not a Licensor.
    if(row[2].startswith('aux') and (Parsed[parent-1][3].startswith('VB') or Parsed[parent-1][3].startswith('JJ') or Parsed[parent-1][3].startswith('RB'))):# Example Sentence where this rule applies: "... has eaten ..."
        ellipsis = False
    
    # RULE: If 'To have' verb's dependency relation with its parent is that of an auxiliary (i.e. It is not the main verb) and its parent is a 'To be' type helper verb then it is not a Licensor. 
    if(row[2]=='aux' and Parsed[parent-1][0] in Indicator_To_Be): 
        #Note: 'has been eating' - This ellipsis has been handled in To_Be()
        #Example Sentence where this rule applies: In 'I haven't been' haven't is an aux child of 'been'. In 'I haven't been shopping', it is an aux child of VBG 'shopping', and so ellipsis is ruled out by above condition.
        ellipsis = False
    
    if(row[2] == 'ROOT'):
        
        # RULE: If 'To have' verb is the ROOT in the sentence and it has a negation adverbial modifier child then it is a licensor.
        # E.g "I have not.", "I haven't.", "It hasn't." (This is so because if the 'To have' verb is a root verb then it has to be the possessive verb have and not an auxilliary to another main verb 
        # and when we want to negate that possessive 'To have' verb we use a "don't" and not a "not", hence making the "To have" verb a licensor in this particular pattern.) 
        for i in range(row_index, Parsed_l):
            if ((int)(Parsed[i][1])-1 == row_index and (Parsed[i][-1] == "not" or Parsed[i][-1] == "n't")):
                ellipsis = True
                return 1
        
        # NEW TEST RULE: If 'To have' verb is the ROOT in the sentence AND it has an Object then it is not a Licensor.
        for i in range(0, Parsed_l):
            if((int)(Parsed[i][1])-1 == row_index and 'obj' in Parsed[i][2]): # Example Sentence where this rule applies: "has apples", "What an amazing skirt you have on."
                ellipsis = False
    
    # RULE: If 'To have' verb is a child to another verb such that the dependency relation between them is that of conjunct in the sentence and it has a negation adverbial modifier child then it is a licensor.
    # NOTE: This would work because if the 'To have' verb acts is linked to another as a conjunct then it behaves similar to the case wherein it is the sole root verb and if negation not is added after it then it
    # means that it is not the possessive verb have but is acting as an aux for an ellided verb
    
    # E.g.: "I kept telling you that I would treat you to dinner but I still haven't ."
    if row[2] == 'conj':
        for i in range(row_index, Parsed_l):
            if ((int)(Parsed[i][1])-1 == row_index and (Parsed[i][-1] == "not" or Parsed[i][-1] == "n't")):
                ellipsis = True
                return 1
        
    
    # NEW TEST RULE: If 'what' is an object of the 'To have' verb such that it occurs before the 'To have' verb in the sentence then the 'To Have' verb is not a licensor.
    # E.g. "What would you like to have?"
    for i in range(0, row_index):
        if ((int)(Parsed[i][1])-1 == row_index and 'obj' in Parsed[i][2] and Parsed[i][3] == 'WP'):
            ellipsis = False
    
    # NEW TEST RULE: If an entity is an object of the 'To have' verb such that it occurs before the 'To have' verb in the sentence then the 'To Have' verb is not a licensor.
    # E.g. "What soup would you like to have?"
    for i in range(0, row_index):
        if ((int)(Parsed[i][1])-1 == row_index and 'obj' in Parsed[i][2]):
            ellipsis = False
    
    # RULE: If the 'To Have' verb has a parent such that it is a noun and is linked to it with the relative clause dependency then it is not a licensor.
    # E.g. " Actually it was the most interesting day I've had so far .", "I live in London, which has some fantastic parks."
    if 'relcl' in row[2] and 'NN' in Parsed[int(row[1])-1][3]:
        ellipsis = False
    
    # Looping on tokens that occur after the 'To have' in the sentence
    for i in range(row_index, Parsed_l):

        # RULE: If 'To have' verb is parent to an entity (that occurs after it in the sentence) such that, the entity is an object to the 'To have' verb then it is not a Licensor.
        if((int)(Parsed[i][1])-1 == row_index and 'obj' in Parsed[i][2]): # Example Sentence where this rule applies: "has apples"
            ellipsis = False
        
        # NEW TEST RULE: If 'To have' verb is parent to an entity (that occurs after it in the sentence) such that, the dependency relation between the entity and the 'To have' verb is that an Clausal Complement (ccomp/xcomp) then it is not a Licensor.
        if((int)(Parsed[i][1])-1 == row_index and Parsed[i][2].endswith('comp')): # Example Sentence where this rule applies: "has to go shopping" 
            ellipsis = False
        
        # RULE: If 'To have' verb is parent to an entity (that occurs after it in the sentence) such that, the entity is either a Pronoun or a Noun, then it is not a Licensor.
        if((int)(Parsed[i][1])-1 == row_index and (Parsed[i][2].startswith('PR') or Parsed[i][2].startswith('NN'))): # Example Sentence where this rule applies: "has apples" or "has it"
            ellipsis = False
    
    # Return 0 if 'To be' verb is not a Licensor and 1 if it is a licensor.
    if(ellipsis):
        return(1)
    return(0)