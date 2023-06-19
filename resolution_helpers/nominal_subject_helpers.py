def extract_nominal_subject_verb(Parsed, verb_index):
    
    real_index = verb_index
    noun_subject_row = -1
    noun_subject = -1

    if(Parsed[real_index][2].endswith('comp') or Parsed[real_index][2].endswith('conj')):
        subject_exists = True
        while(subject_exists and noun_subject_row == -1):
            for row in Parsed:
                if((int)(row[1]) - 1 == real_index and row[2].startswith('nsubj')):
                    noun_subject_row = row
                    subject_exists = False
                    break
            if(Parsed[real_index][3].startswith('VB') and (Parsed[real_index][2].endswith('comp') or Parsed[real_index][2].endswith('conj'))):
                real_index = int(Parsed[real_index][1]) - 1
            else:
                subject_exists = False
	#Routine for others
    else:
        for row in Parsed:
            if(int(row[1]) - 1 == real_index and row[2].startswith('nsubj')):
                noun_subject_row = row
    
    
    # Step 9: IF Nominal Subject is found in above steps do the following
    if(noun_subject_row != -1):
        # Step 9.1: If POS Tag of currently identified nominal subject is either Wh determiner / Wh Pronoun / Wh adverb 
        # AND has a dependency relation of relative clause (acl:relcl) with its parent, 
        # then the actual Nominal Subject is its parent in the dependency tree.
        # (i.e. Find subject of adjective clause)
        if(noun_subject_row[3].startswith('W') and 'relcl' in Parsed[real_index][2]):
            parent_noun = int(Parsed[real_index][1]) - 1
            noun_subject_row = Parsed[parent_noun]
        
        # Step 9.2: Store Noun subject name in variable 'noun_subject'
        noun_subject = noun_subject_row[0]
    
    return noun_subject, noun_subject_row

def extract_nominal_subject_details(Parsed, noun_subject_row, noun_subject, row_index):
    
    first_person_pronouns = ["i", "me", "we", "us", "mine", "ours", "myself", "ourselves"]
    second_person_pronouns = ["you", "yours", "yourself", "yourselves"]
    third_person_pronouns = ["he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves"]
    
    number = -1
    proper = -1
    passive = -1
    person = 0
    pronoun_flag = 0
    
    if noun_subject_row == -1:
        return number, person, pronoun_flag, passive, proper
    
    # Extracting person details (1st/2nd/3rd person or not) of the nominal subject
    if noun_subject_row != -1:
        if noun_subject in first_person_pronouns:
            person = 1
            pronoun_flag = 1
        elif noun_subject in second_person_pronouns:
            person = 2
            pronoun_flag = 1
        elif noun_subject in third_person_pronouns:
            person = 3
            pronoun_flag = 1
        else:
            person = 3
            pronoun_flag = 0
    
    # Extracting Passivity of nominal subject
    if(noun_subject_row[2].endswith('pass')):
        passive = 1
    else:
        passive = 0

    # Step 9.4: Finding whether the Nominal Subject is Singular or Plural. 
    # If plural then flag variable 'number' is marked with 1

    # Step 9.4.1: Here we are handling Noun-Determiner Phrases. If currently identified nominal subject is a Determiner
    # then we look for all tokens in the Parsed sentence. IF we find a token such that its parent is the aforementioned determiner
    # with nmod relation with it and such that the index of the token is less that that of the current licensor,
    # then we check whether that token (nominal token) is singular or not. 
    # [I think the condition should be identified to see if is a child to noun, but not a parent, but I may be wrong]
    if(noun_subject_row[3].startswith('DT')):
        for r in range(len(Parsed)):
            if((int)(Parsed[r][1]) - 1 == Parsed.index(noun_subject_row) and Parsed[r][2].startswith('nmod') and r < row_index):
                if(Parsed[r][3].endswith('S') or Parsed[r][4] == 'they' or Parsed[r][4] == 'we'):
                    number = 1
                else:
                    number = 0
                break

    # Step 9.4.2: When Nominal subject is independent [I think], then we can directly check for plurality and mark the flag value correspondingly.
    if(number == -1):
        if(noun_subject_row[3].endswith('S') or noun_subject_row[4] == 'they' or noun_subject_row[4] == 'we'):
            number = 1
        else:
            number = 0

    # Step 9.5: Here we are handling Conjugate nouns. [Multiple individual nouns linked together with conjunctions/punctuations]
    conj_exists = False
    for row in Parsed:
        # Step 9.5.1: For all tokens in Parsed, see if Nominal Subject is parent to the token 
        # AND see if the relation between them is that of coordinating conjunction (cc) 
        # AND see if the conjunction itself is 'and'
        # then Conjugate noun exists
        if(int(row[1]) - 1 == Parsed.index(noun_subject_row) and row[2].startswith('cc') and row[4].startswith('and')):
            conj_exists = True

        # Step 9.5.2: For all tokens in Parsed, see if Nominal subject is parent to the token
        # AND see if the relation between them is that of conjunction (conj)
        # AND see if the POS Tag of the token is either a Noun or Personal Pronoun
        # within it see if conjugate exists
        # then the number of Nominal Subject is Plural and we change thr flag value accoridngly.
        if(int(row[1]) - 1 == Parsed.index(noun_subject_row) and row[2].startswith('conj') and (row[3].startswith('N') or row[3].startswith('PRP'))):
            if(conj_exists):
                number = 1

    # Step 9.6: Here we are checking the Properness i.e IF Nominal Subject is a proper noun or not.
    if(noun_subject_row[3].endswith('NP') or noun_subject_row[3].endswith('NPS')):
        proper = 1
    else:
        proper = 0
    
    return number, person, pronoun_flag, passive, proper