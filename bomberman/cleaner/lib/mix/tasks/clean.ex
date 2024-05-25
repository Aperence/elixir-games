defmodule Mix.Tasks.Cluster.Clean do
  use Mix.Task

  @shortdoc "Clean the outdated game servers"
  def run(_) do
    Application.ensure_all_started(:mongodb_driver)
    Application.ensure_all_started(:k8s)
    Cleaner.clean()
  end
end
