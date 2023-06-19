from helper_functions.sentence_type_categorizer import check_tag_question, check_question

# Function to check whether the Encountered 'To be' type helper verb in the sentence is an ellipsis licensor or not 
def To_Be(Parsed, row_index, sen_srl):
    
    row = Parsed[row_index] # Word, Parent, Dependency Relation, POS Tag and Lemma details for the 'To Be' type helper verb is stored in 'row' variable
    Parsed_l = len(Parsed) # Length of Parsed array would essentially mean length of all tokens in the sentence (The code treats each line as a sentence, so if multiple sentences are in a line, this code fails)
    ellipsis = True # We first assume the helper verb as an indicator of Ellipsis and then apply the rules to see if our assumption is True or not
    parent = (int)(row[1]) # Index of Parent Node.
        
    sent_type = "normal"
    # RULE: If The sentence is a tag type question and the 'To be' aux is at the third last or the fourth last position (negation cases) in the Tag question then it is a Licensor
    if check_tag_question(Parsed):
        sent_type = "tag"
        if row_index == len(Parsed)-3 or row_index == len(Parsed)-4:
            ellipsis = True
            return 1
    elif check_question(Parsed):
        sent_type = "question"
    
    # Note: 'parent-1' is done as Stanford Parser indexing starts from 1 (0th index is Root), but list's indexing starts from 0
    
    # RULE: If ['To be' verb's dependency relation with its parent is that of an auxiliary (i.e. It is not the main verb)] and [if its parent is either a verb or an adverb] then the 'To be' verb isn't a licensor. 
    if(row[2].startswith('aux') and (Parsed[parent-1][3].startswith('VB') or Parsed[parent-1][3].startswith('RB') or Parsed[parent-1][3].startswith('IN'))):
        ellipsis = False
         
    # RULE: If 'To be' verb's dependency relation with its parent is 'cop' then it is not a Licensor. (That is if the 'To be' verb acts as a copula then it is not a Licensor)
    if(row[2] == 'cop'):
        ellipsis = False
    
    # RULE: If 'To be' verb's dependency relation with its parent verb is that of a conjunct then it is not a Licensor
    if (row[2] == 'conj'):
        ellipsis = False
    
    if(row[2] == 'ROOT'):
        
        # RULE: If the 'To be' root verb has a child such that it is an adverbial modifier and there are no further object-like entities then it is not a licensor if and only if SRL Tagger marks the adverbial modifier as ARG2.
        # If the adverbial modifier is marked as an Adverbial Modifier even by the SRL Tagger then the 'To be' root verb is a licensor
        
        # E.g. "I am too.", "It sure was." will be marked as sentences with Ellipsis but sentences like "He is ahead.", "Here you are." will not be marked as cases of Ellipsis
        
        adv_mod_flag = False
        obj_attr_flag = False
        
        for i in range(0, Parsed_l):
            if ((int)(Parsed[i][1]) - 1 == row_index and (Parsed[i][2] == 'advmod' and Parsed[i][4] != 'not' and Parsed[i][3] != 'WRB')):
                for srl_verb in sen_srl['verbs']:
                    if (srl_verb['verb'] == row[0] and 'ARGM-ADV' in srl_verb['tags'][i]):
                        adv_mod_flag = True
                    
                    if (srl_verb['verb'] == row[0] and 'ARG2' in srl_verb['tags'][i]):
                        obj_attr_flag = True #If it is marked as ARG2 then it acts like an object like adverbial modifier to the 'To Be' Root verb.
            
            if ((int)(Parsed[i][1]) - 1 == row_index and (Parsed[i][2] == 'amod' or Parsed[i][2] == 'acomp' or Parsed[i][2] == 'ccomp' or Parsed[i][2] == 'xcomp' or Parsed[i][2] == 'attr' or 'obj' in Parsed[i][2] or 'tmod' in Parsed[i][2])):
                obj_attr_flag = True
                
        if adv_mod_flag and not obj_attr_flag:
            ellipsis = True
            return 1
                
        # RULE: If the 'To be' root verb has a child such that is an adjectival modifier/Wh-adverb OR an object (direct or object to a preposition) / attribute / adjectivial complement / clausal complement / open clausal complement to it then it is not a Licensor.
        for i in range(0, Parsed_l):
            if ((int)(Parsed[i][1]) - 1 == row_index and (Parsed[i][2] == 'amod' or (Parsed[i][2] == 'advmod' and Parsed[i][3] == 'WRB') or Parsed[i][2] == 'acomp' or Parsed[i][2] == 'ccomp' or Parsed[i][2] == 'xcomp' or Parsed[i][2] == 'attr' or 'obj' in Parsed[i][2])):
                ellipsis = False
        
        # RULE: If the 'To be' root verb has a preposition child that occurs after it such that the preposition also has a prepositional object then the 'To be' verb is not a licensor. 
        # E.g. "Are you in a hurry?", "I am in pain.", "Is he from India?"
        for i in range(row_index, Parsed_l):
            if (int)(Parsed[i][1]) - 1 == row_index and Parsed[i][2] == 'prep':
                prep_index = i
                for j in range(prep_index, Parsed_l):
                    if (int)(Parsed[j][1]) - 1 == prep_index and Parsed[j][2] == 'pobj':
                        ellipsis = False
                        break
            if ellipsis == False:
                break
    
    
    # RULE: If the 'To be' verb has a 'existential there' child with the dependency relation expletive AND it also has a child with the dependency relation of that of either subject/attribute then the 'To be' verb is not a licensor
    # E.g. "There is a chance.", "There aren't enough buses in this city", "Is there a possibility?"
    expl_flag = False
    subj_attr_flag = False
    
    for i in range(0,Parsed_l):
        if (int)(Parsed[i][1]) - 1 == row_index and Parsed[i][2] == 'expl' and Parsed[i][3] == "EX":
            expl_flag = True
        if (int)(Parsed[i][1]) - 1 == row_index and (Parsed[i][2] == 'attr' or Parsed[i][2] == 'nsubj'):
            subj_attr_flag = True
    
    if expl_flag and subj_attr_flag:
        ellipsis = False
    
    # RULE: If 'To be' verb is a child to another verb such that its relation with its parent verb is that of a clausal complement then it is not a Licensor if and only if it has a subject
    # AND has a object like child (it can be an adjectival/adverbial modifier OR an object (direct or object to a preposition)/ attribute / adjectivial complement / clausal complement / open clausal complement)
    
    # E.g. It is a licensor in "I think it is.", "I wish it wasn't." but
    # it is not a licensor in "I think the party is tomorrow.", "I hope the food is great."
    if row[2] == 'ccomp':
        
        subj_flag = False
        obj_flag = False
        for i in range(0, Parsed_l):
            if ((int)(Parsed[i][1]) - 1 == row_index and (Parsed[i][2] == 'amod' or (Parsed[i][2] == 'advmod' and Parsed[i][4] != 'not') or Parsed[i][2] == 'acomp' or Parsed[i][2] == 'ccomp' or Parsed[i][2] == 'xcomp' or Parsed[i][2] == 'attr' or 'obj' in Parsed[i][2] or 'tmod' in Parsed[i][2])):
                obj_flag = True
            if ((int)(Parsed[i][1]) - 1 == row_index and ('subj' in Parsed[i][2])):
                subj_flag = True
        
        if subj_flag and obj_flag:
            ellipsis = False
        
        if ellipsis:
            return 1
    
    # Looping across all the tokens in the sentence
    for i in range(0, Parsed_l):

        # RULE: If the 'To be' verb is a parent to an entity such that, the entity is an object/attribute of the 'To be' verb then it is not a Licensor.
        if((int)(Parsed[i][1]) - 1 == row_index and ('attr' in Parsed[i][2] or 'obj' in Parsed[i][2])): 
            ellipsis = False
        
        # RULE: If the 'To be' verb is a parent to an entity such that, the entity is a temporal modifier child to it and the entity occurs after the 'To be' verb in the sentence then it is not a licensor.
        if((int)(Parsed[i][1]) - 1 == row_index and 'tmod' in Parsed[i][2] and i > row_index): 
            ellipsis = False
        
        # RULE: If the 'To be' verb is a parent to an entity such that, the entity is an adverbial modifier of the 'To be' verb then it is not a Licensor. 
        # This rule is executed after checking for 'To be' root verb such that it has only the Adverbial modifier children marked by SRL tagger. So this rule works on the rest of the cases with Adverbs.
        # Therefore, this will mark "Here we are." as case where there is no Ellipsis but "Yes, we are." will be marked as a case of Ellipsis
        if((int)(Parsed[i][1]) - 1 == row_index and Parsed[i][2] == 'advmod' and Parsed[i][-1] != 'not'): 
            ellipsis = False

        # RULE: If the 'To be' verb is a parent to an entity such that, the dependency relation between the entity and the 'To be' verb is that of either a Clausal Complement (ccomp) or an Open Clausal Complement (xcomp) then it is not a licensor.
        if((int)(Parsed[i][1]) - 1 == row_index and Parsed[i][2].endswith('comp')): # Example Sentence where this rule applies: "It used to be that you coudn't..."
            ellipsis = False
        
        # NEW TEST RULE (BROUGHT BACK OLD DELETED RULE): If there is a Verb in the sentence whose relation to its parent is that of Open Clausal Complement then the 'To be' Verb is not a Licensor. (Note: Here the parent doesn't have to be the current 'To be' verb)
        if(Parsed[i][3].startswith('VB') and Parsed[i][2] == 'xcomp'):
            ellipsis = False
        
        # RULE: If the ['To be' Verb's dependency relation with its parent is that of Clausal Complement or Open Clausal Complement] and [the 'To be' verb is parent to an entity such that, the entity is a subject of the 'To be' verb] then the 'To be' Verb isn't a Licensor.
#         if(row[2].endswith('comp') and (int)(Parsed[i][1]) - 1 == row_index and Parsed[i][2].startswith('nsubj')): # Example Sentence where this rule applies: "They say that there is a dog..."
#             ellipsis = False
    
    # Return 0 if 'To be' verb is not a Licensor and 1 if it is a licensor.
    if(ellipsis):
        return(1)
    return(0)