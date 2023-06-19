import re
import json
from helper_functions.helpers import clean, Parse, Parse_spacy
import pandas as pd

def compare_head_verb(classification_output, annotation_str, corr_count, total_count, comp_category, temp_entry_output_storage_file):
        
    # This flag lets us print only the cases where our resolution rules fail
    print_flag = False
    
    # Organizing original annotation for comparison
    ann_regex = r'.*?\<\<(.*)\>\>.*'
    vpe_list = re.findall('\[.*?\]',annotation_str)
    
    annotations = []
    
    if comp_category is not None:
        for vpe in vpe_list:
            annotation_content = json.loads(vpe)
            if annotation_content[-2] == comp_category:
                annotations.append(annotation_content)
    else:
        for vpe in vpe_list:
            annotation_content = json.loads(vpe)
            annotations.append(annotation_content)
    
    explicit_ellipsis_ann_list = []
    for i in range(0,len(annotations)):
        if annotations[i][6] != 6 and annotations[i][0] != 4:
            explicit_ellipsis_ann_list.append(annotations[i])
    
    to_compare_annotations = []
    for ann in explicit_ellipsis_ann_list:
        if ann[3] != 0:
            annotated_resolution = re.search(ann_regex, ann[7]).group(1)
            parsed_resolved_vp = Parse_spacy(annotated_resolution)
            ann_head_verb = ""
            ann_head_verb_index = ""
            ann_vpe_sent = clean(re.sub("\<\<.*?\>\>","", ann[-1]).replace("//", "").strip())

            for vb_index, entry in enumerate(parsed_resolved_vp):
                if ('VB' in entry[3] or ('IN' == entry[3] and 'like' == entry[-1])) and entry[2] != 'aux':
                    ann_head_verb = entry[-1]
                    ann_head_verb_index = str(vb_index+1)
                    break
            
            # When two verbs joined by a conjunction are in the annotation, check for correct classification
            # against the latter verb. This is because the verb nearer to the site of ellipsis is usually resolved
            # in case of matching scores.
            if ann_head_verb != "":
                for vb_index, entry in enumerate(parsed_resolved_vp):
                    if entry[1] == ann_head_verb_index and 'VB' in entry[3] and entry[2] == 'conj':
                        ann_head_verb = entry[-1]
                        ann_head_verb_index = str(vb_index+1)
                        break
                    
            # Checking if the annotated verb has another gerund attached to it using hyphen after it. If it exists we choose
            # the latter gerund verb. For e.g. in <<very thought-provoking>>, our main head verb is "provoking"
            if ann_head_verb != "" and int(ann_head_verb_index) + 1 <= len(parsed_resolved_vp) - 1 and parsed_resolved_vp[int(ann_head_verb_index)][0] == "-" and parsed_resolved_vp[int(ann_head_verb_index)+1][3] == 'VBG':
                ann_head_verb = parsed_resolved_vp[int(ann_head_verb_index) + 1][-1]
                ann_head_verb_index = str(int(ann_head_verb_index) + 2)
            
            if ann_head_verb == "":
                ann_head_verb = parsed_resolved_vp[0][-1]
            to_compare_annotations.append([ann_head_verb.casefold(), clean(ann_vpe_sent)])
            
    if len(to_compare_annotations) == 0:
        return corr_count, total_count, print_flag
    
    # Organizing classifier output for comparison
    to_compare_classifications = []
    for classification in classification_output:
        if classification['resolved_head_verb'] is not None:
            lemmatized_resolved_headverb = Parse_spacy(classification['resolved_head_verb'])[0][-1]
            to_compare_classifications.append([lemmatized_resolved_headverb.casefold(), clean(classification['vpe_sent'])])
    
    # Comparing Head Verb Ellipsis Cases for correctness
    curr_correct_count = 0
    if len(to_compare_annotations) == len(to_compare_classifications):    
        for i in range(0,len(to_compare_annotations)):
            if to_compare_annotations[i] == to_compare_classifications[i]:
                curr_correct_count += 1
    else:
        for i in range(0,len(to_compare_annotations)):
            if to_compare_annotations[i] in [item for item in to_compare_classifications]:
                curr_correct_count += 1
    
    
    print("\nCOMPARING PURE ELLIPSIS RESOLUTIONS WITH ITS ANNOTATIONS\n", file = temp_entry_output_storage_file)
    
    print(to_compare_annotations, file = temp_entry_output_storage_file)
    print(to_compare_classifications, file = temp_entry_output_storage_file)
    
    corr_count += curr_correct_count
    total_count += len(to_compare_annotations)
    
    if len(to_compare_annotations) != curr_correct_count:
        print_flag = True
    
    print("\n%d resolutions out of %d are correct." % (curr_correct_count, len(to_compare_annotations)), file = temp_entry_output_storage_file)
                
    return corr_count, total_count, print_flag

def compare_ellided_obj_parent(structured_conversation, classification_output, annotation_str, corr_count, total_count, comp_category, temp_entry_output_storage_file):
    
    # This flag lets us print only the cases where our resolution rules fail
    print_flag = False
    
    if pd.isna(annotation_str):
        return corr_count, total_count, print_flag
    
    # Organizing original annotation for comparison
    vpe_list = re.findall('\[.*?\]',annotation_str)
    annotations = []
    
    if comp_category is not None:
        for vpe in vpe_list:
            annotation_content = json.loads(vpe)
            if annotation_content[-3] == comp_category:
                annotations.append(annotation_content)
    else:
        for vpe in vpe_list:
            annotation_content = json.loads(vpe)
            annotations.append(annotation_content)
    
    explicit_ellipsis_ann_list = []
    for i in range(0,len(annotations)):
        if annotations[i][6] != 6 and annotations[i][0] != 4:
            explicit_ellipsis_ann_list.append(annotations[i])
    
    to_compare_annotations = []
    for ann in explicit_ellipsis_ann_list:
        if ann[3] == 0:
            ann_vpe_sent = clean(re.sub("\<\<.*?\>\>","", ann[-2]).replace("//", "").strip())
            ann_parent_verb = ann[-1]
            to_compare_annotations.append([ann_parent_verb.casefold(), clean(ann_vpe_sent)])
    
    
    # Organizing classifier output for comparison
    to_compare_classifications = []
    for classification in classification_output:
        if classification['ellided_obj_child_parent_verb'] is not None:
            
            resolved_parent_verb = None

            if classification['sen_type'] == 4:
                resolved_parent_verb = classification['parsed_vpe_sent'][classification['ellided_obj_child_parent_verb']][0]
            
            elif classification['sen_type'] == 2:
                resolution_sen_index = classification['sen_index']-1
                parsed_resolution_sen = structured_conversation[resolution_sen_index]
                resolved_parent_verb = parsed_resolution_sen[classification['ellided_obj_child_parent_verb']][0]
            
            if resolved_parent_verb is not None:
                to_compare_classifications.append([resolved_parent_verb.casefold(), clean(classification['vpe_sent'])])
            else:
                to_compare_classifications.append([resolved_parent_verb, clean(classification['vpe_sent'])])
    

    # Comparing Object only Ellipsis Cases for correctness
    curr_correct_count = 0
    if len(to_compare_annotations) == len(to_compare_classifications):    
        for i in range(0,len(to_compare_annotations)):
            if to_compare_annotations[i] == to_compare_classifications[i]:
                curr_correct_count += 1
    else:
        for i in range(0,len(to_compare_annotations)):
            if to_compare_annotations[i] in [item for item in to_compare_classifications]:
                curr_correct_count += 1
    
    
    print("\nCOMPARING OBJECT ONLY ELLIPSIS RESOLUTIONS WITH ITS ANNOTATIONS\n", file = temp_entry_output_storage_file)
    
    print(to_compare_annotations, file = temp_entry_output_storage_file)
    print(to_compare_classifications, file = temp_entry_output_storage_file)
    
    corr_count += curr_correct_count
    total_count += len(to_compare_annotations)
    
    if len(to_compare_annotations) != curr_correct_count:
        print_flag = True
    
    print("\n%d resolutions out of %d are correct." % (curr_correct_count, len(to_compare_annotations)), file = temp_entry_output_storage_file)
                
    return corr_count, total_count, print_flag