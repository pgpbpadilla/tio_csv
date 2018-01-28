class User:
    def __init__(self, ucm_account=None, user_id=None):
        self.ucm_account = ucm_account
        self.id = user_id


def load_user_by_group(filename):
    with open(filename) as f:
        next(f) # skip headers
        for line in f:
            row_fields = [field.strip() for field in line.split(',')]
            group_id = row_fields[0]
            user_id = row_fields[1]
            yield group_id, user_id


def load_users(filename):
    with open(filename) as f:
        next(f) # skip headers
        for line in f:
            row_fields = [field.strip() for field in line.split(',')]
            ucm_account = row_fields[0]
            user_id = row_fields[1]
            yield User(ucm_account, user_id)
