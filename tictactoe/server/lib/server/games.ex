defmodule Games do
  use Agent

  # in production, use a db instead, we are using an agent for simplicity

  def start_link(_) do
    Agent.start_link(fn -> %{} end, name: __MODULE__)
  end

  def get_game(id) do
    Agent.get(__MODULE__, fn games -> Map.get(games, id, %Tictactoe{}) end)
  end

  def update(id, state) do
    Agent.update(__MODULE__, fn games -> Map.update(games, id, state, fn _prev -> state end) end)
  end
end
