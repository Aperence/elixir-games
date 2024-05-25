defmodule RoomInfo do

  @derive {Jason.Encoder, only: [:id, :key, :players, :server]}
  defstruct id: "", server: "", key: "", players: [], server_ready: false

  defimpl Mongo.Encoder do
    def encode(%RoomInfo{id: id, server: server, key: key, players: players, server_ready: server_ready}) do
      now = :os.system_time(:millisecond)
      %{
        _id: id,
        server: server,
        key: key,
        players: players,
        server_ready: server_ready,
        creationTime: now
      }
    end
  end

  def from_mongo(%{"_id" => id, "server" => server, "key" => key, "players" => players, "server_ready" => server_ready}) do
    %RoomInfo{
      id: id,
      server: server,
      key: key,
      players: players,
      server_ready: server_ready
    }
  end

  def add_player(%RoomInfo{id: id, server: server, key: key, players: players}, user) do
    %RoomInfo{id: id, server: server, key: key, players: players ++ [user]}
  end

  def get_player_name(%RoomInfo{key: _, players: players}, user) do
    id =
      players
      |> Enum.with_index()
      |> Enum.filter(fn p -> elem(p, 0) == user end)
      |> Enum.map(fn p -> elem(p, 1) end)
      |> Enum.at(0)
    "P#{id+1}"
  end

  def get_number_players(%RoomInfo{players: players}) do
    Enum.count(players)
  end

  def get_player_id(%RoomInfo{players: players}, user_id) do
    Enum.find_index(players, fn (p) -> user_id == p end)
  end
end
