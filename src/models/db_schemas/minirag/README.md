## Run Alembic Migrations

### Configuration

```Shell
cp alembic.ini.exmaple alembic.ini
```

- Update the `alembic.ini` with your database credentials (`sqlalchemy.url`)

### (Optional) Create a new migration

```Shell
alembic revision --autogenerate -m "Add ..."
```

### Upgrade the database

```Shell
alembic upgrade head
```
