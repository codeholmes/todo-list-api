from flask import Flask, request
import pandas as pd
from datetime import datetime
import os


class TodoListAPI:
    def __init__(self):
        if os.path.exists("tasks.csv"):
            try:
                self.df = pd.read_csv("tasks.csv")
            except pd.errors.EmptyDataError:
                self.df = pd.DataFrame(columns=["task_name", "completed", "created_at"])
        else:
            self.df = pd.DataFrame(columns=["task_name", "completed", "created_at"])

    def index(self):
        """List of tasks!"""
        return self.df.to_dict()

    def create(self):
        """Create a task"""
        task = request.data.decode("utf-8")
        created_at = datetime.today()  # default
        task_completed = False  # default
        new_task = [[task, task_completed, created_at]]
        task_df = pd.DataFrame(
            new_task, columns=["task_name", "completed", "created_at"]
        )
        self.df = self.df.append(task_df, ignore_index=True)
        self.df.index = range(len(self.df))
        self.df["id"] = self.df.index
        self.df.to_csv("tasks.csv", index=False)

        return new_task, 200

    def delete():
        """Delete a task"""
        # To do
        return "Deleting.."

    def update_task():
        """Update a task"""
        # To do
        return "Updating.."

    def update_status():
        # To do
        return "Updating.."
