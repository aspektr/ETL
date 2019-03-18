# pysdtt - simple data transfer tool

is able to transfer data from any sources to postgresql

## Usage
* wright sql query and put it into query folder as .sql file
* fill the `config/config.yaml` up for a source db in the source_name section
* fill the `config/config.yaml` up for a sink db in the sink_name section
* run `python etl.py --from your_source_name --to your_sink_name --mode multi`
* check `logs/info.log` and `logs/errors.log`

## TODO
* add csv support
* add mongodb support
*   It might be more convinient use in config the following schema defining the types:

        int4:
            col1
            col2
            col3
        varchar(64):
            col1
            col2
            col3

* handle bug in multi mode, add error message when cursor_size is not specified


## Introduction
<ul>
<li>Prototype - base class</li>
    <ul>
        <li>Batch loading (based on pandas) uses together the following classes:</li>
            <ul>
            <li>Source class</li>
                <ol>
                    <li> can use all sources available for SQLAlchemy</li>
                    <li> usefull for small data</li>
                    <li> specify date_column field in the congif.yaml if result of query execution contains timestamp fields  </li>
                </ol>
            <li>Sink   class</li>
                <ol>
                <li> can use all sinks   available for SQLAlchemy</li>
                <li> usefull for small data</li>
                </ol>
            </ul>
            </ul>
            <ul>
        <li>Parallel loading (as for sink only postgres is available) uses together the following classes:</li>
            <ul>
                <li>Producer class</li>
                <li>Sink   class</li>
                </ul>
            </ul>
</ul>


### Config description

source_name:
  test_source2:
    type: postgresql+psycopg2
    host: 172.18.151.27
    port: 5432
    dbname: superset
    schema: upload
    user: superset
    psw: DEkde3467XDer4G
    file: query/test.sql
    receive mode: batch

source_name - section name, can't be changed
test_source - source pseudonym, used in the command prompt
type - type db, see also SQLAlchemy
file - file containig query to db
cursor_size - number of rows transmitted to insertion in one commitment (receive_mode = row_by_row or multiprocessing]


### Command prompt
mode:
* all_data, will be used pandas as backend, doesn't work when source is mongodb
* row_by_row,  will consume small batch from db cursor and load it into sink (specify cursor_size in the source_name section). This allows you to process unlimited or unknown amounts of data with a fixed amount of memory.
* multi, the same as row_by_row, but much faster

### Notice
UUID stands for Universal Unique Identifier defined by RFC 4122 and other
related standards. A UUID value is 128-bit quantity generated by an
algorithm that make it unique in the known universe using the same algorithm

Because of its uniqueness feature, you often found UUID in the distributed
systems because it guarantees a better uniqueness than the `SERIAL` data
type which generates only unique values within a single database.

PostgreSQL allows you store and compare UUID values but it does not
include functions for generating the UUID values in its core.
Instead, it relies on the third-party modules that provide specific
algorithms to generate UUIDs. For example the uuid-ossp module provides
some handy functions that implement standard algorithms for generating UUIDs.

To install the uuid-ossp module, you use the CREATE EXTENSION statement as follows:

`CREATE EXTENSION IF NOT EXISTS "uuid-ossp";`

The `IF NOT EXISTS` clause allows you to avoid re-installing the module.

It's important because there is uuid generator is being used.
If you don't have the opportunity to create extension you should
replace uuid_generate_v1() by serial

### Notice

`There are two JSON data types: json and jsonb. They accept almost
identical sets of values as input. The major practical difference is one
of efficiency. The json data type stores an exact copy of the input text,
which processing functions must reparse on each execution
while jsonb data is stored in a decomposed binary format that makes it slightly
slower to input due to added conversion overhead, but significantly faster
to process, since no reparsing is needed. jsonb also supports indexing,
which can be a significant advantage.

Because the json type stores an exact copy of the input text,
it will preserve semantically-insignificant white space between tokens,
as well as the order of keys within JSON objects.
Also, if a JSON object within the value contains the same key more than
once, all the key/value pairs are kept.
(The processing functions consider the last value as the operative one.)
By contrast, jsonb does not preserve white space,
does not preserve the order of object keys,
and does not keep duplicate object keys.
If duplicate keys are specified in the input, only the last value is kept.`

### Challenges with writing Custom ETL scripts to move data from MongoDB to PostgreSQL:
   1. Schema detection cannot be done up front
   Unlike a relational database, a MongoDB collection doesn’t have a predefined schema.
   Hence, it is impossible to look at a collection and create a compatible table in PostgreSQL upfront.

   2. Different documents in a single collection can have a different set of fields
   A document in a collection in MongoDB can have a different set of fields. 

     {

        "name": "John Doe",

        "age": 32,

        "gender": "Male"

    }

    {

        "first_name": "John",

        "last_name": "Doe",

        "age": 32,

        "gender": "Male"

    }

   3. Different documents in a single collection can have incompatible field data types
   Hence, the schema of the collection cannot be determined by reading one or a few documents.

   Two documents in a single MongoDB collection can have fields with values of different types.

    {

        "name": "John Doe",

        "age": 32,

        "gender": "Male"

        "mobile": "(424) 226-6998"

    }
   and

    {
        "name": "John Doe",

        "age": 32,

        "gender": "Male",

        "mobile": 4242266998

    }
   The field mobile is a string and a number in the above documents respectively.
   It is a completely valid state in MongoDB. In PostgreSQL, however, both these values
   either will have to be converted to a string or a number before being persisted.

   4. New fields can be added to a document at any point in time
   It is possible to add columns to a document in MongoDB by running a simple update
   to the document. In PostgreSQL, however, the process is harder as you have to construct
   and run ALTER statements each time a new field is detected.

   5. Character lengths of String columns
   MongoDB doesn’t put a limit on the length of the string columns.
   It has a 16MB limit on the size of the entire document.
   However, in PostgreSQL, it is a common practice to restrict string columns
   to a certain maximum length for better space utilization.
   Hence, each time you encounter a longer value than expected,
   you will have to resize the column.

   6. A document can have nested objects and arrays with a dynamic structure
   The most complex of MongoDB ETL problems is handling nested objects and arrays.

    {

        "name": "John Doe",

        "age": 32,

        "gender": "Male",

        "address": {

            "street": "1390 Market St",

            "city": "San Francisco",

            "state": "CA"

        },

        "groups": ["Sports", "Technology"]

    }
   MongoDB allows nesting objects and arrays to a number of levels.
   In a complex real-life scenario is may become a nightmare trying to flatten
   such documents into rows for a PostgreSQL table.

   7. Data Type incompatibility between MongoDB and PostgreSQL
   Not all data types of MongoDB are compatible with PostgreSQL.
   ObjectId, Regular Expression, Javascript are not supported by PostgreSQL.



