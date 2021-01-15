FROM python:3.7-alpine
COPY ./ .

RUN pip install -r requirements.txt
RUN chmod +x spdx_to_dbom.py
RUN echo $GATEWAY
RUN echo $REPO 
RUN echo $CHANNEL 
RUN echo $FILE
RUN echo $ASSET

CMD python3 dbom_to_spdx.py -g $GATEWAY -r $REPO -c $CHANNEL -f $FILE -a $ASSET
