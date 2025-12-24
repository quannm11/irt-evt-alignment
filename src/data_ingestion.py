import pandas as pd
from datasets import load_dataset

def extract_first_turn(text):
    parts = text.split('\n\nAssistant: ')
    prompt = parts[0].replace('\n\nHuman: ', '').strip()
    response = parts[1].split('\n\nHuman:')[0].strip()
    return prompt, response

def is_refusal(response):
    refusal_phrases = [
        "I'm sorry",
        "I cannot",
        "As an AI language model",
        "I don't have the capability",
        "I am unable to assist",
        "I cannot provide",
        "I am not able to",
        "I do not have the ability",
        "I apologize",
        "I'm afraid",
        "I really couldn’t say",
    ]
    response_prefix = response[:150].lower() #check only the beginning of the response
    for phrase in refusal_phrases:
        if phrase.lower() in response_prefix:
            return True
    return False

def run_ingestion(dataset_name, subset, target_count):
    #starts loading the dataset in streaming mode
    dataset = load_dataset(dataset_name, data_dir=subset, split="train", streaming=True) 
    records = []
    
    for item in dataset:
        prompt, chosen_resp = extract_first_turn(item['chosen'])
        _, rejected_resp = extract_first_turn(item['rejected'])
        
        if is_refusal(chosen_resp):
            records.append({
                "prompt": prompt,
                "response_chosen": chosen_resp,
                "response_rejected": rejected_resp,
                "label_chosen": 1,
                "label_rejected": 0
            })
        
        # stop when reach the target sample count
        if len(records) >= target_count:
            break
            
    return pd.DataFrame(records)