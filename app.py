from flask import Flask, request
import pandas as pd
from datetime import datetime
import os


class TodoListAPI:
    def __init__(self):
        # check if the file exist
        if os.path.exists("tasks.csv"):
            try:  # read the file
                self.df = pd.read_csv("tasks.csv")
            # if the file is empty
            except pd.errors.EmptyDataError:
                # create columns
                self.df = pd.DataFrame(columns=["task_name", "completed", "created_at"])
        # create columns
        else:
            self.df = pd.DataFrame(columns=["task_name", "completed", "created_at"])

    def index(self):
        """This function will return all the tasks and it's
        associated attributes in a dict data type"""
        return self.df.to_dict()

    def create(self):
        """This function creates a new task"""
        # decode and store the data from the request body
        task = request.data.decode("utf-8")
        # check for data length
        if len(task.strip()) != 0:
            # if length not 0, capture current time, task status as false
            created_at = datetime.today()  # default
            task_completed = False  # default
            new_task = [[task, task_completed, created_at]]
            # make a pandas dataframe
            task_df = pd.DataFrame(
                new_task, columns=["task_name", "completed", "created_at"]
            )
            # append it to the df
            # self.df = self.df.append(task_df, ignore_index=True)
            self.df = pd.concat([self.df, task_df], ignore_index=True)
            self.reset_index()  # reset the index and give each row an id
            self.save_to_csv()  # write to csv file
            return new_task, 200
        else:
            # if the request body is empty
            return "No input provided!", 400

    def delete(self, id):
        """This function drops a row, reset the ids, and save them back with new ids"""
        # find the task name for later returning it upon success drop of task
        try:
            task_name = self.df[self.df["id"] == id]["task_name"].values[0]
            self.df = self.df.drop(id)  # drop the row
            self.reset_index()
            self.save_to_csv()
            return "'{task_name}' deleted!".format(task_name=task_name), 200
        except IndexError:
            return "ID ({id}) not found!".format(id=id), 400

    def update_task(self, id):
        """This function updates the existing task_name, and save it back"""
        try:
            updated_task = request.data.decode("utf-8")
            old_task = self.df.loc[id, "task_name"]
            # reassign the task_name with updated one
            self.df.loc[id, "task_name"] = updated_task
            self.save_to_csv()
            return {"old_task": old_task, "updated_task": updated_task}, 200
        except IndexError:
            return "ID ({id}) not found!".format(id=id), 400

    def update_status(self, id):
        """This function updates the status (True or False) of the task, and save it back"""
        try:
            new_status = request.data.decode("utf-8")
            # check whether new_status having string "true" or "false"
            if str(new_status).lower().strip() in ["true", "false"]:
                # strip the whitespaces, capitalize, convert the str into bool and
                # assign it the "completed" column
                self.df.loc[id, "completed"] = bool(
                    str(new_status).capitalize().strip()
                )
                self.save_to_csv()
                return self.df.iloc[id].to_dict(), 200
            else:
                return "Invalid input!", 400
        except IndexError:
            return "ID ({id}) not found!".format(id=id), 400

    def reset_index(self):
        """This function reset the index,
        creates a new column named 'id' and
        assign each row (id) newly generated index"""
        self.df.index = range(len(self.df))
        # creating an "id" column with id as their index value
        self.df["id"] = self.df.index

    def save_to_csv(self):
        # convert df into csv
        self.df.to_csv("tasks.csv", index=False)
