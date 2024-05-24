defmodule ServerWeb.RoomController do
  use ServerWeb, :controller

  def create_room(conn, _params) do
    id = UUID.uuid4()
    key = UUID.uuid4()
    user_id = UUID.uuid4()
    room = Rooms.create_room(id, key, user_id)
    Rooms.start_game_server(room)
    json(conn, %{id: id, key: key, user_id: user_id})
  end

  def get_rooms(conn, _params) do
    json(conn, Rooms.get_rooms())
  end

  def add_player(conn, %{"id" => id, "key" => key}) do
    user_id = UUID.uuid4()
    res = Rooms.add_player(id, key, user_id)
    if (res == :failed) do
      conn
      |> Plug.Conn.put_status(401)
      |> json(%{"reason" => "invalid room/key"})
    else
      json(conn, %{user_id: user_id, player_id: res})
    end
  end

  def server_ready(conn, %{"id" => id, "key" => key, "server_id" => server_id}) do
    Rooms.server_ready(id, key, server_id)
    json(conn, %{status: "ok"})
  end

  def get_nodes(conn, _) do
    self_node = inspect(node())
    nodes = inspect(Node.list())
    json(conn, %{server: self_node, nodes: nodes})
  end

  def state_room(conn, %{"id" => id}) do
    room = Rooms.get_room(id)
    IO.inspect(room)
    if room == :none do
      json(conn, %{status: :empty})
    else
      json(conn, %{status: :ok, nb_players: length(room.players), server_ready: room.server_ready})
    end
  end
end
