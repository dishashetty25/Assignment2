# Socket Programming Assignment

This is a simple client-server socket programming assignment using Python and SQLite.

## Structure

- `server.py`: Waits for connections, performs SELECT, INSERT, DELETE on the database.
- `client.py`: Takes formatted string input from CLI and communicates with the server.
- `logs.txt`: Logs all client responses with timestamps.

## Example Commands

```bash
python client.py "2|BOOKS|BookID=105, Title=Python, Author=Alice, Genre=Tech, YearPublished=2024"
python client.py "1|BOOKS|105"
python client.py "3|BOOKS|105"
