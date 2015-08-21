import cx_Freeze

executables = [cx_Freeze.Executable("MainGame.py")]

cx_Freeze.setup(
    name="Donkey Kong",
    options={"build_exe": {"packages":["pygame"]}},
    executables = executables

    )
