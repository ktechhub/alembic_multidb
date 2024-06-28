<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/ktechhub/doctoc)*

<!---toc start-->

* [Managing Multiple Databases in FastAPI with SQLAlchemy and Alembic](#managing-multiple-databases-in-fastapi-with-sqlalchemy-and-alembic)
  * [Overview](#overview)
  * [Key Features](#key-features)
  * [Setup](#setup)
    * [Prerequisites](#prerequisites)
    * [Installation](#installation)
  * [Database Deployment](#database-deployment)
  * [Revisions](#revisions)
  * [Blog Post](#blog-post)
  * [API Endpoints](#api-endpoints)
  * [Configuration](#configuration)
  * [License](#license)

<!---toc end-->

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Managing Multiple Databases in FastAPI with SQLAlchemy and Alembic
In software development, efficiently managing databases across different environments—such as development, testing, QA, and production—can be challenging. This repository demonstrates how to streamline database schema migrations in a FastAPI project using SQLAlchemy for ORM and Alembic for database migrations.

## Overview
This project aims to simplify the management of multiple databases within a FastAPI application. By leveraging SQLAlchemy's powerful ORM capabilities and Alembic's migration framework, developers can seamlessly synchronize database schemas across various environments.

## Key Features
- Environment-specific Database Configuration: Configure database URLs and credentials using environment variables for each environment (dev, test, qa, prod).
- Alembic Integration: Integrate Alembic to manage database migrations efficiently, ensuring database schema evolution is handled seamlessly.
- Flexibility and Control: Perform migrations such as creating new revisions, upgrading to the latest schema version, and rolling back to previous migrations as needed.

## Setup
### Prerequisites
Before getting started, ensure you have the following installed:

- Python 3.7+
- FastAPI
- SQLAlchemy
- Alembic
- MySQL (or your preferred database)
- aiomysql library for asynchronous MySQL connections
- python-dotenv for managing environment variables

### Installation
1. Clone the repository:

   ```bash
   git clone https://github.com/ktechhub/alembic_multidb.git
   cd fastapi_todo_async
   ```

2. Create a virtual environment:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Copy and update .env file
   ```bash
   cp .env.example .env
   ```
5. Set up the database configuration in `app/core/config.py`.


## Database Deployment
Run container;
```sh
docker run --name mysqldb -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_USER=dev -e MYSQL_PASSWORD=root -e MYSQL_DATABASE=dev mysql:latest
```
Login into container
```sh
docker exec -it mysqldb /bin/bash

mysql -u root -p
Enter password: 
```
Create the databases;
```sh
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| dev                |
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.02 sec)

mysql> create database test;
Query OK, 1 row affected (0.03 sec)

mysql> create database qa;
Query OK, 1 row affected (0.02 sec)

mysql> create database prod;
Query OK, 1 row affected (0.00 sec)

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| dev                |
| information_schema |
| mysql              |
| performance_schema |
| prod               |
| qa                 |
| sys                |
| test               |
+--------------------+
8 rows in set (0.01 sec)
```

## Revisions
Run revisions with
```sh
python alembic_cli.py revision --db dev --message "initial"
```
Output;
```sh
{'dev', 'test', 'prod', 'qa'}
revision for dev: mysql+aiomysql://root:root@localhost:3306/dev
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'todos'
INFO  [alembic.autogenerate.compare] Detected added index ''ix_todos_created_at'' on '('created_at',)'
INFO  [alembic.autogenerate.compare] Detected added index ''ix_todos_id'' on '('id',)'
INFO  [alembic.autogenerate.compare] Detected added index ''ix_todos_title'' on '('title',)'
INFO  [alembic.autogenerate.compare] Detected added index ''ix_todos_updated_at'' on '('updated_at',)'
  Generating alembic_multidb/alembic/versions/dev/4039c07e6631_initial_on_2024_06_28_12_12_13_958182.py ...  done
venv➜  alembic_multidb git:(main) ✗ python alembic_cli.py revision --message "initial" 
{'qa', 'test', 'dev', 'prod'}
revision for qa: mysql+aiomysql://root:root@localhost:3306/qa
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'todos'
INFO  [alembic.autogenerate.compare] Detected added index ''ix_todos_created_at'' on '('created_at',)'
INFO  [alembic.autogenerate.compare] Detected added index ''ix_todos_id'' on '('id',)'
INFO  [alembic.autogenerate.compare] Detected added index ''ix_todos_title'' on '('title',)'
INFO  [alembic.autogenerate.compare] Detected added index ''ix_todos_updated_at'' on '('updated_at',)'
  Generating alembic_multidb/alembic/versions/qa/86652cb46652_initial_on_2024_06_28_12_12_31_618365.py ...  done
revision for test: mysql+aiomysql://root:root@localhost:3306/test
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'todos'
INFO  [alembic.autogenerate.compare] Detected added index ''ix_todos_created_at'' on '('created_at',)'
INFO  [alembic.autogenerate.compare] Detected added index ''ix_todos_id'' on '('id',)'
INFO  [alembic.autogenerate.compare] Detected added index ''ix_todos_title'' on '('title',)'
INFO  [alembic.autogenerate.compare] Detected added index ''ix_todos_updated_at'' on '('updated_at',)'
  Generating alembic_multidb/alembic/versions/test/2a039512c4a5_initial_on_2024_06_28_12_12_31_772744.py ...  done
revision for dev: mysql+aiomysql://root:root@localhost:3306/dev
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'todos'
INFO  [alembic.autogenerate.compare] Detected added index ''ix_todos_created_at'' on '('created_at',)'
INFO  [alembic.autogenerate.compare] Detected added index ''ix_todos_id'' on '('id',)'
INFO  [alembic.autogenerate.compare] Detected added index ''ix_todos_title'' on '('title',)'
INFO  [alembic.autogenerate.compare] Detected added index ''ix_todos_updated_at'' on '('updated_at',)'
  Generating alembic_multidb/alembic/versions/dev/98343cfb98c9_initial_on_2024_06_28_12_12_31_811355.py ...  done
revision for prod: mysql+aiomysql://root:root@localhost:3306/prod
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'todos'
INFO  [alembic.autogenerate.compare] Detected added index ''ix_todos_created_at'' on '('created_at',)'
INFO  [alembic.autogenerate.compare] Detected added index ''ix_todos_id'' on '('id',)'
INFO  [alembic.autogenerate.compare] Detected added index ''ix_todos_title'' on '('title',)'
INFO  [alembic.autogenerate.compare] Detected added index ''ix_todos_updated_at'' on '('updated_at',)'
  Generating alembic_multidb/alembic/versions/prod/3bf8810daf96_initial_on_2024_06_28_12_12_31_861122.py ...  done
```
Migrate;
```sh
venv➜  alembic_multidb git:(main) ✗ python alembic_cli.py upgrade                    
{'prod', 'dev', 'qa', 'test'}
upgrade for prod: mysql+aiomysql://root:root@localhost:3306/prod
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 3bf8810daf96, initial on 2024-06-28 12:12:31.861122
upgrade for dev: mysql+aiomysql://root:root@localhost:3306/dev
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 98343cfb98c9, initial on 2024-06-28 12:12:31.811355
upgrade for qa: mysql+aiomysql://root:root@localhost:3306/qa
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 86652cb46652, initial on 2024-06-28 12:12:31.618365
upgrade for test: mysql+aiomysql://root:root@localhost:3306/test
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 2a039512c4a5, initial on 2024-06-28 12:12:31.772744
```
Changes;
```sh
venv➜  alembic_multidb git:(main) ✗ python alembic_cli.py revision --message "added category"         
{'qa', 'test', 'dev', 'prod'}
revision for qa: mysql+aiomysql://root:root@localhost:3306/qa
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added column 'todos.category'
  Generating alembic/versions/qa/d9ee653f9916_added_category_on_2024_06_28_17_08_03_.py ...  done
revision for test: mysql+aiomysql://root:root@localhost:3306/test
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added column 'todos.category'
  Generating alembic/versions/test/f2d77a691374_added_category_on_2024_06_28_17_08_04_.py ...  done
revision for dev: mysql+aiomysql://root:root@localhost:3306/dev
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added column 'todos.category'
  Generating alembic/versions/dev/1c8765a319fb_added_category_on_2024_06_28_17_08_04_.py ...  done
revision for prod: mysql+aiomysql://root:root@localhost:3306/prod
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added column 'todos.category'
  Generating alembic/versions/prod/e464c7a6122c_added_category_on_2024_06_28_17_08_04_.py ...  done
venv➜  alembic_multidb git:(main) ✗ python alembic_cli.py upgrade             
{'dev', 'qa', 'test', 'prod'}
upgrade for dev: mysql+aiomysql://root:root@localhost:3306/dev
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 98343cfb98c9 -> 1c8765a319fb, added category on 2024-06-28 17:08:04.125174
upgrade for qa: mysql+aiomysql://root:root@localhost:3306/qa
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 86652cb46652 -> d9ee653f9916, added category on 2024-06-28 17:08:03.821398
upgrade for test: mysql+aiomysql://root:root@localhost:3306/test
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 2a039512c4a5 -> f2d77a691374, added category on 2024-06-28 17:08:04.094032
upgrade for prod: mysql+aiomysql://root:root@localhost:3306/prod
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 3bf8810daf96 -> e464c7a6122c, added category on 2024-06-28 17:08:04.152972
venv➜  alembic_multidb git:(main) ✗ python alembic_cli.py downgrade
{'test', 'prod', 'qa', 'dev'}
Error: Missing revision for downgrade.
venv➜  alembic_multidb git:(main) ✗ python alembic_cli.py downgrade --db test --revision f2d77a691374
{'prod', 'qa', 'test', 'dev'}
downgrade for test: mysql+aiomysql://root:root@localhost:3306/test
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
venv➜  alembic_multidb git:(main) ✗ python alembic_cli.py downgrade --db test --revision 2a039512c4a5            
{'test', 'dev', 'prod', 'qa'}
downgrade for test: mysql+aiomysql://root:root@localhost:3306/test
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running downgrade f2d77a691374 -> 2a039512c4a5, added category on 2024-06-28 17:08:04.094032
venv➜  alembic_multidb git:(main) ✗ python alembic_cli.py upgrade --db test --revision 2a039512c4a5
{'test', 'qa', 'dev', 'prod'}
upgrade for test: mysql+aiomysql://root:root@localhost:3306/test
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 2a039512c4a5 -> f2d77a691374, added category on 2024-06-28 17:08:04.094032
```

## Blog Post
[https://www.ktechhub.com/tutorials/effortlessly-manage-multiple-databases-in-fastapi-with-sqlalchemy-and-alembic](https://www.ktechhub.com/tutorials/effortlessly-manage-multiple-databases-in-fastapi-with-sqlalchemy-and-alembic)


Run the FastAPI application:

   ```bash
   uvicorn app.main:app --reload
   ```

Visit `http://localhost:8000/docs` for Swagger UI or `http://localhost:8000/redoc` for ReDoc.

## API Endpoints

- **POST `/todos/`**: Create a new TODO item.
- **GET `/todos/`**: Get all TODO items.
- **GET `/todos/{id}/`**: Get a TODO item by ID.
- **PUT `/todos/{id}/`**: Update a TODO item by ID.
- **DELETE `/todos/{id}/`**: Delete a TODO item by ID.

## Configuration

- Modify `app/core/config.py` to configure database settings (`DATABASE_URL`, etc.).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.