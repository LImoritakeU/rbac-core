# Concept 
![RBACCORE](/home/shihhao/bluetech/rbac/rbac0-classic/rbac_core.png)

# ER Diagram
![RBAC ERDIAGRAM](/home/shihhao/bluetech/rbac/rbac0-classic/rbac_erdiagram.png)


## import rabc_core.sql to Database

```bash
$ export PGHOST="127.0.0.1"
$ export PGPORT=5432
$ export PGUSER=postgres
$ export PGPASSWORD=password
$ export PGDATABASE=rbac
$ psql -a -f sql/rbac_core_<db-type>.sql
```

## Generate SQLAlchemy's Model from Database

注意sqlacodegen不支援生成sequence，codegen雖然方便，但是還是需要修改，並且留意這是第三方外掛。

```bash
$ sqlacodegen postgres://postgres:password@127.0.0.1:5432/rbac > rbac/models_autogen.py
```


