
# import openai_secret_manager
import json
# assert "openai" in openai_secret_manager.get_services()
# secrets = openai_secret_manager.get_secret("openai")
from config import Config
import openai

#GET OPENAI API KEY FROM CONFIG.PY FROM .ENV
config = Config()
openai.api_key = config.OPENAI_API_KEY #secrets["api_key"]

#DEFINE OPENAI MODEL
ENGINE = "gpt-3.5-turbo"

#works with:
'''
text-davinci-003
text-davinci-002
code-davinci-002
'''
#Input: dataset .json file
#Output: (# correct model answers ) / (total # questions asked)
def create_completion(dataset):
    correct = 0
    total = 0
    for example in dataset:
        expected_response = example['response']    
        response_text = completion(example)#response['choices'][0]['text'].strip()
        print(f'Response: {response_text}')
        print(f'Expected Response: {expected_response}')
        if response_text == expected_response:
            correct += 1
            print("Answer Correct")
        total += 1
    accuracy = correct / total
    return accuracy

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
        response_text = chat_completion(example)
        print(f'Response: {response_text}')
        print(f'Expected Response: {expected_response}')
        correct += evaluate_answers(response_text, expected_response)
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
        max_tokens=2,
        n=1,
        stop=None,
        temperature=0.5
    )
    return response.choices[0].message.content.strip()

#Input: single query form .json file
#Output: stripped response from model
def completion(example):
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
        max_tokens=2,
        n=1,
        stop=None,
        temperature=0.5
    )
    return response.choices[0].message.content.strip()

#Input: stripped model response, expected response from .json
#Retun: 1 if match, 0 if no match
def evaluate_answers(response_text, expected_response):
        if response_text == expected_response:
            print("Answer Correct")
            return 1
        return 0

#Input: path to .json dataset
#Output: none
def evaluate_LLM(dataset_path):
    with open(dataset_path, 'r') as f:
        dataset = json.load(f)
    if ENGINE.startswith("gpt-3.5"):
        accuracy = create_chat_completion(dataset)
        print(f'Accuracy: {accuracy:.2f}')
    else:  
        accuracy = create_completion(dataset)
        print(f'Accuracy: {accuracy:.2f}')

if __name__ == '__main__':
    dataset_path = '/home/xdoestech/Documents/Discrete_Math_project/train_models/math20.json'
    evaluate_LLM(dataset_path)
