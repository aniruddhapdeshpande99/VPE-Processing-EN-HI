def extract_verb_comp_depth(Parsed, row_index):
    # Step 12.1: Start with the index of the current Licensor. Store it in variable 'key'
    key = row_index
    comp_clause_depth = 0

    # Step 12.2: Check if the current token (with index 'key') is related to its parent by a 
    # Complement type relation and loop on it until the condition is true.
    while(Parsed[key][2].endswith('comp')):
        parent = int(Parsed[key][1]) - 1
        comp_clause_depth += 1
        # Step 12.2.2: Update 'key' with the index of the parent to the current token.
        key = parent
    
    return comp_clause_depth

def extract_verb_aux(Parsed, row_index):
    key = row_index
    auxiliary = 0
    aux_class = 0
    lemmatized_auxiliary = 0
    
    Indicator_To_Be = ["'s", "is", "isn’t","be", "been", "was", "wasn’t", "am", "ain’t", "are", "aren’t", "'m", "were", "weren't", "'re"] #NEW_CHANGE - Added 'm
    Indicator_To_Have = ["has", "hasn’t", "have", "had", "'d", "'ve"] #NEW_CHANGE - Added 'd and 've
    Indicator_To_Do = ["does", "doesn’t", "do", "don’t", "did"]
    Indicator_Modals = ["will", "wo", "would", "may", "might", "must", "can", "ca", "could", "should", "shall", "shan't", "'d", "'ll"] #NEW_CHANGE - Added shall, 'd and 'll
    Indicator_To = ["to"]
    
    if(Parsed[key][4] == 'be'.casefold()) and Parsed[(int)(Parsed[row_index][1]) - 1][3].startswith("VB"):
        key = (int)(Parsed[row_index][1]) - 1

    # Step 14.3: Looping across each token in the sentence we do following
    for row in Parsed:
        # Step 14.4.1: We check IF the Parent to that token is our current Verb from the verb list or not
        if(int(row[1]) - 1 == key):
            # Step 14.4.2: We check IF the token is an AUX or not, IF true then
            if(row[2] == 'aux'):
                
                auxiliary = row[0].casefold()
                lemmatized_auxiliary = row[4].casefold()
                
                # Step 14.4.3: We check what category of AUX it belongs to by seeing what list of AUX it is a part of
                if(row[0].casefold() in Indicator_To_Be):
                    aux_class = 1
                if(row[0].casefold() in Indicator_To_Do):
                    aux_class = 2
                if(row[0].casefold() in Indicator_To_Have):
                    aux_class = 3
                if(row[0].casefold() in Indicator_Modals):
                    aux_class = 4

            # Step 14.4.5: If POS Tag of token is 'TO' then the AUX class is 5 (Same class as 'To')
            if(row[3].casefold() == 'TO'.casefold()):
                aux_class = 5
    
    return auxiliary, aux_class, lemmatized_auxiliary