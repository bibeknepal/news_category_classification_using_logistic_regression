#This sets up the container with the python 3.12 installed
FROM python:3.12-slim

#This sets up the \app directory as the working directory for any RUN,CMD,ENTRYPOINT or COPY Command
WORKDIR /app

#This copies everything from your current directory to the app directory in the container
COPY app.py /app
COPY requirements.txt /app
COPY model /app/model

#This installs all the packages listed in requirements.txt file.
RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt stopwords wordnet averaged_perceptron_tagger

#This tells the docker to listen at the port 8501 at runtime
EXPOSE 8501
#This sets the default command for the container to run app with streamlit
ENTRYPOINT [ "streamlit","run" ]
# This command tells streamlit to run app.py script
CMD ["app.py"]