# Walmart Advanced Software Engineering Job Simulation

**Platform:** Forage  
**Organization:** Walmart USA  
**Focus:** Data structures, software architecture, relational database design, and Python data processing  
**Project type:** Self-paced job simulation (not an internship or employment)

## Overview

This repository documents my work on the **Walmart USA Advanced Software Engineering Job Simulation**, completed through Forage. The simulation consists of four engineering exercises that cover algorithm design, extensible software architecture, normalized relational database modeling, and an ETL workflow for shipping data.

The work includes Java source code, UML and entity-relationship diagrams, and a Python script that consolidates shipping records into SQLite.

## Tasks and deliverables

### Task 1 — Advanced Data Structures

**Goal:** Implement a power-of-two max heap in Java for a priority queue.

- Built an array-backed max heap where the constructor's `childrenExponent` parameter determines the number of children per node (`2^childrenExponent`).
- Implemented `insert(int value)` and `popMax()` with sift-up and sift-down operations.
- Handled duplicates, negative integers, empty heaps, and very large exponent values.
- Ran a Java test harness successfully across **11 exponent settings**: `0, 1, 2, 3, 5, 10, 20, 30, 31, 62, 100`.

**Deliverable:** `Task1-Advanced-Data-Structures/PowerOfTwoMaxHeap.java`

### Task 2 — Software Architecture

**Goal:** Design a dynamically reconfigurable data processor using UML.

- Modeled `configure(ModeIdentifier, DatabaseIdentifier)` and `process(Datapoint)`.
- Separated processing behavior into **Dump**, **Passthrough**, and **Validate** modes.
- Designed database adapters for **Postgres**, **Redis**, and **Elastic** with abstract `connect`, `insert`, and `validate` operations.
- Applied the **Strategy** and **Adapter** patterns and registries to support extensibility and switching modes/databases.

**Deliverable:** `Task2-Software-Architecture/Walmart_Task2_Data_Processor_UML.pdf`

### Task 3 — Relational Database Design

**Goal:** Design a normalized database for Walmart's pet department.

- Created an ERD with **13 tables** to model pet food, toys, apparel, manufacturers, and animal compatibility.
- Modeled customers, transactions, and purchased products using transaction line items.
- Modeled store locations, shipments, shipment products, and quantities.
- Used primary/foreign keys and junction tables to represent one-to-many and many-to-many relationships.

**Deliverable:** `Task3-Relational-Database-Design/Walmart_Task3_Pet_Department_ERD.pdf`

### Task 4 — Data Munging

**Goal:** Consolidate three shipping CSV files into an SQLite database using Python.

- Read and transformed records from **three CSV datasets**.
- Loaded records from Spreadsheet 0 and combined Spreadsheets 1 and 2 by shipping identifier.
- Grouped repeated products within a shipment to calculate quantities and matched shipment routes.
- Inserted the transformed shipment-product records into SQLite while preserving the original database.

**Observed local run:**

```text
Read 110 records from shipping_data_0.csv
Grouped 110 rows from shipping_data_1.csv
Matched routes from 20 rows of shipping_data_2.csv
Inserted 154 shipment-product rows
Output database: shipment_database_populated.db
```

**Deliverable:** `Task4-Data-Munging/populate_shipping_database.py`

## Suggested repository structure

Organize the files in this repository as follows (the names below are a suggested layout):

```text
walmart-advanced-software-engineering/
├── README.md
├── Task1-Advanced-Data-Structures/
│   ├── PowerOfTwoMaxHeap.java
│   └── PowerOfTwoMaxHeapTest.java
├── Task2-Software-Architecture/
│   └── Walmart_Task2_Data_Processor_UML.pdf
├── Task3-Relational-Database-Design/
│   └── Walmart_Task3_Pet_Department_ERD.pdf
└── Task4-Data-Munging/
    ├── populate_shipping_database.py
    └── Walmart_Task4_Data_Munging_Script.pdf
```

The original Task 4 CSV datasets and starter SQLite database are available in the [Walmart Forage Task 4 starter repository](https://github.com/theforage/forage-walmart-task-4). They are not required in this solutions repository.

## Run the code

### Task 1: Java max heap

**Requirement:** JDK (Java 21 was used during local testing).

From the Task 1 folder, run:

```bash
javac PowerOfTwoMaxHeap.java PowerOfTwoMaxHeapTest.java
java PowerOfTwoMaxHeapTest
```

Expected final test output:

```text
All heap tests passed.
```

### Task 4: Python ETL and SQLite

**Requirement:** Python 3. The script uses standard-library modules, so no third-party packages are necessary.

1. Download or clone the [official Task 4 starter repository](https://github.com/theforage/forage-walmart-task-4).
2. Place `populate_shipping_database.py` in the starter repository's root directory, alongside its SQLite database and `data` folder.
3. Run:

```bash
python populate_shipping_database.py
```

The script creates `shipment_database_populated.db` and leaves the starter database unchanged.

## Skills and tools

- **Java:** array-backed heaps, priority queues, algorithmic edge cases, correctness testing
- **Software design:** UML, Strategy Pattern, Adapter Pattern, SOLID principles
- **Databases:** ERD design, relational modeling, normalization, primary and foreign keys
- **Python:** CSV processing, data aggregation, joining datasets, ETL workflows
- **SQLite:** database connections and inserts

## Key takeaways

The simulation reinforced the relationship between data-structure performance, maintainable software design, relational data integrity, and data pipelines. It also provided practice turning written business requirements into code and technical design artifacts.

## Disclaimer

This repository contains work completed as part of a **Walmart USA job simulation hosted by Forage**. It represents an educational simulation, **not employment, an internship, or a project commissioned by Walmart**.
