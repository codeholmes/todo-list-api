# TodoList API

Backend app for TODO list management

## Features

-   Create a new task
-   Delete an existing task
-   Update an existing task
-   Update task completion status

## Installation

Clone the project & change the directory to `todo-list-api` root

```sh
git clone https://github.com/codeholmes/todo-list-api.git
cd todo-list-api/
```

Create a virtual environment in the project root & activate it

```sh
python3 -m venv .
source bin/activate
```

Install the dependencies in the virtual environment

```sh
pip3 install -r requirements.txt
```

## Run

Run the app use following code, it will start a `Flask` server:

```sh
python3 api.py
```

## Endpoints

| Endpoints                 | Method Allowed |
| ------------------------- | -------------- |
| `/todo`                   | `GET`          |
| `/create`                 | `POST`         |
| `/delete/<int:id>`        | `DELETE`       |
| `/update_task/<int:id>`   | `PUT`          |
| `/update_status/<int:id>` | `PUT`          |

## Testing

_[Note: Make sure `ipython` & `requests` is installed, if not, follow the link for installation for `ipython` from [here](https://ipython.org/install.html), and for `requests` from [here](https://pypi.org/project/requests/)]_

Run `ipython`

```
ipython
```

Once you're in `ipython` shell, try out testing example:

```sh
import requests
requests.get("http://127.0.0.1:5000/todo")
```

It should return `<Response [200]>` but the response (.text) won't have any data, to add data (task) use try the following code (replace the port with the one you're using)

#### `/create`

```sh
res = requests.post("http://127.0.0.1:5000/create", data="Write requirement file")
res.text
```

Output
`'{"1": {"task_name": "Write requirement file", "completed": "False", "created_at": "2023-02-16 12:06"}}'`

## Docker

[Todo]

## Edge cases covered

[Todo]
