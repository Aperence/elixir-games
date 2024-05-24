defmodule Server.Repo do
  use Mongo.Repo,
    otp_app: :server,
    topology: :mongo
end
