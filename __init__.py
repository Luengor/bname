from importlib.metadata import entry_points

display_eps = entry_points(group="bname")
display = display_eps[0].load()

