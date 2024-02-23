# PandaQ: SQL Interpreter in Python

PandaQ is a small SQL interpreter in Python that utilizes the antlr4 library. This interpreter can process some basic SQL queries on databases in .csv format and display them graphically using the Streamlit library.

## Setup

First, you'll need to install the antlr4 and Streamlit Python libraries. To do this, go to the src folder and follow these command:

```bash
make setup
```

## Execution

In order to execute the program go to the src folder and just type in the following command:

```bash
make run
```
This will output two URLs in the terminal, one local and the other not, which if opened in any browser will take us to the interface generated with the Streamlit library.

## Design Decisions

Firstly, this interpreter supports the following SQL utilities:
> Table selection\
> Field selection from tables\
> Calculated field selection\
> Order by function\
> Where function\
> Inner join function\
> Symbol table\
> Plots\
> Subqueries

Queries are performed one by one within the text box of the Streamlit application, and to execute them, you need to press the "Submit" button. Then the command will be executed, and a table with the data of the main query or its corresponding graph will be displayed on the screen. Subqueries will not be displayed on the screen.

When creating charts for a table or any query, only numerical data excluding identifiers will be represented, as it would not make sense otherwise.

All queries must end with a ";" to declare that the statement has ended.

In case of any syntax error, an error message will be printed to the terminal, indicating that there has been a problem. It will also indicate what the grammar expected and the parse tree it has been able to construct with your input to ease error tracking.

Strings of the queries don't go in quotes, that is:
> select * from countries where country_name <> "France";

Would be incorrect, but the following case would be correct:

> select * from countries where not country_name <> France;

Finally, the source code is commented to ease its reading and help understand wht's happening.

## Examples of queries

### Some examples testing the implemented functionalities could be:

Simple queries on tables:
> select * from employees;

> select first_name, last_name, salary from employees;

Query with calculated fields:
> select first_name, last_name, salary, salary * 1.5 as new_salary from employees;

Sorted queries:
> select * from employees order by last_name desc, first_name;

> select first_name, last_name, salary from employees order by salary;

Queries with where and subqueries:
> select first_name, last_name, salary from employees where salary > 7000;

> select first_name, last_name, salary from employees where department_id in (select * from departments where location_id = 1700);

Queries with inner join:
> select first_name, department_name from employees inner join departments on department_id = department_id;

> select first_name, last_name, job_title, department_name from employees inner join departments on department_id = department_id inner join jobs on job_id = job_id;

Use of the symbol table:
> hola := select first_name, last_name, salary from employees where salary > 7000;

> select first_name, last_name from hola;

Plots:
> hola := select first_name, last_name, salary, salary * 1.5 as new_salary from employees;

> plot hola;


## References

A continuació, les referències usades per aquest treball:

[ANTLR in Python](https://gebakx.github.io/Python3/compiladors.html#1)\
[Pandas docs](https://pandas.pydata.org/pandas-docs/stable/index.html)\
[Streamlit docs](https://docs.streamlit.io)\
[SQL tutorial](https://www.sqltutorial.org)