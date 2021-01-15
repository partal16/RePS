#!/usr/bin/pyhton
import psycopg2
from config import config

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE student (
            email VARCHAR(50) PRIMARY KEY,
            student_id SERIAL UNIQUE,
            first_name VARCHAR(30) NOT NULL,
            last_name VARCHAR(30) NOT NULL,
            password TEXT NOT NULL,
            faculty TEXT NOT NULL,
            s_question TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE problem (
            problem_id SERIAL PRIMARY KEY,
            title VARCHAR(20) NOT NULL,
            description VARCHAR(140) NOT NULL,
            privacy BOOLEAN NOT NULL,
            solution_r VARCHAR(140) NOT NULL,
            number_of_seen INT
        )
        """,
        """
        CREATE TABLE notifying (
            problem_id INTEGER PRIMARY KEY,
            student_id INTEGER,
            notification_date DATE NOT NULL DEFAULT CURRENT_DATE,
            FOREIGN KEY(problem_id)
                REFERENCES problem(problem_id),
            FOREIGN KEY(student_id)
                REFERENCES student(student_id)
        )
        """,
        """
        CREATE TABLE authorized_person (
            id_number SERIAL PRIMARY KEY,
            email VARCHAR(50) NOT NULL,
            first_name VARCHAR(30) NOT NULL,
            last_name VARCHAR(30) NOT NULL,
            password TEXT NOT NULL,
            s_question TEXT NOT NULL,
            code TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE ended (
            problem_id INTEGER PRIMARY KEY,
            id_number INTEGER,
            ended_date DATE,
            CONSTRAINT fk_problem
                FOREIGN KEY(problem_id)
                    REFERENCES problem(problem_id),
            CONSTRAINT fk_authorized
                FOREIGN KEY(id_number)
                    REFERENCES authorized_person(id_number)
        )
        """,
        """
        CREATE TABLE build (
            problem_id INTEGER PRIMARY KEY,
            name VARCHAR(150) NOT NULL,
            CONSTRAINT fk_problem
                FOREIGN KEY(problem_id)
                    REFERENCES problem(problem_id)
        )
        """)

    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    create_tables()
