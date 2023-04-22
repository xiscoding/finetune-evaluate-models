
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
def create_completion(dataset):
    correct = 0
    total = 0
    for example in dataset:
        query = example['query']
        print(f'Query: {query}')
        expected_response = example['response']    
        response = openai.Completion.create(
                engine=ENGINE,
                prompt=query,
                max_tokens=2,
                n=1,
                stop=None,
                temperature=0.1
            )

        response_text = response['choices'][0]['text'].strip()
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
def create_chat_completion(dataset):
    correct = 0
    total = 0
    for example in dataset:
        query = example['query']
        print(f'Query: {query}')
        expected_response = example['response']
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
        response_text = response.choices[0].message.content.strip()
        print(response_text)
        print(f'Response: {response_text}')
        print(f'Expected Response: {expected_response}')
        if response_text == expected_response:
            correct += 1
            print("Answer Correct")
        total += 1
    accuracy = correct / total
    return accuracy

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
