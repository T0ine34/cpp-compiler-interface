from subprocess import run

def create_cmd(input_path : str , output_path : str | None, to_exe : bool = False, show_err : bool = True) -> str:
    cmd = 'g++'
    if show_err:
        cmd += ' -Wall'
    if not to_exe:
        cmd += ' -c'
    cmd += " "+input_path
    if output_path is not None:
        cmd += ' -o '+output_path

    return cmd

if __name__ == "__main__":
    cmd = create_cmd("C:\\Users\\antoi\\OneDrive\\IUT\\1e\\info\\hello_world.cpp","C:\\Users\\antoi\\OneDrive\\IUT\\1e\\info\\hello_world.o")
    print(cmd)
    run(cmd)