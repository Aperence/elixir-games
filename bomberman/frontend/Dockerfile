FROM python

RUN pip install pygame
RUN pip install websockets
RUN pip install requests

WORKDIR /app

COPY ./assets ./assets
COPY ./src ./src

CMD python3 -u /app/src/bomberman_server.py --key $room_key --room-id $room_id --user-id $server_id --host $host