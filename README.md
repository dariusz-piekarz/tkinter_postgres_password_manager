# Password Manager Application

## Preliminaries:

Before using the app, ensure that PostgreSQL and pgAdmin 4 are installed on your system. Create a server with password protection (typically with *host* = 'localhost', *port* = '5432', *database* = 'postgres', *user* = 'postgres').
In case of any issues, refer to the following guide: [Stack Overflow - Setting password for the 'postgres' user in pgAdmin 4](https://stackoverflow.com/questions/64198359/pg-admin-4-password-for-postgres-user-when-trying-to-connect-to-postgresql-1).
Create a new *database* with a name of your choice, a *schema*, and a *table*. The table must contain the following fields (field_name, field_type, primary key, not_null):
- ("Name", text, True, True),
- ("Login", text, False, False),
- ("Password", text, False, False),
- ("Email", text, False, False),
- ("PIN", integer, False, False),
- ("Phone Number", text, False, False),
- ("Comment", text, False, False).
Then, update the config.json file with the database name, host, port, and table_name.

## Usage:

Your login credentials are the same as specified in PostgreSQL (most likely 'postgres'), and the password is the one you set up earlier for the server.
After logging in, you can:
- Display existing passwords by "Name",
- Delete records,
- Modify existing records,
- Insert new records.

