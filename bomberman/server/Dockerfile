# Use an official Elixir runtime as a parent image.
FROM elixir:latest

RUN apt update
RUN apt install -y inotify-tools
# Create app directory and copy the Elixir projects into it.
RUN mkdir /app
COPY . /app
WORKDIR /app

# Install Hex package manager.
RUN mix local.hex --force

# Compile the project.
RUN mix deps.get
RUN mix do compile

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

CMD /wait && elixir --name server@$POD_IP --cookie $ERLANG_COOKIE --no-halt -S mix phx.server