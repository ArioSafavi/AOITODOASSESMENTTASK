# SOFTWARE ENGINEERING PROJECT DOCUMENTATION TEMPLATE {#software-engineering-project-documentation-template}
# ALL IMAGES ARE BUGGY AND DIDNT WORK WHEN I DOWNLOADED IT AS A MD FILE SO PLEASE LOOK AT THE PDF FOR THE IMAGES
---

## RATIONALE {#rationale}

This documentation template is designed to help you complete **Component A – Project Documentation** of your Software Engineering Year 12 Personal Project.

**The template supports the four required stages from the syllabus:**

* Identifying and Defining

* Research and Planning

* Producing and Implementing

* Testing and Evaluating

**It also includes essential modelling tools (which are EXAMINABLE in the HSC\!):**

* Context Diagram

* Data Flow Diagrams (DFDs)

* Structure Chart

* IPO Chart

* Data Dictionary

* UML Class Diagram (if OOP)

---

## TITLE PAGE {#title-page}

**Project Title:	Aoi Todo**  
**Student Name:	Ario Safavi**  
**Date:			09/3/26**  
**Course:** Software Engineering Stage 6  
**GitHub URL (if applicable):**

Table of Contents

[SOFTWARE ENGINEERING PROJECT DOCUMENTATION TEMPLATE	1](#software-engineering-project-documentation-template)

[RATIONALE	1](#rationale)

[TITLE PAGE	2](#title-page)

[Syllabus Requirements	5](#heading)

[1\. Identifying and Defining	7](#1.-identifying-and-defining)

[1.1 Problem Statement	7](#1.1-problem-statement)

[1.2 Project Purpose and Boundaries	7](#1.2-project-purpose-and-boundaries)

[1.3 Stakeholder Requirements	7](#1.3-stakeholder-requirements)

[1.4 Functional Requirements	7](#1.4-functional-requirements)

[1.5 Non-Functional Requirements	7](#1.5-non-functional-requirements)

[1.6 Constraints	7](#1.6-constraints)

[1.7 Requirements Analysis and Prioritisation	8](#1.7-requirements-analysis-and-prioritisation)

[2\. Research and Planning	9](#2.-research-and-planning)

[2.1 Development Methodology	9](#2.1-development-methodology)

[2.2 Tools and Technologies	9](#2.2-tools-and-technologies)

[2.3 Gantt Chart / Timeline	9](#2.3-gantt-chart-/-timeline)

[2.4 Communication Plan	9](#2.4-communication-plan)

[2.5 Resource Allocation Justification	9](#2.5-resource-allocation-justification)

[3\. System Design	10](#heading=h.qcc4bg7xshui)

[3.1 Context Diagram	10](#3.1-context-diagram)

[3.2 Data Flow Diagrams (Level 0 and Level 1\)	10](#3.2-data-flow-diagrams-\(level-0-and-level-1\))

[3.3 Structure Chart	10](#3.3-structure-chart)

[3.4 IPO Chart	10](#3.4-ipo-chart)

[3.5 Data Dictionary	10](#3.5-data-dictionary)

[3.6 UML Class Diagram (if OOP)	10](#3.6-uml-class-diagram-\(if-oop\))

[4\. Producing and Implementing	11](#4.-producing-and-implementing)

[4.1 Development Process	11](#4.1-development-process)

[4.2 Key Features Developed	11](#4.2-key-features-developed)

[4.2.1 Back-End Engineering Contribution	11](#4.2.1-back-end-engineering-contribution)

[4.3 Screenshots of Interface	11](#4.3-screenshots-of-interface)

[4.4 Version Control Summary (Optional)	11](#4.4-version-control-summary-\(optional\))

[5\. Testing and Evaluation	12](#heading=h.dtbuxiw2qk41)

[5.1 Testing Methods Used	12](#5.1-testing-methods-used)

[5.2 Test Cases and Results	12](#5.2-test-cases-and-results)

[5.3 Evaluation Against Requirements	12](#5.3-evaluation-against-requirements)

[5.4 Improvements and Future Development	12](#5.4-improvements-and-future-development)

[6\. Feedback, Security and Reflection	13](#6.-feedback,-security-and-reflection)

[6.1 Summary of Client or Peer Feedback	13](#6.1-summary-of-client-or-peer-feedback)

[6.2 Secure Software Design and Data Handling	13](#6.2-secure-software-design-and-data-handling)

[6.3 Personal Reflection	13](#6.3-personal-reflection)

[7\. Appendices	14](#heading=h.emtb6w8gpaqd)

##  {#heading}

# 1\. Identifying and Defining {#1.-identifying-and-defining}

## 1.1 Problem Statement {#1.1-problem-statement}

Todo list applications are often hard to use or have features that limit the possibilities of the application. My project aims to make a todo list that is easy to use and provides features that a student such as myself would use. My life is very unorganized and I find it hard to remember certain tasks that I must complete throughout the day. Other todo lists are not catered to students and lack features such as once every two weeks.  On top of this I am very competitive especially when it comes to myself. The Todo list will feature analytics boards so that I can compete against myself. This project is catered to students and competitive people.

---

## 1.2 Project Purpose and Boundaries {#1.2-project-purpose-and-boundaries}

Aoi Todo aims to become a useful and fun todo list that can make one compete against themselves. Also it should improve productivity of students and be a convenient way to track and manage tasks.

---

## 1.3 Stakeholder Requirements {#1.3-stakeholder-requirements}

Stakeholders include: Me, Other students, Mr Scott, Maksim (because he said he would use it) 

Their needs for my project include an easy to use GUI that is functional, specific features such as analytics(showing information such as how long it takes to complete a task), searching(being able to search through for tasks using keywords), tags(being able to put tasks into certain categories), notifications(Getting desktop reminders that can be adjusted), priority(being able to choose which tasks need to be completed first), setting due dates(being able to set a date when a task is due), pomodoro timer(a time-management tool) and being able to create tasks from natural language.

---

## 1.4 Functional Requirements {#1.4-functional-requirements}

* Create tasks  
* Have a easy to use GUI  
* Be able to check of tasks  
* Set a due date for tasks  
* Have a viewing system of when each task is due (eg. calendar)  
* Have an analytics system in showing graphs of how long it takes to complete tasks and other information such as log on dates  
* Search and filter through tasks  
* Provide notifications and reminders for tasks  
* Set pomodoro timers  
* Create tasks from natural language inputs from the user  
* A log on system and storage of certain tasks  
* Encryption of saved json files

---

## 1.5 Non-Functional Requirements {#1.5-non-functional-requirements}

* Performance \- should be able to run on any computer made after 2010

* Usability \- Needs to be user friendly and able to be used by not so tech savvy teenagers

* Security \- Users should be able to only access their own log in information and all stored json files should be encrypted

* Reliability \- The program should run 100% of the time on laptops that have at least a cpu and a gpu and memory and storage

---

## 1.6 Constraints {#1.6-constraints}

Limitations that affect the project include time constraints and software accessibility. Due to developing the code in a school environment certain packages may be blocked and unusable on top of this I only have until the end of term 2 to finish this project that has a lot of coding involved.

---

## 1.7 Requirements Analysis and Prioritisation {#1.7-requirements-analysis-and-prioritisation}

The requirements were analysed based on how important they are to the main goal of the project which is to make a simple and useful todo list for students. The most important requirements were creating tasks, being able to complete tasks and having an easy to use GUI. These were prioritised because without them the program would not work as a todo list. The next important features were things like analytics, notifications and search. These improve the experience but are not required for the program to function. Lower priority features include natural language input and more advanced analytics. These were harder to implement and due to time and skill constraints may not be fully completed. Some trade-offs had to be made because of time and technical knowledge. For example the natural language feature may be simplified and encryption may not be very advanced. Overall all requirements link back to the main problem which is helping students stay organised and making the process more engaging. 

---

# 2\. Research and Planning {#2.-research-and-planning}

## 2.1 Development Methodology {#2.1-development-methodology}

Agile is the development approach taken to develop Aoi Todo. The Agile development approach is an iterative and incremental project management approach focused on flexibility, collaboration, and continuous delivery of working software. Due to the project having many functional and non-functional requirements it would be better to follow a more open ended development approach. By using Agile it allows the software to be developed in a timely manner to be able to meet the time constraints and also take feedback and start debugging from early in the development process.

---

## 2.2 Tools and Technologies {#2.2-tools-and-technologies}

Python is being used to develop this program as it is what I am best at, it is simple to code in, it is fast and allows me to develop all of my requirements. I am using Tkinter to develop this but if I become aware of any other tools that would help me do this faster I would use that instead. I am using Json files to store information of the user because they are simple, light and have all the necessary tools for the project. To develop this software I will use VSCODE because it is what the school offers. I will use github as version control because it is the best free software to use for version control in my opinion due to the easy accessibility it offers.

---

## 2.3 Gantt Chart / Timeline {#2.3-gantt-chart-/-timeline}

Most of the time was allocated to the development stage since this project involved a large amount of coding across many different features. Planning and research were given two weeks to make sure the requirements were clear before any code was written. Producing and implementing took up the largest block of time since this is where the actual coding debugging and feature additions happened. Testing and evaluation were scheduled towards the end but overlapped with development towards the end.

![][image1]

---

## 2.4 Communication Plan {#2.4-communication-plan}

I received feedback from my peers and Mr Scott by asking them. They offered the idea of the pomodoro timer and the analytics.

---

## 2.5 Resource Allocation Justification {#2.5-resource-allocation-justification}

Most of the time will be spent developing the software and the other will be spent debugging and doing theory. I will use free software so there are not any negatives for the software chosen such as python and github. I used feedback from my peers and teachers to improve my software.

---

# 3\. System Design

This section justifies the use of modelling tools to represent system structure, data flow, and processing logic prior to implementation.

---

## 3.1 Context Diagram {#3.1-context-diagram}

Include a context diagram showing system boundaries and external entities.

![][image2]

---

## 

## 

## 

## 

## 

## 

## 

## 

## 

## 3.2 Data Flow Diagrams (Level 0 and Level 1\) {#3.2-data-flow-diagrams-(level-0-and-level-1)}

Illustrate how data moves through the system.

Level 0:

Level 1:

![][image3]

## 

## 

## 

## 

## 

## 3.3 Structure Chart {#3.3-structure-chart}

Show the modular structure of the system and relationships between modules.

![][image4]

---

## 3.4 IPO Chart {#3.4-ipo-chart}

| Input | Process | Output |
| :---- | :---- | :---- |
| Task info  | Save task | Task saved |
| Login  | Validate  | Access  |
| Time/date  | Check | Reminder  |
| Task data  | Analyse  | Graphs  |

---

## 3.5 Data Dictionary {#3.5-data-dictionary}

| Name | Type | Description | Format for Display | Size (bytes) | Size for Display | Example | Validation |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| username | String | Stores user login name | Plain text | up to 50 | up to 50 characters | Ario | Must not be empty, must not already exist |
| password | String | User password | Plain text (masked on entry) | up to 50 | up to 50 characters | mypassword123 | Must not be empty |
| taskList | List | Stores user's tasks | List of Task objects | variable | depends on task count | \[Task1, Task2\] | Must contain valid Task objects |
| task | Class | A task that user can edit | N/A (object) | variable | N/A | Task("Essay", "DD-MM-YYYY", 1\) | Must have a title |
| title | String | Name of task | Plain text | up to 100 | up to 100 characters | Finish essay | Must not be empty |
| due date | Date | Deadline for task | DD-MM-YYYY | 10 | 10 characters | 25-12-2026 | Must match DD-MM-YYYY format or be blank |
| priority | Integer | Priority level of the task | Whole number, 1–3 | 1 | 1 digit | 2 | Must be between 1 and 3 |
| tags | List | Categories the task belongs to | Comma-separated text | variable | depends on tag count | school, urgent | Each tag must be a non-empty string |
| completed | Boolean | Checks if task is completed or not | True/False | 1 | 1 character | FALSE | Must be True or False |
| save | JSON | Stores saved tasks and analytics | Encrypted binary file | variable | depends on data size | aoi\_data.enc | Must decrypt to valid JSON structure |

## 3.6 UML Class Diagram (if OOP) {#3.6-uml-class-diagram-(if-oop)}

More than one class is needed for this project. It uses a class to define my tasks as it would be easier to have a blueprint for every task. Most of the attributes are public so that they would be able to be accessed and the functions are set to change values of the task along with a function to remind the user when tasks are due. The other class is used to define the Tkinter app and all of the features of the code sit inside there.

![][image5]

---

# 4\. Producing and Implementing {#4.-producing-and-implementing}

## 4.1 Development Process {#4.1-development-process}

The program was built in python through the use of Tkinter. I started with a basic task list and added more features over time such as saving, user accounts and analytics and a pomodoro timer.

The code is split into different sections such as file handling and different themes along with the two main tasks ‘ task’ and ‘aoitodoapp’. Task is the basic functionality of Aoitodo and is the way that tasks are stored and created. Aoitodoapp on the other hand is a Tkinter class and handles the UI. Different functions such as get\_selected\_task are written once and reused across multiple features making the code more readable and modular. Error handling is used by doing a try/except blocks and dictionary lookups use defaults so missing data doesn't take the app down

---

## 4.2 Key Features Developed {#4.2-key-features-developed}

The core of the app is straightforward task management, creating, editing, deleting, and completing tasks, each with a title, due date, priority, and tags. A filter sidebar and an inline search bar with key:value syntax make it easy to find what you need as the list grows. User accounts keep each person's data separate, which is handy on a shared computer. Templates cut down on repetitive entry for tasks that come up regularly. The Pomodoro timer keeps the focus session in the same window as the task list, and the analytics dashboard gives a useful snapshot of productivity trends using data that was already being collected anyway.

---

## 4.2.1 Back-End Engineering Contribution {#4.2.1-back-end-engineering-contribution}

Tasks are converted to plain dictionaries for storage and rebuilt into objects on load, which keeps the storage format separate from how the app actually works with the data. Analytics calculations like durations, streaks, and tag breakdowns are all handled in plain Python without any extra libraries. Input validation is done at the point of entry, registration blocks duplicate usernames, task creation requires a title, and dialog inputs fall back to sensible defaults if left blank. The save file is encrypted using a SHA-256 based XOR cipher so the data is not sitting in readable plaintext. Authentication works by comparing entered credentials against what is stored in the encrypted file, and each login gets timestamped and counted for the analytics view.

---

## 4.3 Screenshots of Interface {#4.3-screenshots-of-interface}


Basic login page with a register button a login button an area to input username and password and a theme changer button

Main GUI all actions can be done through here such as viewing tasks, adding tasks, adding tasks through a template, viewing analytics, setting a timer, loggin out, searching for tasks, and changing themes

After pressing add tasks you are prompted with an input for the task name

After pressing ok you are prompted to input the task due date

Next you are prompted to input the task priority

Finally you are prompted to input any tags associated with the task.

As you can see a new task called hi was created

After selecting the task and pressing complete a picture of conquest appears to confirm you have completed the task

Selecting a task and pressing delete gets rid of the task and does not show it anymore

Selecting templates allows you to add, edit, delete or use a template

Selecting analytics shows your analytics for your account

Selecting pomodoro timer urges you to add how many minutes you  are planning to work for

Next it asks for how many minutes you want a break

After pressing ok it starts the timer and shows it in a window

Changing the view to completed shows this to the user and changing the view to today shows all tasks due today

Pressing logout takes you back to the login page

---

## 4.4 Version Control Summary (Optional) {#4.4-version-control-summary-(optional)}

**Summarise** commits, iterations, or sprints if version control was used.

## Commit 1:

I worked a lot on the code that day. I was able to set up a monitor app and basic adding/deleting of tasks. Some of the code was reused from a previous project and stackoverflow saved me a lot thanks to those two. I was able to bang this out in one day.

## Commit 2:

I again had a lot of time to work on the code that day so i was able to add a save /load system, a theme toggle and most importantly file encryption, this was done with the help of AI (NOT Coded by ai) I didnt know how to encrypt or which type of encryption i should use but i concluded that it did not need to be very complicated and only prevent people from being able to read the save file as a plaintext so i settled on sha 256 and xor hashing.

## Commit 3:

I added themes and some fun easter eggs during class after i finished adding a search bar /filter at the top of the Tkinter, it gave me a lot of trouble but thanks to stack overflow and ai i was able to debug it.

## Commit 4:

I added analytics and tried adding advanced analytics after but they were too buggy and too hard to code so I gave up on them, I added the pomodoro timer as well which in my opinion is the most useful feature of this app. (I am using it while writing this up).

## Commit 5: 

I cleaned up the code and added a templates button so that tasks are reusable. I did this over the weekend and it worked out perfectly (before the due date i might add a bunch of comments for readability)

## Commit 6: 

I added comments to the code nothing to serious just the parts that are hard to read

# 5\. Testing and Evaluation

## 5.1 Testing Methods Used {#5.1-testing-methods-used}

I tested through integrated testing as it being a very big Tkinter project unit testing seemed overkill, so I focused on testing things in context rather than in isolation things like logging with correct and incorrect residential, adding and deleting tasks, switching themes and triggering the easter eggs. I tested every time a new feature was using existing parts of the app or interacted with the existing parts of the app. For example when I added templates I made sure they still worked correctly with the existing task creation flow rather than just testing them on their own. The same went for the save file everytime i added new information that needed to be saved i tested if the save files still loaded correctly without crashing which inspired me to use default values especially throughout the task class.

Testing inspired me to get rid of advanced analytics as it was getting too close to the project due date and the analytics function already worked perfectly fine. I also noticed during testing that deleting as task sometimes selected the wrong row if two tasks had the same title and no due date which is why task lookup heck both title and due together rather than just tile alone.

---

## 5.2 Test Cases and Results {#5.2-test-cases-and-results}

## 

| Test ID | Description | Expected Result | Actual Result | Pass/Fail |
| ----- | ----- | ----- | ----- | ----- |
| TC01 | Valid login | Success message, main window opens | Success message, main window opens | Pass |
| TC02 | Invalid login | Error message shown | Error message shown | Pass |
| TC03 | Register with existing username | Error message, account not created | Error message, account not created | Pass |
| TC04 | Add task with empty title | Dialog cancels, no task added | Dialog cancels, no task added | Pass |
| TC05 | Delete task | Task removed from list and save file | Task removed from list and save file | Pass |
| TC06 | Mark task complete | Status updates to Done, Conquest popup appears | Status updates to Done, Conquest popup appears | Pass |
| TC07 | Search with tag: filter | Only matching tagged tasks shown | Only matching tagged tasks shown | Pass |
| TC08 | Load older save file without templates key | App loads without crashing, empty template list | App loads without crashing, empty template list | Pass |
| TC09 | Open advanced analytics with no completed tasks | Friendly message shown, no crash | Friendly message shown, no crash | Pass |
| TC10 | Export and re-import tasks as JSON | Tasks match original list | Tasks match original list | Pass |

## 

## ---

## 5.3 Evaluation Against Requirements {#5.3-evaluation-against-requirements}

Although I checked off most of my requirements a couple were neglected such as notifications, I originally planned on adding them and all tasks even have a stored variable of ‘notified’ showing how i was originally planning on adding them but the requirement was cut due to it not working on my macbook and being too hard to create separate macbook and windows versions. Also natural language task creation was not implemented due to complexity issues. I originally coded it in but I realised that it was just as convenient to add tasks the normal way so I ended up scrapping it in the final design. A calendar style due date view was planned but I also removed that due to incompatibility with macbook.

Going back to the non-functional requirements set out in section 1,5 performance held up according to plan as the app runs smoothly on a standard laptop and has not slowed down or crashed during testing meeting the original goal of running on any laptop made after 2010\. Usability is great as the GUI is simple enough for someone who isn't savvy to use without needing instruction which was the original target audience. Reliability has also held up as the app never crashed during testing. Unfortunately security is the weakest feature but still not weak as it cannot be read by any one as a plaintext file or as a json file but can still be decrypted due to the hard coded key in the code.

---

## 5.4 Improvements and Future Development {#5.4-improvements-and-future-development}

The biggest limitation is that the notification system was never finished although the groundwork for it was already built but there is no reminder system running in the background. Natural language input was created but not implemented in the final tasks due to its inconvenience.

For future enhancements the next step would be finishing the notification system, likely using a library like plyer to trigger real desktop alerts when tasks become due. Natural language task creation on the other hand is hard because it would require me to use some type of artificial intelligence (maybe a API) because hardcoding it takes away the point of it being ‘natural language’ It could also be worth reexploring a calendar view fondue dates and ignore the fact that it doesn't work on mac.

Another feature that I am interested in adding is recurring tasks as right now every task is a one off so something reoccurring such as tutoring homework weekly has to be re entered every time. Recurring tasks would be regenerated daily, weekly or bi weekly (which would help students as biweekly allows for customization of week a week b tasks).

---

# 6\. Feedback, Security and Reflection {#6.-feedback,-security-and-reflection}

## 6.1 Summary of Client or Peer Feedback {#6.1-summary-of-client-or-peer-feedback}

| Name | Plus | minus | implication |
| :---- | :---- | :---- | :---- |
| Maksim | Good to use and helps with productivity | Basic and there are a lot of apps like it | Better if there was recurring tasks |
| Rufus | Pomodoro timer is great addition and works, helps with productivity | Lots of features that can be more fleshed out | Better if the current features were improved upon |
| Jamie | Works very well, no glitches or bugs and does what it set out to do. | Not very fun to use wish it could have been more fun | Encryption could use work as it is very easy to break in right now. |

---

## 6.2 Secure Software Design and Data Handling {#6.2-secure-software-design-and-data-handling}

Basic security precautions were taken to make sure that the file could not simply be read or accessed. Encryption of the save file instead of simply saving tasks and credentials as plain json was the main one. This was achieved using a sha-256 based xor cipher which would not stand up to high level encryption standards but it does protect the file from being read with a text editor which was the main threat for this risk. Input validation is performed by the app at several different places. For example username entry will not accept duplicates and empty entry will not create a task, registration requires a name and any cancel/blank entries have default values instead of crashing. Error handling is very important in my code as many inputs by the user have the opportunity to crash or harm my system. Therefore all file reading and writing is done with try/catch to ensure that if a user's saved file is missing or corrupt the application will launch into a blank dataset instead of crashing. Dictionary access when loading saved data uses .get() to ensure that no key errors will occur if fields are added or removed after save files have already been made. This means that when variables such as ‘tim\_block’ and ‘notified’ were introduced during the project old save files were still loadable. Aoitodoapp’s weakest point is in its authentication and credential storage. Passwords are saved directly in the encrypted files so if the encryption key were obtained (it is hardcoded in the source code) credential would be viewable. For a single user and on a local sale this security arrangement works fine as the app is not communicating sensitive information over the network and the encryption should ward off casual attackers. On the other hand against more serious attackers this encryption would not hold up as well. However the application is very good at error handling and does not crash even if saved files load fields or information that is unknown.

---

## 6.3 Personal Reflection {#6.3-personal-reflection}

Throughout the project I learnt almost everything, especially since I had almost no prior knowledge of Tkinter before starting. Figuring out how to structure a GUI properly, manage windows, widgets and event driven code taught me a lot on how to program. I learnt especially a lot on how classes are used to create a Tkinter GUI. 

Along with that I learnt about date and time management in python, working with the datetime module to handle due dates, calculate completion duration and figure out streaks for the analytics feature. BUilding the pomodoro timer taught me how to use tkinter’s after() method to create a countdown that updated the GUI without freezing the rest of the app.

I learnt about hashing, sha 256 and how xor encryption works which i used to build a basic encryption system for the save file instead of storing everything as plain text. I also learnt how to properly store and structure information in a json file including how to convert custom objects like tasks into dictionaries and bask again so they could be saved and loaded correctly. 

The bugs that I encountered included a task selection bug where deleting a task would select the wrong row if two tasks shared the same title and had no due date which I fixed by checking both the due date and the title instead of just the tile alone. Also ran into issues with older save files breaking when I added new fields like time\_block and notified which is what led me to use default values throughout the task so older data would still load  properly.

# 7:

Code snippets:

Encryption system:

```py
def _keystream(length: int):
    # builds a repeating SHA-256 keystream long enough to XOR against the data
    stream = b""
    counter = 0
    while len(stream) < length:
        h = hashlib.sha256(SECRET_KEY + counter.to_bytes(4, "big")).digest()
        stream += h
        counter += 1
    return stream[:length]


def encrypt(data: str) -> bytes:
    raw = data.encode("utf-8")
    ks = _keystream(len(raw))
    return bytes(a ^ b for a, b in zip(raw, ks))  # XOR is reversible, same op decrypts


def decrypt(data: bytes) -> str:
    ks = _keystream(len(data))
    raw = bytes(a ^ b for a, b in zip(data, ks))
    return raw.decode("utf-8", errors="ignore")

```

