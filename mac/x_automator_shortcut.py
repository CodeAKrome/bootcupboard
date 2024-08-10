import subprocess

def create_shortcut():
    applescript = '''
    tell application "Automator"
        set newWorkflow to make new workflow
        tell newWorkflow
            make new action with properties {class:run shell script action, properties:{shell:"/bin/bash", source:"open -a 'Shortcuts' 'shortcuts://create-shortcut?name=Hello%20World&actions=%5B%7B%22WFWorkflowActionIdentifier%22:%22is.workflow.actions.showresult%22,%22WFWorkflowActionParameters%22:%7B%22Text%22:%7B%22Value%22:%7B%22attachmentsByRange%22:%7B%7D,%22string%22:%22Hello%20World%22%7D%7D%7D%7D%5D'"}}
        end tell
        save newWorkflow in (POSIX file "/tmp/CreateShortcut.workflow")
    end tell

    tell application "Finder"
        open POSIX file "/tmp/CreateShortcut.workflow"
    end tell
    '''
    
    try:
        subprocess.run(["osascript", "-e", applescript], check=True)
        print("Automator workflow created and executed. Check the Shortcuts app for the new shortcut.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_shortcut()