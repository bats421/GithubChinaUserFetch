# GithubChinaUserFetch
Fetch Github China users by Python with Github GraphQL API.

## Config

Create `config.yml` as config file at project root directory, and write this line below:

```yaml
token: xxx
```

Follow the steps in "[Creating a personal access token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)" to create a token and fill in config file. The scope requires **repo**, **admin:org** and **user** to fetch data.

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## API

### `class.User.fetch(num=10, batch_size=10)`

Executing GraphQL query to fetching Github China's users.

Parameters:

- `num`: How many users you want to fetch?
- `batch_size`: How many users to fetch in a request?

### `class.User.toDataFrame()`

Transform data to Pandas DataFrame.

### `class.User.saveCSV(fileName, mode)`

Write DataFrame to file. Notice: you must run `toDataFrame()` before calling this function.

Parameters:

- `fileName`: The file name you want to write.
- `mode`: Writing mode
  - `a`: append to file
  - `w`: overwrite the file

## License

This project is licensed under the terms of the MIT license.