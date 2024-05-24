defmodule TictactoeTest do
  use ExUnit.Case

  setup do
    game = %Tictactoe{}

    %{game: game}
  end

  test "game win row", %{game: game} do
    game1 = Tictactoe.play(game, 0, 0, :o)
    game2 = Tictactoe.play(game1, 1, 0, :x)
    game3 = Tictactoe.play(game2, 0, 1, :o)
    game4 = Tictactoe.play(game3, 2, 0, :x)
    game5 = Tictactoe.play(game4, 0, 2, :o)
    IO.inspect(game5)

    assert(game5.winner != :none)
  end
end
