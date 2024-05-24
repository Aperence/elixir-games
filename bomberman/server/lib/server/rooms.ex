defmodule Rooms do

  @max_number_players 4

  def create_room(id, key, player_id) do
    server_id = UUID.uuid4()
    room = %RoomInfo{id: id, server: server_id, key: key, players: [player_id]}
    Mongo.insert_one(:mongo, "games", room)
    room
  end

  def start_game_server(%RoomInfo{id: id, key: key, server: server_id}) do
    if Application.get_env(:server, :kube) do
      IO.puts("Lauching game server in kubernetes pod with server id = #{server_id}")
      {:ok, conn} = K8s.Conn.from_service_account("/var/run/secrets/kubernetes.io/serviceaccount")
      resource =
        %{
          "apiVersion" => "apps/v1",
          "kind" => "Deployment",
          "metadata" => %{"name" => "game-server-#{id}", "namespace" => "default"},
          "spec" => %{
            "replicas" => 1,
            "selector" => %{"matchLabels" => %{"app" => "game-server-#{id}"}},
            "template" => %{
              "metadata" => %{"labels" => %{"app" => "game-server-#{id}"}},
              "spec" => %{
                "containers" => [
                  %{
                    "env" => [
                      %{"name" => "room_key", "value" => key},
                      %{"name" => "room_id", "value" => id},
                      %{"name" => "server_id", "value" => server_id},
                      %{"name" => "host", "value"=> "server:4000"}
                    ],
                    "image" => "aperence/bomberman-game-server",
                    "imagePullPolicy" => "Always",
                    "name" => "server",
                    "resources" => %{
                      "limits" => %{"cpu" => "500m", "memory" => "512Mi"}
                    }
                  }
                ]
              }
            }
          }
        }

      operation = K8s.Client.create(resource)
      {:ok, _deployment} = K8s.Client.run(conn, operation)
    else
      IO.puts("Lauching game server in local with server id = #{server_id}")
      Task.async(fn-> System.cmd("python3", ["../frontend/src/bomberman_server.py",  "--key", "#{key}", "--room-id", "#{id}", "--user-id", "#{server_id}"])end)
    end
  end

  def get_room(id) do
    case Mongo.find(:mongo, "games", %{_id: id}) |> Enum.to_list() do
      [] -> :none
      [room] -> RoomInfo.from_mongo(room)
    end
  end

  def get_rooms() do
    Mongo.find(:mongo, "games", %{}) |> Enum.to_list() |> Enum.map(fn r -> RoomInfo.from_mongo(r) end)
  end

  def add_player(id, key, user) do
    if (get_room(id) == :none or get_room(id)["key"] != key) do
      {:err, :invalid_room}
    else
      add_player_real(id, key, user)
    end

  end

  defp add_player_real(id, key, user) do
    res = Mongo.update_one(:mongo, "games",
      %{
        _id: id,
        key: key
      }, %{
        "$push": %{
          players: %{
            "$each": [user],
            "$slice": @max_number_players
          }
      }
      })
    room = get_room(id)
    case res do
      {:ok, _} -> if Enum.any?(room.players, fn x -> x == user end) do :ok else :room_full end
      _ -> res
    end
  end

  def get_number_players(id) do
    room = get_room(id)
    if room == :none do
      0
    else
      RoomInfo.get_number_players(room)
    end
  end

  def server_ready(id, key, server_id) do
    Mongo.update_one(:mongo, "games",
    %{
      _id: id,
      key: key,
      server: server_id
    }, %{
      "$set": %{
        server_ready: true
      }
    })
  end
end
