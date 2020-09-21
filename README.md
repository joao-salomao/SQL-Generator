# SQL Generator

SQL Generator is an SQL code generator from spreadsheet files
## Web
Access the website on [Heroku](https://sqlgenerator.herokuapp.com/).
## CLI
### Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies.

```bash
pip install -r requirements.txt 
```

### Usage
Currently the file formats allowed are: xlsx and csv.

If you are using files in the xlsx format, the spreadsheet named with the default name "Sheet1" will be used.

##### *All the examples showed bellow will be using a table called "users".

##### Allowed Operations: insert, update, delete.

Command:
```bash
 python3 sql_generator.py OPERATION TABLE_NAME FILE_PATH
```

###  Examples
#### Insert
The first row of the spreadsheet must contain the column names and the others the data. Ex:
![insert example](https://raw.githubusercontent.com/joao-salomao/SQL-Generator/master/sql_generator/static/images/insert_example.png)

Run:

```bash
 python3 sql_generator.py insert users users.xlsx
```

The result will be like this:
```sql
INSERT INTO users(name,idade,data) VALUES ('João',200,'2020-08-10 00:00:00'),
('Mariza',123,'2020-08-11 00:00:00'),('Valcir',200,'2020-08-12 00:00:00'),
('Lara',123,'2020-08-13 00:00:00');
```

#### Update
The first row of the spreadsheet must contain the column names, the last column of the first row must contain the WHERE clause and the other lines the data used for the update, the last column being the condition used in the WHERE clause. Ex:

![update example](https://raw.githubusercontent.com/joao-salomao/SQL-Generator/master/sql_generator/static/images/update_example.png)

Run:
```bash
 python3 sql_generator.py update users users.xlsx
```

The result will be like this:
```sql
UPDATE users SET name = 'João', likes = 200, data = '2020-08-10 00:00:00' WHERE id = 1;
UPDATE users SET name = 'Mariza', likes = 123, data = '2020-08-11 00:00:00' WHERE id = 2;
UPDATE users SET name = 'Valcir', likes = 200, data = '2020-08-12 00:00:00' WHERE id = 3;
UPDATE users SET name = 'Lara', likes = 123, data = '2020-08-13 00:00:00' WHERE id = 4;
```

#### Delete
The use for the delete operation is similar to that of update, the difference being that all the columns defined in the first row are used in the construction of the WHERE clause. Ex:

![delete example](https://raw.githubusercontent.com/joao-salomao/SQL-Generator/master/sql_generator/static/images/delete_example.png)

Run:

```bash
 python3 sql_generator.py delete users users.xlsx
```
The result will be like this:
```sql
DELETE FROM users WHERE id = 1 AND name = 'João' AND age = 21;
DELETE FROM users WHERE id = 2 AND name = 'Mariza' AND age = 41;
DELETE FROM users WHERE id = 3 AND name = 'Valcir' AND age = 53;
DELETE FROM users WHERE id = 4 AND name = 'Lara' AND age = 22;
```
