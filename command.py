from subprocess import run
from os import remove

def compile(input_path : list , output_path : str, operation : str = 'Executable (.exe)', show_err : bool = True, temp_path : str = 'C:') -> None:
    if operation == 'Shared library (.so)': 
        if not output_path.endswith(".so"):
            output_path+= ".so"
        files = []
        for file in input_path:
            name = file.split('/')[-1].split('.')[0]
            cmd = "g++ -c -o \""+temp_path+"\\"+name+".o\" \""+file+"\""
            files.append(temp_path+"\\"+name+".o")

            print('Executing :\n\t'+cmd)
            run(cmd)

        cmd = "gcc -Wall -shared -o \""+output_path+'" "'+'" "'.join(files)+'" -lstdc++'
        print('Executing :\n\t'+cmd)
        run(cmd)

        for file in files:
            remove(file)
            print("file \"%s\"deleted"%file)

    else:
        extension, param = ('.o', '-c') if operation == 'Compiled file (.o)' else ('.s','-S') if operation == 'Assembly (.s)' else ('.exe','')

        if not output_path.endswith(extension):
            output_path+= extension

        print("operation : %s"%operation)

        print(str(len(input_path))+' files to compiles :')
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
                name = file.split('/')[-1].split('.')[0]
                cmd = 'g++'
                if show_err:
                    cmd += ' -Wall'
                cmd += ' '+param
                cmd += ' -o "'+temp_path+'\\'+name+extension+'"'
                cmd += ' "'+file+'"'
                cmds.append(cmd)
                names.append(temp_path+'\\'+name+extension)

            for cmd in cmds:
                print('Executing :\n\t'+cmd)
                run(cmd)
            
            
            if operation == 'Executable (.exe)':
                cmd = 'g++'
                for name in names:
                    cmd += ' "'+name+'"'
                if show_err:
                    cmd += ' -Wall'  
                cmd += ' -o "'+output_path+'"'
                print('Executing :\n\t'+cmd)
                run(cmd)      

            print('Files compiled !')

            for file in names:
                remove(file)
                print("file \"%s\"deleted"%file)

        else:
            input_path = input_path[0]
            cmd = 'g++'
            if show_err:
                cmd += ' -Wall'
            cmd += " \""+input_path+"\""
            cmd += " "+param
            cmd += ' -o \"'+output_path+"\""
            print(cmd)
            run(cmd)
            print('File compiled !')
             

if __name__ == "__main__":
    cmd = compile(["C:\\Users\\antoi\\OneDrive\\IUT\\1e\\info\\hello_world.cpp"],"C:\\Users\\antoi\\OneDrive\\IUT\\1e\\info\\hello_world")