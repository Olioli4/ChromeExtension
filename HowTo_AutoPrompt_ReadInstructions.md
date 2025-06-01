Dear Olivier

## How to Automatically Prompt Users to Read Project Instructions on VS Code Startup

When collaborating on a project, it’s important that all contributors read the user or setup instructions before making changes. You can configure your VS Code workspace to automatically remind users to read a specific instructions file (like `Instructions.instructions.md`) every time the project is opened—with a direct link to open it.

### Why Do This?

- **Consistency:** Ensures all users see important guidelines or onboarding steps.
- **Onboarding:** New contributors won’t miss critical setup or usage notes.
- **Automation:** Reduces the need for manual reminders or documentation checks.
- **Convenience:** A direct link makes it easy for users to open the instructions immediately.

### How It Works

1. **Create a VS Code Task:**  
   In your `.vscode/tasks.json`, define a shell task that displays a message with a clickable link to your instructions file. For example:
   ```json
   {
     "label": "read-user-instructions-on-start",
     "type": "shell",
     "command": "echo Please read the USER INSTRUCTIONS for this project. Open them here: vscode://file/${workspaceFolder}/Instructions.instructions.md",
     "isBackground": false,
     "group": "build"
   }
   ```
   This uses the `vscode://file/` URI scheme, which allows users to click the link in the terminal and open the file directly in VS Code.

2. **Install and Configure the Auto Run Command Extension:**  
   In your `.vscode/settings.json`, configure the [Auto Run Command](https://marketplace.visualstudio.com/items?itemName=ctf0.auto-run-command) extension to automatically run the task when the workspace contains your instructions file:
   ```json
   {
     "auto-run-command.commands": [
       {
         "command": "workbench.action.tasks.runTask",
         "args": "read-user-instructions-on-start",
         "when": [
           "workspaceContains:Instructions.instructions.md"
         ]
       }
     ]
   }
   ```

3. **Result:**  
   Now, whenever someone opens the workspace in VS Code, the task runs automatically and prints a message with a clickable link to open the instructions file.

---

This approach helps maintain project quality and ensures everyone is on the same page from the start—with the added convenience of a direct link to the instructions.
