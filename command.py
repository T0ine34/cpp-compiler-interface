from subprocess import run

def compile(input_path : list , output_path : str, operation : str = 'Executable (.exe)', show_err : bool = True, temp_path : str = 'C:') -> None:
    extension, param = ('.o', '-c') if operation == 'Compiled file (.o)' else ('.s','-S') if operation == 'Assembly (.s)' else ('.exe','')
    print(str(len(input_path))+' files to compiles :')
    if not output_path.endswith(extension):
        output_path+= extension
    for i in input_path:
        print('\t'+i)
    if len(input_path) > 1:
        #we have multiple file to compile together
        if param == '':
            param = '-c'
            extension = '.o'
        cmds = []
        names = []
        for file in input_path:
            name = file.split('\\')[-1]
            cmd = 'g++'
            if show_err:
                cmd += ' -Wall'
            cmd += ' '+param
            cmd += ' -o "'+temp_path+'\\'+name+extension+'"'
            cmds.append(cmd)
            names.append(temp_path+'\\'+name+extension)

        for cmd in cmds:
            run(cmd)
        
        
        if operation == 'Executable (.exe)':
            cmd = 'g++'
            for name in names:
                cmd += ' "'+name+'"'
            if show_err:
                cmd += ' -Wall'
                cmd += ' -o "'+output_path+'"'
            run(cmd)      
        print('Files compiled !')



    else:
        input_path = input_path[0]
        cmd = 'g++'
        if show_err:
            cmd += ' -Wall'
        cmd += " "+input_path
        cmd += " "+param
        cmd += ' -o '+output_path
        print(cmd)
        run(cmd)
        print('File compiled !')
             

if __name__ == "__main__":
    cmd = compile(["C:\\Users\\antoi\\OneDrive\\IUT\\1e\\info\\hello_world.cpp"],"C:\\Users\\antoi\\OneDrive\\IUT\\1e\\info\\hello_world")