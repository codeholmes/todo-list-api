from flask import request
import pandas as pd
from datetime import datetime
import os
import json


class TodoListAPI:
    def __init__(self):
        # check if the file exist
        if os.path.exists("tasks.csv"):
            try:  # read the file
                self.df = pd.read_csv("tasks.csv")
            # if the file is empty
            except pd.errors.EmptyDataError:
                # create columns
                self.df = pd.DataFrame(
                    columns=["task_name", "completed", "created_at", "task_id"]
                )
        # create columns
        else:
            self.df = pd.DataFrame(
                columns=["task_name", "completed", "created_at", "task_id"]
            )

    def todo(self):
        """This function will return all the tasks and it's
        associated attributes in a dict data type"""
        todo_dict_raw = self.df.to_dict()
        # segregating each items
        task_id = [
            [j for i, j in v.items()]
            for k, v in todo_dict_raw.items()
            if k == "task_id"
        ][0]
        task_name = [
            [j for i, j in v.items()]
            for k, v in todo_dict_raw.items()
            if k == "task_name"
        ][0]
        created_at = [
            [str(j) for i, j in v.items()]
            for k, v in todo_dict_raw.items()
            if k == "created_at"
        ][0]
        completed = [
            [str(j) for i, j in v.items()]
            for k, v in todo_dict_raw.items()
            if k == "completed"
        ][0]
        # making a dict structure
        todo_dict = {
            task_id[i]: {
                "task_name": task_name[i],
                "completed": completed[i],
                "created_at": created_at[i],
            }
            for i in range(len(task_id))
        }
        return todo_dict, 200

    def create(self):
        """This function creates a new task"""
        # decode and store the data from the request body
        task = request.data.decode("utf-8")
        # check for data length
        if len(task.strip()) != 0:
            # if length not 0, capture current time, task status as false
            created_at = datetime.strftime(
                datetime.today(), "%Y-%m-%d %H:%M"
            )  # default
            task_completed = False  # default
            task_id = int(1) if self.df.empty else (self.df["task_id"].max() + 1)
            new_task = [[task, task_completed, created_at, task_id]]
            # make a pandas dataframe
            task_df = pd.DataFrame(
                new_task, columns=["task_name", "completed", "created_at", "task_id"]
            )
            # append it to the df
            self.df = pd.concat([self.df, task_df], ignore_index=True)
            self.save_to_csv()  # write to csv file
            created_task = {
                "task_id": int(new_task[0][3]),
                "task_name": new_task[0][0],
                "completed": new_task[0][1],
                "created_at": new_task[0][2],
            }
            return created_task, 200
        else:
            # if the request body is empty
            return "No input provided!", 400

    def delete(self, id):
        """This function drops a row, reset the ids, and save them back with new ids"""
        for index, row in self.df.iterrows():
            if row["task_id"] == id:
                task_name = self.df.loc[self.df["task_id"] == id]["task_name"].values[0]
                self.df = self.df.drop(index)  # drop the row
                self.save_to_csv()
                return (
                    f"Task '{task_name}' with ID '{id}' deleted!".format(
                        task_name=task_name, id=id
                    ),
                    200,
                )
        return f"ID ({id}) not found!".format(id=id), 400

    def update_task(self, id):
        """This function updates the existing task_name, and save it back"""
        updated_task = request.data.decode("utf-8")
        # check whether the updated_task is empty or not, then continue
        if len(updated_task.strip()) != 0:
            for index, row in self.df.iterrows():
                if row["task_id"] == id:
                    # assign the task_name with updated one
                    self.df.loc[index, "task_name"] = updated_task
                    self.save_to_csv()
                    return self.df.iloc[index].to_dict(), 200
            # return below if id not exist or invalid
            return f"ID ({id}) not found!".format(id=id), 400
        else:
            return "Invalid input. Empty entry not allowed.", 400

    def update_status(self, id):
        """This function updates the status (True or False) of the task, and save it back"""
        new_status = request.data.decode("utf-8")
        # check whether new_status having string "true" or "false"
        if str(new_status).lower().strip() in ["true", "false"]:
            # strip the whitespaces, capitalize, convert the str into bool and
            # assign it to the "completed" column
            for index, row in self.df.iterrows():
                if row["task_id"] == id:
                    self.df.loc[index, "completed"] = bool(
                        str(new_status).capitalize().strip()
                    )
                    self.save_to_csv()
                    return self.df.iloc[index].to_dict(), 200
            # return below if id not exist or invalid
            return f"Invalid ID ({id})".format(id=id), 400
        # return below if data is some random text or empty
        return "Invalid input. This endpoint only accepts: True/False", 400

    def save_to_csv(self):
        """This function writes the data (df) to a csv file"""
        # convert df into csv
        self.df.to_csv("tasks.csv", index=False)
