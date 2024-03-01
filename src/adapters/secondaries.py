import csv
import sqlite3


def create_table():
    connection = sqlite3.connect("../../database.sqlite")  # Replace 'your_database.db' with your desired database name
    cursor = connection.cursor()

    # SQL statement to create the table
    create_table_sql = """
    CREATE TABLE quality_view (
         id INTEGER PRIMARY KEY,
         created TEXT,
         updated TEXT,
         dataset_id TEXT,
         title TEXT,
         publisher TEXT,
         published BOOLEAN,
         restricted BOOLEAN,
         description_score INTEGER,
         default_score INTEGER,
         dcat_score INTEGER,
         quality_score INTEGER
    );
    """

    cursor.execute(create_table_sql)

    connection.commit()
    connection.close()


def import_quality_report():
    connection = sqlite3.connect("database.sqlite")
    cursor = connection.cursor()

    with open("2024-02-29-datasets-quality-report.csv", "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # Convert 'published' and 'restricted' columns to boolean
            row["published"] = row["published"].lower() == "true"
            row["restricted"] = row["restricted"].lower() == "true"

            # Insert data into the database
            cursor.execute(
                """
                INSERT INTO quality_view (
                    created, updated, dataset_id, title, publisher, published,
                    restricted, description_score, default_score,
                    dcat_score, quality_score
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    row["created"],
                    row["updated"],
                    row["dataset_id"],
                    row["title"],
                    row["publisher"],
                    row["published"],
                    row["restricted"],
                    row["description_score"],
                    row["default_score"],
                    row["dcat_score"],
                    row["quality_score"],
                ),
            )

    connection.commit()
    connection.close()