import os
import time
from tqdm import tqdm
from openai import AzureOpenAI

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")

TEST_INPUTS_DIR = "test_inputs"  # The directory where the test inputs are stored
RESULT_DIR = "results"  # The directory where the results will be stored

# The Assistant ID list, you can add more assistant IDs to the list
ASSISTANT_ID_LIST = [
    'asst_B3mLtXZ8cRKcADvwvahMyd9P',
    'asst_opyd0CDXHEKUYcsopdlPil4Q',
]

# Initialize the client
client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version="2024-05-01-preview",
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)


# Run the assistant
def run_assistant(input_text, assistant_id):
    # Create a thread
    thread = client.beta.threads.create()

    # Add a user question to the thread
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=input_text
    )

    # Run the thread
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    # Looping until the run completes or fails
    while run.status in ['queued', 'in_progress', 'cancelling']:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        return messages
    elif run.status == 'requires_action':
        # the assistant requires calling some functions
        # and submit the tool outputs back to the run
        pass
    else:
        return None


# Get the test inputs
def get_text_file_contents_from_dir(dir_path: str) -> dict:
    test_inputs = {}
    for file_name in os.listdir(dir_path):
        if file_name.endswith(".txt"):
            with open(os.path.join(dir_path, file_name), "r") as file:
                file_name_without_ext = os.path.splitext(file_name)[0]
                test_inputs[file_name_without_ext] = file.read()
    return test_inputs


def main():
    # Get the test inputs
    test_inputs = get_text_file_contents_from_dir(TEST_INPUTS_DIR)
    pbar = tqdm(ASSISTANT_ID_LIST)
    for assistant_id in pbar:
        pbar.set_description(f"Running assistant {assistant_id}")
        test_inputs_pbar = tqdm(test_inputs.items())
        for test_input_name, test_input in test_inputs_pbar:
            # Run the assistant
            test_inputs_pbar.set_postfix({"Test input": test_input_name})
            messages = run_assistant(test_input, assistant_id)
            if messages:
                # Save the results
                result_file_name = f"{assistant_id}_{test_input_name}_result.json"
                if not os.path.exists(RESULT_DIR):
                    os.makedirs(RESULT_DIR)
                with open(os.path.join(RESULT_DIR, result_file_name), "w") as file:
                    file.write(messages.to_json())
                test_inputs_pbar.set_postfix({"Result": "Success"})
            else:
                test_inputs_pbar.set_postfix({"Result": "Failed"})
    print("All tests completed.")


if __name__ == '__main__':
    main()
