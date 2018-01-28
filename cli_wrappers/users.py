class User:
    def __init__(self, ucm_account=None, user_id=None):
        self.ucm_account = ucm_account
        self.id = user_id


class Group:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name


def upsert_from_file(ctx, filename):
    users = load_users(filename)
    for u in users:
        print('Inserting user: {}'.format(u.id))
    ctx.run('echo "This is a Bash/Shell command"', echo=True)


def load_user_groups(filename):
    with open(filename) as f:
        next(f) # skip headers
        for line in f:
            row_fields = [field.strip() for field in line.split(',')]
            user = User(user_id=row_fields[0])
            group = Group(id=row_fields[1])
            yield user, group


def assign_groups(ctx, filename):
    for user, group in load_user_groups(filename):
        print('Assigning user: {} to group: {}'.format(user.id, group.id))
    ctx.run('echo "This is another shell command"', echo=True)


def load_users(filename):
    users = []
    with open(filename) as f:
        next(f) # skip headers
        for line in f:
            row_fields = [field.strip() for field in line.split(',')]
            ucm_account = row_fields[0]
            user_id = row_fields[1]
            users.append(User(ucm_account, user_id))
    return users
