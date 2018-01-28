from invoke import task
from cli_wrappers import users


cli_image_name = 'tio_cli'


@task
def build(ctx):
    """Builds Docker image for a fake CLI"""
    ctx.run('docker build -t {} .'.format(cli_image_name))


def build_docker_cmd(cli_cmd):
    base_docker_cmd = 'docker run -i --rm {}'.format(cli_image_name)
    return '{} {}'.format(base_docker_cmd, cli_cmd)


@task(help={
    'filename': 'The input file to read users from'
})
def upsert(ctx, filename):
    """Insert or Create the users in the specified file."""
    list_cmd = build_docker_cmd("cli list users juan johndoe")
    list_users_result = ctx.run(list_cmd, echo=True)

    users_to_insert = users.load_users(filename)

    for user in users_to_insert:
        if user.id in list_users_result.stdout:
            print('User: {} exists'.format(user.id))
        else:
            print('User: {} not found, inserting'.format(user.id))
            insert_cmd = build_docker_cmd('cli create user {}'.format(user.id))
            insert_result = ctx.run(insert_cmd, echo=True)
            print('User: {} created'.format(user.id))


@task(help={
    'filename': "The input file to read user-group associations"
})
def assign_group(ctx, filename):
    """Assigns the users to the specified groups."""
    users_by_group = users.load_user_by_group(filename)
    for group_id, user_id in users_by_group:
        assign_cmd = build_docker_cmd(
            'cli assign user={} group={}'.format(group_id, user_id)
        )
        ctx.run(assign_cmd, echo=True)
        print('Commdand successful')

