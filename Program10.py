# Program 10: Bug Tracking System

class BugTracker:
    def __init__(self):
        # Dictionary to store bugs
        # Format: { bug_id: {"description": str, "severity": str, "status": str} }
        self.bugs = {}

    def add_bug(self, bug_id: str, description: str, severity: str) -> None:
        """Add a new bug with default status 'Open'."""
        if bug_id in self.bugs:
            print(f"Bug ID {bug_id} already exists!")
        else:
            self.bugs[bug_id] = {
                "description": description,
                "severity": severity,
                "status": "Open"
            }
            print(f"Bug {bug_id} added successfully.")

    def update_status(self, bug_id: str, new_status: str) -> None:
        """Update the status of an existing bug."""
        if bug_id in self.bugs:
            self.bugs[bug_id]["status"] = new_status
            print(f"Bug {bug_id} status updated to {new_status}.")
        else:
            print(f"Bug ID {bug_id} not found!")

    def list_all_bugs(self) -> None:
        """Print details of all bugs in a readable format."""
        if not self.bugs:
            print("No bugs found.")
        else:
            print("\n=== Bug Records ===")
            for bug_id, details in self.bugs.items():
                print(f"Bug ID      : {bug_id}")
                print(f"Description : {details['description']}")
                print(f"Severity    : {details['severity']}")
                print(f"Status      : {details['status']}")
                print("-" * 30)


if __name__ == "__main__":
    # Create BugTracker object
    tracker = BugTracker()

    # Add at least three bugs
    tracker.add_bug("BUG001", "Login button not working", "High")
    tracker.add_bug("BUG002", "Profile picture upload fails", "Medium")
    tracker.add_bug("BUG003", "Settings page loads slowly", "Low")

    # Update statuses
    tracker.update_status("BUG002", "In Progress")
    tracker.update_status("BUG003", "Closed")

    # List all bugs
    tracker.list_all_bugs()
