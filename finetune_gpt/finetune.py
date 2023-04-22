import openai

# Set up OpenAI API key
openai.api_key = "your_openai_api_key"

# Upload the dataset to OpenAI
with open("your_dataset.txt", "rb") as f:
    dataset = openai.Dataset.create(file=f, purpose="fine-tuning")

# Define the model configuration and training task
model_config = {
    "dataset_id": dataset["id"],
    "model": "text-davinci-003",  # Choose the GPT-3 base model you want to fine-tune
    "description": "Fine-tuning GPT-3 on my custom dataset",
    "n_epochs": 1,
    "learning_rate_multiplier": 0.1,
    "batch_size": 4,
}

# Create a fine-tuning job
job = openai.FineTuning.create(**model_config)

# Check the status of the fine-tuning job
job_id = job["id"]
job_status = openai.FineTuning.get(job_id)
print("Job status:", job_status["status"])

# Once the job is completed, you can use the fine-tuned model for inference
if job_status["status"] == "succeeded":
    fine_tuned_model = job_status["fine_tuned_model"]
    prompt = "Your prompt here"
    
    response = openai.Completion.create(
        engine=fine_tuned_model,
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.8,
    )

    print(response.choices[0].text.strip())
