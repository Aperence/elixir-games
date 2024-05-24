defmodule ServerWeb.GameChannel do
  use ServerWeb, :channel
  require Logger

  @impl true
  def join("room:" <> roomID, payload = %{"user_id" => user_id}, socket) do
    if authorized?(payload) do
      send(self(), {:player_joined, roomID, user_id})
      {:ok, socket}
    else
      {:error, %{reason: "unauthorized"}}
    end
  end

  @impl true
  def handle_info({:player_joined, roomID, user_id}, socket) do
    room = Rooms.get_room(roomID)
    if room != :none do
      Logger.info("User #{user_id} joined room #{inspect(room)}")
      broadcast!(socket, "player_joined", %{nb_players: Rooms.get_number_players(roomID)})
    end
    {:noreply, socket}
  end

  @impl true
  def handle_in(msg, payload, socket) do
    topic = socket.topic
    ["room", roomID] = String.split(topic, ":")

    {user_id, rest_payload} = Map.pop(payload, "user_id")

    room = Rooms.get_room(roomID)
    if (room != :none) do
      if (user_id == room.server) do
        broadcast(socket, msg, rest_payload)
      else
        player_id = RoomInfo.get_player_id(room, user_id)
        broadcast(socket, msg, Map.put(payload, "player_id", player_id))
      end
    end
    {:noreply, socket}
  end

  # Add authorization logic here as required.
  defp authorized?(_payload) do
    true
  end
end
