#!/usr/bin/python3
"""contain the entry point of the command interpreter"""
import cmd
from models.base_model import BaseModel
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.user import User
from models import storage


class HBNBCommand(cmd.Cmd):
    """contains the method for the commands for the interpreter"""
    prompt = "(hbnb) "
    __classes = ["BaseModel", "Place", "State", "City", "Amenity", "Review", "User"]

    def default(self, line):
        """The default behavior for cmd module when input is invalid"""
        clsname = line.split(".")[0]
        try:
            rest = line.split(".")[1]
        except IndexError:
            print("** invalid command **")
            return
        """print(clsname, rest)"""
        if rest == "create()":
            self.do_create(clsname) 
        elif rest == 'all()':
            self.do_all(clsname)
        elif rest[:5] == 'show(':
            self.do_show(clsname + ' ' + rest[6:-2])
        elif rest[:7] == "count()":
            self.do_count(clsname)
        elif rest[:8] == "destroy(":
            self.do_destroy(clsname + ' ' + rest[9:-2])
        elif rest[:7] == "update(":
            """User.update("38f22813-2753-4d42-b37c-57a17f1e4f88", {'first_name': "John", "age": 89})
            User.update("38f22813-2753-4d42-b37c-57a17f1e4f88", "first_name", "John")
            User.update("38f22813-2753-4d42-b37c-57a17f1e4f88", "age", 89)"""
            li = rest[7:].split(",")
            print(li)
            oid = li[0].replace('"', '')
            att = li[1].replace(' ', '').replace('"', '')
            if '"' in li[2]:
                val = li[2].replace(' ', '').replace('"', '')
            else:
                val = int(li[2].replace(' ', ''))

            print(clsname, oid, att, val)

            self.do_update(clsname + ' ' + oid + ' ' + att + ' ' + str(val))


        else:
            print("** invalid command **")

    def emptyline(self):
        """Define the behaviour of the interpreter when command is empty"""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program"""
        print("")
        return True

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it adn prints the id"""
        argv = arg.split()
        if len(argv) == 0:
            print("** class name missing **")
        elif argv[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argv[0])().id)
            storage.save()

    def do_show(self, arg):
        """Prints the string representation of an instance based on the class
        name and the id"""
        argv = arg.split()
        objs = storage.all()
        if len(argv) == 0:
            print("** class name missing **")
        elif argv[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argv) == 1:
            print("** instance id is missing **")
        elif "{}.{}".format(argv[0], argv[1]) not in objs:
            print("** no instance found **")
        else:
            on = "{}.{}".format(argv[0], argv[1])
            print(objs[on])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id, save changes"""
        argv = arg.split()
        objs = storage.all()
        if len(argv) == 0:
            print("** class name missing **")
        elif argv[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argv) == 1:
            print("** instance id is missing **")
        elif "{}.{}".format(argv[0], argv[1]) not in objs:
            print("** no instance found **")
        else:
            on = "{}.{}".format(argv[0], argv[1])
            del objs[on]
            storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances based or not
        on the class name"""
        argv = arg.split()
        objs = storage.all()
        pl = []
        if len(argv) > 0 and argv[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        else:
            for obj in objs.values():
                if len(argv) > 0 and argv[0] == obj.__class__.__name__:
                    pl.append(obj.__str__())
                elif len(argv) == 0:
                    pl.append(obj.__str__())
        print(pl)

    def do_update(self, arg):
        """Update an instance based on the class name and id by adding or
        updating attribute
        update Class id attribute value
        """
        argv = arg.split()
        objs = storage.all()
        if len(argv) == 0:
            print("** class name missing **")
        elif argv[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argv) == 1:
            print("** instance id is missing **")
        elif "{}.{}".format(argv[0], argv[1]) not in objs:
            print("** no instance found **")
        elif len(argv) == 2:
            print("** attribute name missing **")
        elif len(argv) == 3:
            print("** value missing **")
        elif argv[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            for oid in objs.keys():
                if oid == "{}.{}".format(argv[0], argv[1]):
                    setattr(objs[oid], argv[2], argv[3])
                    objs[oid].save()
                    storage.save()

    def do_count(self, arg):
        """Retrieve the number of instances of a given class."""
        argv = arg.split()
        objs = storage.all()
        count = 0
        if argv:
            for obj in objs.values():
                if obj.__class__.__name__ == argv[0]:
                    count += 1
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
