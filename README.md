GitData
====
Data Wrangling for Everyone.

GitData is an easy to use, fast, scalable, distributed data extraction system
with a rich set of commands that provide ways to gather, manage and query data in
an unusually rich variety of ways.

## Concepts
GitData stores data as facts.

Facts are triples of the form (subject, predicate, object) where subject is
typically an entity, predicate is typically an attribute of that entity and
object is the value of the attribute.  In the case where the attribute represents
a relationship between entities, the object is another entity.

## Commands
GitData shares many of the commands and concepts you are familiar with from
the git source code revision control system with some important differences
which make it ideal for working with data.

#### Data repostitories
Data repositories are where GitData stores the data it is managing.  That data
is typically pulled in from other data sources and is stored in the data
repository for quick access.

<pre>
init   - initialize a new data repository
status - show repository status
</pre>
