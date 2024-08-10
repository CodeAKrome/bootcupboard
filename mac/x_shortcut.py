import subprocess
import platform

class MacShortcuts:
    def __init__(self):
        if platform.system() != "Darwin":
            raise OSError("This class is only compatible with macOS.")
        
        # Check if the shortcuts command-line tool is available
        try:
            subprocess.run(["shortcuts", "-h"], capture_output=True, check=True)
        except subprocess.CalledProcessError:
            raise OSError("The shortcuts command-line tool is not available. "
                          "Make sure you have Shortcuts app installed and "
                          "Command Line Tools enabled in Xcode.")

    def list_shortcuts(self):
        """List all available shortcuts."""
        result = subprocess.run(["shortcuts", "list"], capture_output=True, text=True, check=True)
        return result.stdout.strip().split('\n')

    def run_shortcut(self, shortcut_name):
        """Run a shortcut by its name."""
        try:
            result = subprocess.run(["shortcuts", "run", shortcut_name], 
                                    capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Error running shortcut '{shortcut_name}': {e.stderr.strip()}")

    def run_shortcut_with_input(self, shortcut_name, input_data):
        """Run a shortcut with input data."""
        try:
            result = subprocess.run(["shortcuts", "run", shortcut_name, "-i", input_data], 
                                    capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Error running shortcut '{shortcut_name}' with input: {e.stderr.strip()}")

# Example usage
if __name__ == "__main__":
    try:
        mac_shortcuts = MacShortcuts()
        
        # List all shortcuts
        print("Available shortcuts:")
        for shortcut in mac_shortcuts.list_shortcuts():
            print(f"- {shortcut}")
        
        # Run a shortcut
        shortcut_name = "My Shortcut"
        result = mac_shortcuts.run_shortcut(shortcut_name)
        print(f"\nResult of running '{shortcut_name}':")
        print(result)
        
        # Run a shortcut with input
        shortcut_with_input = "Shortcut With Input"
        input_data = "Hello, Shortcut!"
        result_with_input = mac_shortcuts.run_shortcut_with_input(shortcut_with_input, input_data)
        print(f"\nResult of running '{shortcut_with_input}' with input:")
        print(result_with_input)
        
    except (OSError, ValueError) as e:
        print(f"Error: {e}")
