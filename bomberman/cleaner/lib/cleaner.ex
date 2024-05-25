defmodule Cleaner do
  require Logger

  defp getRooms(url) do
    {:ok, conn} = Mongo.start_link(url: url)

    now = :os.system_time(:millisecond)

    temp = System.get_env("DELETE_DELAY") || "10"
    {delay, _} = Integer.parse(temp)

    outdated = now - delay * 60 * 1000   # all rooms that are up until more than delay minutes
    # Gets an enumerable cursor for the results
    cursor = Mongo.find(conn, "games", %{creationTime: %{ "$lt": outdated }})

    cursor
    |> Enum.to_list()
  end

  defp delete_game_server(deploy_name) do
    {:ok, conn} = K8s.Conn.from_service_account("/var/run/secrets/kubernetes.io/serviceaccount")

    operation = K8s.Client.delete("apps/v1", :deployment, [namespace: "default", name: deploy_name])
    {:ok, _} = K8s.Client.run(conn, operation)
  end

  defp clean_room(%{"_id" => id}, url, kube) do
    deploy_name = "game-server-#{id}"
    Logger.info("Deleting room #{id}")

    # delete game server
    if (kube) do
      delete_game_server(deploy_name)
    end

    # delete from db
    {:ok, conn} = Mongo.start_link(url: url)
    Mongo.delete_one(conn, "games", %{_id: id})
  end

  @doc """
  Clean the outdated game servers
  """
  def clean do
    Logger.info("Cleaning...")

    url = System.get_env("MONGODB_URI") || "mongodb://localhost:27017/db-bomberman"
    kube = System.get_env("KUBERNETES") || false
    for room <- getRooms(url) do
      clean_room(room, url, kube)
    end
  end
end
