tasks = []
def addTask():
 
    

    
    title = input("Input the title of your work")
    priority = input("Enter your work priority")
    tasks.append ( {"title" : title,
                    "done" : False,
                     " priority" : priority}
    )
    for task in tasks:
        if task["title"].lower() == title.lower():
                  print("This task already exists")
        return
                     
                  
    
    

def removeTask():
    taskToBeRemoved = input("Enter which task you want to remove")
    tasks.remove = {"title" : taskToBeRemoved}

def modifytask():
    taskModification = input("Enter which task to modify ")
    modification = input("Enter your modified task")
    priority = input("Enter your priority")
    if(tasks["title"].lower() == taskModification):
          tasks.append( {
                "title" : modification,
                "done" : False,
                "priority": priority
                
          })

def displayTaskDetail():
      print(tasks)

def displayAllTasks():
     for task in tasks:
      print(task["title"])

def exit():
     print("Thank You For Using Our Service")
     return


while True:
    print("""
    1. Add Task
    2. Delete Task
    3. Display Task Detail
    4. Display All tasks
    5. Modify Task
    6. exit
    
    """)    
    choice = int(input("Enter your choice"))
    if choice == 1:
          addTask()
    elif choice == 2:
          removeTask()
    elif choice == 5:
          modifytask()
    elif choice == 3 :
        displayTaskDetail()
    elif choice == 4:
         displayAllTasks()
    elif choice == 6:
         exit()
    

    


 
