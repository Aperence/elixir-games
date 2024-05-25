defmodule CleanerTest do
  use ExUnit.Case
  doctest Cleaner

  test "greets the world" do
    assert Cleaner.hello() == :world
  end
end
