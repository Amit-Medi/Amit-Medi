import chromadb
import requests
from slack_sdk import WebClient
from datetime import datetime, timedelta
import cohere
import re

# from sympy import collect
# from transformers.models.pop2piano.convert_pop2piano_weights_to_hf import model

co = cohere.Client('9GNgX78w1JrrgHkqXe5YebstVdTMrbwejFlSNhaC')  # Replace with your actual API key
slack_token = "xoxb-7675160877186-7742108123686-XesnSgFX02dzwYVJ8MJjLkhr"
slack_channel = "C07KNFH0HD4"
slack_client = WebClient(token=slack_token)

from chromadb.utils import embedding_functions

CHROMA_DATA_PATH = "chroma_data/"
EMBED_MODEL = "all-MiniLM-L6-v2"
COLLECTION_NAME = "demo_docs"


client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)

def process_slack_messages(messages):
    client.delete_collection(name=COLLECTION_NAME)
    collection = client.create_collection(name=COLLECTION_NAME, embedding_function=embedding_func, metadata={"hnsw:space": "cosine"})
    user_list_user = []
    user_list = []
    user_list_id = []
    user_list_metadata = []
    no=0;
    for message in messages:
        if 'client_msg_id' in message:
            user_added = next((user for user in user_list_user if user['id'] == message['user']), None)
            if not user_added:
                no += 1
                response = slack_client.users_info(user=message['user'])
                if response['ok']:
                    user_info = response['user']
                    id = user_info['id']
                    real_name = user_info['real_name']
                    message['text'] = re.sub(r'<(.*)>', real_name, message['text'])
                    user_list.append( message['text'] )
                    user_list_user.append({'id': id })
                    #user_list.append( message['text'])
                    user_list_metadata.append({'type': message['type']})
                    user_list_id.append( 'id'+ str(no) )
    collection.add(
        documents=user_list,
        metadatas=user_list_metadata,
        ids=user_list_id
    )

    return collection

def summarize(channel_id, message_response):

    # collection = process_slack_messages(message_response["messages"])

    # Get Data in string format
    # data = str(message_response["messages"])
    # # Prepare the input for the model
    # # input_text = f"{user_query}\n\nPossible answers:\n" + "\n".join(data) + "\n\nGenerated response:"
    #
    # # Generate summary
    # summary_response = co.summarize(
    #     model='command-light-nightly',
    #     text= data
    # )
    # response = co.generate(
    #     model='command-nightly',  # You can specify the model size here
    #     prompt=input_text,
    #     max_tokens=100,  # Adjust based on your needs
    #     temperature=0.7,  # Adjust for randomness
    #     stop_sequences=["\n"]  # Specify stop sequences if needed
    # )
    #
    # # print(response.generations[0].text.strip())
    # # Return the generated text
    # # return response.generations[0].text.strip()
    # print("Processed Slack Messages:", processed_summary)
    return ""

# Get event/prompt and return message
def handle_prompt_request(user_query: str, message_response):
    # Create a new onboarding tutorial.
    collection = process_slack_messages(message_response["messages"])

    results = collection.query(
        query_texts=[user_query],  # Chroma will embed this for you
        n_results=2  # how many results to return
    )

    answers = str(results['documents'])
    # Prepare the input for the model
    input_text = f"{user_query}\n\nPossible answers:\n" + "\n".join(answers) + "\n\nGenerated response:"

    # Generate text
    response = co.generate(
        model='command-nightly',  # You can specify the model size here
        prompt=input_text,
        max_tokens=100,  # Adjust based on your needs
        temperature=0.7,  # Adjust for randomness
        stop_sequences=["\n"]  # Specify stop sequences if needed
    )

    print(response.generations[0].text.strip())
    # Return the generated text
    return response.generations[0].text.strip()

def message_handler():

    user_message = "facing problem with the iphone"  # Stripping to avoid issues with extra spaces
    # user_id = message["user"]
    # channel_id = message["channel"]

    start_date = datetime.now() - timedelta(days=240)
    end_date = datetime.now()
    message_response = slack_client.conversations_history(channel=slack_channel, oldest=start_date.timestamp(),latest=end_date.timestamp())

    if "messages" in message_response:
        if "What's new?" in user_message:
            # Verify if channel_id or channel name
            # print("Channel_id" + channel_id)
            #currently hard coding the channel ID
            summary_response = summarize(slack_channel,message_response)
            # await say(summary_response)
            # Write to the client ChatWise
        else:
            response = handle_prompt_request(user_message, message_response)
            # await say(f"<@{message['user']}> @{response}")
            print("responsee"+ response)
            # await say(response)
            # rewrite line 152 accordingly
            # Write to the client ChatWise
    else:
        return ""# await say("No messages found in the specified channel during the given time period.")


message_handler()