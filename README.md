# End-To-End-Medical-Chatbot


## How to run?
### STEPS:
Clone the repository

Project repo: https://github.com/
### STEP 01- Create a conda environment after opening the repository
conda create -n mchatbot python=3.11 -y
conda activate mchatbot
### STEP 02- install the requirements
python -m pip install -r requirements.txt
### Create a `.env` file in the project root with the Pinecone index settings:
```env
PINECONE_API_KEY=your-api-key
PINECONE_INDEX=medical-chatbot
PINECONE_HOST=your-index-host
```

Use the exact **Host** shown on the selected index's details page in Pinecone.
Do not include a path such as `/query`.
### Download the quantize model from the link provided in model folder & keep the model in the model directory:
Download the Llama 2 Model:

llama-2-7b-chat.ggmlv3.q4_0.bin


From the following link:
https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/tree/main

run the following command

python store_index.py

Finally run the following command
python app.py

Open http://127.0.0.1:5001 in your browser.
If the app reports that port 5001 is already in use, stop the existing chatbot
process before starting another copy.
### Techstack Used:
* Python
* LangChain
* Flask
* Meta Llama2
* Pinecone
