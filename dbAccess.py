import os
from dotenv import load_dotenv
import sqlite3

con = sqlite3.connect("projects.db")
cursor = con.cursor()

#   Used to finalise any db inserts otherwise they don't stick
def commit():
    con.commit()   #commented out for testing


def getProjectID(ProjectName):
    cursor.execute("SELECT COUNT(project_name), ID FROM activeProjects WHERE project_name = ?;",(ProjectName,))
    project = cursor.fetchall()
    if(int(project[0][0]) > 0):
        return int(project[0][1])
    return -1


def isProjectNameUsed(ProjectName):
    if (getProjectID(ProjectName) == -1):
          return False
    return True


def getUniqueName(seed, ProjectName):
    sum = 0
    for digit in str(seed): 
      sum += int(digit)

    newName = ProjectName + str(sum)

    if(isProjectNameUsed(newName)):
         newName = getUniqueName(seed + 1, ProjectName)
    return newName


def ActiveProjects():
    cursor.execute("SELECT * FROM activeProjects;")
    rows = cursor.fetchall()
    return rows


def FindSignUps(uID):
    cursor.execute("SELECT activeParticipants.helper, activeProjects.project_name FROM activeParticipants JOIN activeProjects ON activeParticipants.project_id = activeProjects.ID WHERE activeProjects.owner = ?;", (uID, ) )
    rows = cursor.fetchall()
    return rows


def CreateProject(uID, ProjectName):
        ProjectName = ProjectName.upper()
        if isProjectNameUsed(ProjectName):
             ProjectName = getUniqueName(uID, ProjectName)
        values = (uID, ProjectName)
        cursor.execute("INSERT INTO activeProjects (owner, project_name) VALUES (?, ?);", values)
        commit()
        return(f"Successfully created new project: {ProjectName}")


def CreateSignUp(uID, ProjectName):
        ProjectName = ProjectName.upper()
        projectID = getProjectID(ProjectName)
        if(projectID > 0):
             values = (projectID, uID)
             cursor.execute("INSERT INTO activeParticipants (project_id, helper) VALUES (?, ?);", values)
             commit()
             return True
        else:
             return False


def DeleteProject(uID, ProjectName):
    ProjectName = ProjectName.upper()
    cursor.execute("SELECT ID FROM activeProjects WHERE owner = ? AND project_name = ?",(uID, ProjectName))
    projectID = cursor.fetchall()[0][0]
    if(projectID > 0):
        cursor.execute("DELETE FROM activeProjects WHERE ID = ?;", (projectID, ))
        cursor.execute("DELETE FROM activeParticipants WHERE project_id = ?;", (projectID, ))
        commit()
        return True
    else:
        return False

def DeleteOffer(uID, ProjectName):
    ProjectName = ProjectName.upper()
    cursor.execute("SELECT ID FROM activeProjects WHERE project_name = ?",(ProjectName, ))
    projectID = cursor.fetchall()[0][0]
    if(projectID > 0):
        cursor.execute("DELETE FROM activeParticipants WHERE project_id = ? AND helper = ?;", (projectID, uID))
        commit()
        return True
    else:
        return False
