import os
import FreeCAD as App
import FreeCADGui as Gui

class GitSaveObserver:
    def __init__(self):
        # Store QtWidgets inside the class instance to protect it from garbage collection
        try:
            from PySide6 import QtWidgets, QtCore
            self.QtWidgets = QtWidgets
            self.QtCore = QtCore
        except ImportError:
            App.Console.PrintWarning("PySide6 is not accessible in this context.\n")
            self.QtWidgets = None
            self.QtCore = QtCore = None

        # Store the git module inside the class instance
        try:
            import git
            self.git = git
        except ImportError:
            App.Console.PrintWarning("GitPython is not installed. Git automatic commit disabled.\n")
            self.git = None

    def slotFinishSaveDocument(self, doc, filename=""):
        App.Console.PrintMessage(f"[Git] Catching post-save event for document: {doc.Name}\n")
        
        if not self.git or not self.QtWidgets or not self.QtCore:
            return
        
        # Capture absolute file path of the document saved
        filepath = doc.FileName
        if not filepath:
            return 

        # Identify parent Git repository root directories
        try:
            repo_dir = self.git.Repo(filepath, search_parent_directories=True).working_tree_dir
            repo = self.git.Repo(repo_dir)
        except self.git.InvalidGitRepositoryError:
            return 

        relative_path = os.path.relpath(filepath, repo_dir)
        
        # Extract the string path correctly from the GitPython index keys tuple (path, stage)
        is_tracked = any(entry_key == relative_path for entry_key in repo.index.entries.keys())
        is_modified = relative_path in [item.a_path for item in repo.index.diff(None)]
        
        if is_tracked or is_modified:
            # THREAD FIX: Use QTimer to schedule the dialog invocation on the next main UI event loop cycle.
            # This detaches the dialog box from FreeCAD's low-level saving thread and breaks the deadlock.
            self.QtCore.QTimer.singleShot(0, lambda: self.prompt_git_commit(repo, filepath, relative_path))

    def prompt_git_commit(self, repo, filepath, relative_path):
        # The main UI event loop is now fully unfrozen, giving the window full typing focus
        text, ok = self.QtWidgets.QInputDialog.getText(
            Gui.getMainWindow(), 
            'Git Commit Comment', 
            f'Provide a commit message for {os.path.basename(filepath)}:'
        )
        
        if ok and text:
            try:
                repo.index.add([filepath])
                repo.index.commit(text)
                App.Console.PrintMessage(f"[Git] Successfully committed {relative_path} with message: '{text}'\n")
            except Exception as e:
                App.Console.PrintError(f"[Git] Error committing file: {str(e)}\n")
        else:
            App.Console.PrintWarning("[Git] Commit cancelled by user or empty comment.\n")

# Safely latch the class into memory and check for module activation trace
if not hasattr(App, "__git_observer_instance__"):
    observer_instance = GitSaveObserver()
    
    if observer_instance.git and observer_instance.QtWidgets:
        App.__git_observer_instance__ = observer_instance
        App.addDocumentObserver(App.__git_observer_instance__)
        App.Console.PrintMessage("[Git] Automatic Save Observer registered and hooked successfully.\n")


