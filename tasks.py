from invoke import task
from cli_wrappers import users


cli_image_name = 'tio_cli'


def build_docker_cmd(cli_cmd):
    base_docker_cmd = 'docker run -i --rm {}'.format(cli_image_name)
    return '{} {}'.format(base_docker_cmd, cli_cmd)


@task(help={
    'filename': 'The input file to read users from'
})
def upsert(ctx, filename):
    """Insert or Create the users in the specified file."""
    list_cmd = build_docker_cmd("list users juan johndoe")
    list_users_result = ctx.run(list_cmd, echo=True)

    users_to_insert = users.load_users(filename)

    for user in users_to_insert:
        if user.id in list_users_result.stdout:
            print('User: {} exists'.format(user.id))
        else:
            print('User: {} not found, inserting'.format(user.id))
            insert_cmd = build_docker_cmd('create user {}'.format(user.id))
            insert_result = ctx.run(insert_cmd, echo=True)
            print('User: {} created'.format(user.id))


@task(help={
    'filename': "The input file to read user-group associations"
})
def assign_group(_, filename):
    """Assigns the users to the specified groups."""
    pass
