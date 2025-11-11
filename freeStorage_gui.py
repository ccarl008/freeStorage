import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from threading import Thread
from freeStorage import deleteUserTemp, deleteSysTemp, deleteBrowserCache, isAdmin, runAsAdmin

def startCleanup():
    """Starts cleanup in a new thread after confirmation"""
    confirm = messagebox.askyesno(
        "Confirm Cleanup",
        "Are you sure you want to delete the selected files?"
    )
    if not confirm:
        return

    start_button.configure(state="disabled")
    status_label.configure(text="🧼 Cleaning in progress...")
    progress.set(0)
    Thread(target=runCleanup).start()

def runCleanup():
    """Runs cleanup based on user-selected options with progress tracking"""
    total_tasks = sum([user_temp_var.get(), browser_cache_var.get(), sys_temp_var.get()])
    if total_tasks == 0:
        messagebox.showinfo("No Selection", "Please select at least one cleanup option.")
        start_button.configure(state="normal")
        return

    completed_tasks = 0
    deleted_sections = []

    if user_temp_var.get():
        deleteUserTemp()
        completed_tasks += 1
        deleted_sections.append("User Temp Files")
        progress.set(completed_tasks / total_tasks)

    if browser_cache_var.get():
        deleteBrowserCache()
        completed_tasks += 1
        deleted_sections.append("Browser Cache")
        progress.set(completed_tasks / total_tasks)

    if sys_temp_var.get():
        if isAdmin():
            deleteSysTemp()
            deleted_sections.append("System Temp Files")
        else:
            runAsAdmin()
        completed_tasks += 1
        progress.set(completed_tasks / total_tasks)

    progress.set(1)
    status_label.configure(text="Cleanup Complete!")
    start_button.configure(state="normal")

    summary = "\n".join(f"• {section}" for section in deleted_sections)
    messagebox.showinfo(
        "Cleanup Summary",
        f"✨ Cleanup completed successfully!\n\nDeleted sections:\n{summary}"
    )


# GUI Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("Cresencio's Storage Cleaner")
app.geometry("420x380")

# Title Label
ctk.CTkLabel(
    app,
    text="🧹 Cresencio's Storage Cleaner",
    font=("Segoe UI", 20, "bold")
).pack(pady=15)

# Checkboxes
user_temp_var = ctk.BooleanVar(value=True)
browser_cache_var = ctk.BooleanVar(value=False)
sys_temp_var = ctk.BooleanVar(value=False)

ctk.CTkCheckBox(app, text="Delete User Temporary Files", variable=user_temp_var).pack(anchor="w", padx=25)
ctk.CTkCheckBox(app, text="Delete Browser Cache", variable=browser_cache_var).pack(anchor="w", padx=25)
ctk.CTkCheckBox(app, text="Delete System Temporary Files (Admin Required)", variable=sys_temp_var).pack(anchor="w", padx=25)

# Progress Bar
progress = ctk.CTkProgressBar(app, width=300)
progress.pack(pady=20)
progress.set(0)

# Start Button
start_button = ctk.CTkButton(app, text="Start Cleanup", command=startCleanup, width=200, height=35)
start_button.pack(pady=10)

# Status Label
status_label = ctk.CTkLabel(app, text="", font=("Segoe UI", 12))
status_label.pack(pady=5)

# Exit Button
exit_button = ctk.CTkButton(app, text="Exit", command=app.quit, fg_color="#444")
exit_button.pack(pady=5)

app.mainloop()
