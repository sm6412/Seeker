NUM_LOGICAL_SHARDS = 32
NUM_PHYSICAL_SHARDS = 2

LOGICAL_TO_PHYSICAL = (
    'db1', 'db2', 'db1', 'db2', 'db1', 'db2', 'db1', 'db2',
    'db1', 'db2', 'db1', 'db2', 'db1', 'db2', 'db1', 'db2',
    'db1', 'db2', 'db1', 'db2', 'db1', 'db2', 'db1', 'db2',
    'db1', 'db2', 'db1', 'db2', 'db1', 'db2', 'db1', 'db2',
)


def logical_to_physical(logical):
    if logical >= NUM_LOGICAL_SHARDS or logical < 0:
        raise Exception("shard out of bounds %d" % logical)
    return LOGICAL_TO_PHYSICAL[logical]


def logical_shard_for_user(user_id):
    return user_id % NUM_LOGICAL_SHARDS


class UserRouter(object):
    auth_labels = {'auth', 'contenttypes'}

    def _database_of(self, user_id):
        return logical_to_physical(logical_shard_for_user(user_id))

    def _db_for_read_write(self, model, **hints):
        if model._meta.app_label == 'auth':
            return 'auth_db'
        if model._meta.app_label == 'sessions':
            return 'auth_db'
        db = None
        try:
            instance = hints['instance']
            db = self._database_of(instance.user_id)
        except AttributeError:
            db = self._database_of(instance.id)
        except KeyError:
            try:
                db = self._database_of(int(hints['user_id']))
            except KeyError:
                print("No instance in hints")
        print("Returning", db)
        return db

    def db_for_read(self, model, **hints):
        return self._db_for_read_write(model, **hints)

    def db_for_write(self, model, **hints):
        return self._db_for_read_write(model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.auth_labels and
            obj2._meta.app_label not in self.auth_labels
        ) or (
            obj2._meta.app_label in self.auth_labels and
            obj1._meta.app_label not in self.auth_labels
        ):
            print ("Rejecting cross-table relationship", obj1._meta.app_label, obj2._meta.app_label)
            return False
        return True

    def allow_migrate(self, db, app_label, model=None, **hints):
        return True
