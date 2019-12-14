from django.db.migrations import CreateModel

class CreatePartitionedModel(CreateModel):
    def __init__(self, name, fields, partition_sql, **kwargs):
        self.partition_sql = partition_sql
        super().__init__(name, fields, **kwargs)

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        collector = type(schema_editor)(
            schema_editor.connection, collect_sql=True, atomic=False
        )
        with collector:
            super().database_forwards(
                app_label, collector, from_state, to_state
            )
        collected_sql = collector.collected_sql
        schema_editor.deferred_sql.extend(
            collector.deferred_sql
        )

        model = to_state.apps.get_model(app_label, self.name)
        create_table = 'CREATE TABLE %s' % schema_editor.quote_name(
            model._meta.db_table
        )
        for sql in collected_sql:
            if str(sql).startswith(create_table):
                sql = '%s PARTITION BY %s' % (sql.rstrip(';'), self.partition_sql)
            schema_editor.execute(sql)
