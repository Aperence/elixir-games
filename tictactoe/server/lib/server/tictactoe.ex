defmodule Tictactoe do

  @size 3

  defstruct positions: %{}, player: :o, winner: :none

  defp win_row(positions, {x, y}) do
    Enum.member?(positions, {x, y+1}) and Enum.member?(positions, {x, y+2})
  end

  defp win_column(positions, {x, y}) do
    Enum.member?(positions, {x+1, y}) and Enum.member?(positions, {x+2, y})
  end

  defp win_diag(positions, {x, y}) do
    Enum.member?(positions, {x+1, y+1}) and Enum.member?(positions, {x+2, y+2})
  end

  defp win_diag_rev(positions, {x, y}) do
    Enum.member?(positions, {x+1, y-1}) and Enum.member?(positions, {x+2, y-2})
  end

  defp win_pos(positions, pos) do
    win_row(positions, pos) or win_column(positions, pos) or win_diag(positions, pos) or win_diag_rev(positions, pos)
  end

  def winner(positions) do
    lst_x = Map.get(positions, :x, MapSet.new([]))
    lst_o = Map.get(positions, :o, MapSet.new([]))
    cond do
      Enum.any?(lst_x, fn pos -> win_pos(lst_x, pos) end) -> :x
      Enum.any?(lst_o, fn pos -> win_pos(lst_o, pos) end) -> :o
      true -> :none
    end
  end

  def play(t = %Tictactoe{positions: positions, player: player, winner: win}, i, j, c) when i >= 0 and i < @size and j >= 0 and j < @size and c == player and win == :none do
    if Map.get(positions, :x, MapSet.new([])) |> Enum.member?({i, j}) or Map.get(positions, :o, MapSet.new([])) |> Enum.member?({i, j}) do
      t
    else
      other = case player do
        :x -> :o
        :o -> :x
      end
      updated_position = Map.update(positions, c, MapSet.new([{i, j}]), fn value -> MapSet.put(value, {i, j}) end)
      %Tictactoe{positions: updated_position, player: other, winner: winner(updated_position)}
    end
  end

  def play(tictactoe, _i, _j, _c)do
    tictactoe
  end

  def json(%Tictactoe{positions: positions, player: player, winner: win}) do
    lst_x = Map.get(positions, :x, MapSet.new([]))
    lst_o = Map.get(positions, :o, MapSet.new([]))
    %{
      winner: win,
      player: player,
      board:
        for i <- 0..@size-1 do
          for j <- 0..@size-1 do
            cond do
              Enum.member?(lst_x, {i, j}) -> :x
              Enum.member?(lst_o, {i, j}) -> :o
              true -> :empty
            end
          end
        end
    }
  end
end
