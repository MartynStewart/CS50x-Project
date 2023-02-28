import re
input = "!Quack projects"
TRIGGER = "!Quack"


def actions(message, uid):
    message = message.replace("[","").replace("]","")
    command = message.split()
    if command[0].upper() == TRIGGER:

        if command[1].upper() == "PROJECTS" and len(command) == 2:
            return ("Display Projects")
        elif command[1].upper() == "OFFERS" and len(command) == 2:
            return ("Display Project Offers")
        elif command[1].upper() == "CREATE" and len(command) == 3:
            return (f"Create Project named: {command[2]}")
        elif command[1].upper() == "JOIN" and len(command) == 3:
            return (f"Offer to join Project named: {command[2]}")
        

        elif command[1].upper() == "HELP" and len(command) == 3 and command[2].upper() == "PROJECTS":
            return (f"Usage: \"{TRIGGER} PROJECTS\". Displays a list of all avalible projects looking for help")
        elif command[1].upper() == "HELP" and len(command) == 3 and command[2].upper() == "OFFERS":
            return (f"Usage: \"{TRIGGER} OFFERS\". If you've created a project with me this will tell you all the users who have signed up")
        elif command[1].upper() == "HELP" and len(command) == 3 and command[2].upper() == "CREATE":
            return (f"Usage: \"{TRIGGER} CREATE [project_name]\" note project name must be all 1 word. This will create a new project as you as the owner, If the name is already in use then I will adjust it")
        elif command[1].upper() == "HELP" and len(command) == 3 and command[2].upper() == "JOIN":
            return (f"Usage: \"{TRIGGER} JOIN [project_name]\" note project name must be exact. Will signal you would like to help out with the project")
        

        elif command[1].upper() == "HELP" and len(command) == 2:
            return ("Avalible commands are: [projects], [offers], [create] and [join]. For further info you can type \"!quack help [command]\" ")
        else:
            return ("Sorry that command wasn't found. Try !help for how I work")

print(actions(input, 132))