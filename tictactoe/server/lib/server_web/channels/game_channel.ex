defmodule ServerWeb.GameChannel do
  use ServerWeb, :channel

  @impl true
  def join("room:" <> roomID, payload, socket) do
    if authorized?(payload) do
      send(self(), {:update, roomID})
      {:ok, socket}
    else
      {:error, %{reason: "unauthorized"}}
    end
  end

  # It is also common to receive messages from the client and
  # broadcast to everyone in the current topic (game:lobby).
  @impl true
  def handle_in("play", %{"i" => i, "j" => j, "c" => c}, socket) do
    topic = socket.topic
    ["room", roomID] = String.split(topic, ":")

    game = Games.get_game(roomID)
    updated_game = Tictactoe.play(game, i, j, String.to_atom(c))
    Games.update(roomID, updated_game)

    broadcast(socket, "update", Tictactoe.json(updated_game))
    {:noreply, socket}
  end

  @impl true
  def handle_in("play", _payload, socket) do
    {:reply, :ok, socket}
  end

  @impl true
  def handle_info({:update, roomID}, socket) do
    game = Games.get_game(roomID)
    broadcast(socket, "update", Tictactoe.json(game))
    {:noreply, socket}
  end

  # Add authorization logic here as required.
  defp authorized?(_payload) do
    true
  end
end
