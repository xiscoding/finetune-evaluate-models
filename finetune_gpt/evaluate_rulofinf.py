# import openai_secret_manager
import json
# assert "openai" in openai_secret_manager.get_services()
# secrets = openai_secret_manager.get_secret("openai")
from config import Config
import openai
from evaluators import Eval_rulofinf
#GET OPENAI API KEY FROM CONFIG.PY FROM .ENV
config = Config()
openai.api_key = config.OPENAI_API_KEY #secrets["api_key"]

#DEFINE OPENAI MODEL
ENGINE = "gpt-3.5-turbo"
responses =[]
expected_responses=[]
evaluator = Eval_rulofinf()
#works with:
'''
gpt-3.5-turbo
gpt-3.5-turbo-0301
'''
#Input: dataset .json file
#Output: (# correct model answers ) / (total # questions asked)
def create_chat_completion(dataset):
    
    correct = 0
    total = 0
    for example in dataset:
        expected_response = example['response']
        gpt_response = chat_completion(example)
        print(f'Response: {gpt_response}')
        print(f'Expected Response: {expected_response}')
        correct += evaluate_answers(gpt_response, expected_response)
        total += 1
    accuracy = correct / total
    return accuracy

#Input: single query form .json file
#Output: stripped response from model
def chat_completion(example):
    query = example['query']
    print(f'Query: {query}')
    message= [
                        {
                            "role": 'assistant',
                            "content": query
                        }
                    ]
                
        #https://platform.openai.com/docs/api-reference/chat/create?lang=python
    response = openai.ChatCompletion.create(
        model= ENGINE,
        messages=message,
        max_tokens=75,
        n=1,
        stop=None,
        temperature=0.5
    )
    return response.choices[0].message.content.strip()

#Input: stripped model response, expected response from .json
#Retun: 1 if match, 0 if no match
def evaluate_answers(gpt_response, expected_response):
    is_valid = evaluator.validate_proof(gpt_response, expected_response)
    print(is_valid)
    return is_valid
#Input: path to .json dataset
#Output: none
def evaluate_LLM(dataset_path):

    with open(dataset_path, 'r') as f:
        dataset = json.load(f)
    if ENGINE.startswith("gpt-3.5"):
        accuracy = create_chat_completion(dataset)
        print(f'Accuracy: {accuracy:.2f}')
if __name__ == '__main__':
    dataset_path = '/home/xdoestech/Documents/Discrete_Math_project/train_models/logic5_rulesofinf_symbolic.json'
    evaluate_LLM(dataset_path)