import cmd
from pathlib import Path
from lucy.ollama import chat

class Lucy(cmd.Cmd):
    intro = """
Lucy v2
========
Connected to local Lucy.
Type help for commands.
"""
    prompt = "Lucy> "

    def do_status(self, arg):
        print("Project :", Path.cwd())
        print("Files   :", len(list(Path.cwd().rglob("*"))))

    def do_ls(self, arg):
        for p in sorted(Path.cwd().iterdir()):
            print(p.name)

    def do_pwd(self, arg):
        print(Path.cwd())

    def default(self, line):
        try:
            print()
            print(chat(line))
            print()
        except Exception as e:
            print("ERROR:", e)

    def do_exit(self, arg):
        return True

    def do_quit(self, arg):
        return True

    def emptyline(self):
        pass

def main():
    Lucy().cmdloop()
