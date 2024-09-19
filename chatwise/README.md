# chatwise

## Hackathon 2024

### Explanation:

Slack API Connection: The code begins by importing the necessary modules and setting up the Slack API connection. Replace "your_slack_token" with your actual Slack API token and "your_slack_channel" with the desired Slack channel ID.
Chroma Vector DB Setup: The code sets up the Chroma Vector DB by providing the host address ("your_chroma_host") and creating an HTTP client with the specified settings.
Cohere Command Model Setup: The Cohere Command model is initialized with your Cohere API key ("your_cohere_api_key"). This model will be used for chunking and summarization.
Chroma Instance Creation: A Chroma instance is created using the Chroma client and Cohere Command embeddings.
Retrieval Chain Creation: A retrieval chain is set up using the Chroma retriever and Cohere Command model. The ConversationBufferMemory class is used to store the conversation history.
Slack Message Processing: The process_slack_messages function takes a list of Slack messages as input. It uses the Cohere Command model to chunk the messages into coherent segments, stores the chunked messages in the Chroma Vector DB, and then retrieves and summarizes the messages using the retrieval chain.
Slack Message Retrieval: The code retrieves Slack messages from the specified channel within the last 7 days using the Slack API. It then calls the process_slack_messages function to process and summarize the retrieved messages.
Please note that you need to replace the placeholder values ("your_slack_token", "your_slack_channel", "your_chroma_host", and "your_cohere_api_key") with your actual API tokens, channel IDs, and credentials.

This code demonstrates how to integrate Slack's API, Chroma Vector DB, and the Cohere Command model to retrieve, chunk, store, and summarize messages from Slack conversations. It showcases the power of combining natural language processing tools and databases to build intelligent chatbots and conversational systems.

