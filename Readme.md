1. Create a conda environment with the following command:
    > conda env create -n environment_name python=3.7
2. Activate the environment:
    > conda activate environment_name
3. Install the requirements:
    > pip install -r requirements.txt
5. Run the Rasa server:
    > rasa run -m models --enable-api --cors "*"
6. Launch Index.html file in the browser to interact with the chatbot. 