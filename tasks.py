from invoke import task
import users


@task(help={
    'filename': 'The input file to read users from'
})
def upsert(_, filename):
    """Insert or Create the users in the specified file."""
    users.upsert_from_file(filename)


@task(help={
    'filename': "The input file to read user-group associations"
})
def assign_group(_, filename):
    """Assigns the users to the specified groups."""
    users.assign_groups(filename)
