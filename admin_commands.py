import json

from db.AdminDbQuery import AdminDbQuery
from settings import DB_NAME


queries = AdminDbQuery(DB_NAME)

clb_names = {
    "table": "table_",
    "add": "add_",
    "update": "update_",
    "remove": "remove_",
}

add_text = {
    "tours": {
        "id": 0,
        "name": 'TEXT',
        "table": "tours",
        "command": "add"
    },
}

json_add_text = []
for item in add_text.values():
    json_add_text.append(json.dumps(item))


tables = queries.get_all_tables()
tables_names = []
add_to_table = []
update_table = []
remove_from_table = []
for table in tables:
    tables_names.append(table.get("name"))
    add_to_table.append(f"{clb_names.get('add')}{table['name']}")
    update_table.append(f"{clb_names.get('update')}{table['name']}")
    remove_from_table.append(f"{clb_names.get('remove')}{table['name']}")
