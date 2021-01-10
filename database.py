from problem import Problem
from student import Student
from authorized_person import AuthorizedPerson
from ended import Ended
from notifying import Notifying
from build import Build

import psycopg2
from configparser import ConfigParser

class Database:
    def __init__(self, dbfile):
        self.dbfile = dbfile

    def config(self, section='postgresql'):
        parser = ConfigParser()
        parser.read(self.dbfile)
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Selection {0} not found in the {1} file'.format(section, self.dbfile))
        return db

    def add_problem(self, problem, build):
        """ insert a new problem into the problem table"""
        sql = """INSERT INTO problem(title, description, number_of_seen)
                 VALUES(%s, %s, %s) RETURNING problem_id; """

        sql2_1 = """INSERT INTO notifying(problem_id, student_id)
                    VALUES(%s, %s);"""
        sql3 = """INSERT INTO build(problem_id, name)
                  VALUES(%s, %s); """

        conn = None
        p_id = None
        s_id = None
        try:
            params = self.config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (problem.title, problem.description, problem.n_seen,))
            p_id = cur.fetchone()[0]
            cur.execute(sql2_1, (p_id, 5,))
            cur.execute(sql3, (p_id, build.b_name,))
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return p_id

    
    def update_problem(self, problem_key, problem):
        sql = """UPDATE problem SET title = %s, description = %s WHERE problem_id = %s;"""
        conn = None
        try:
            params = self.config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (problem.title, problem.description, problem_key,))
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()


    def delete_problem(self, problem_key):
        sql = """DELETE FROM problem WHERE problem_id = %s;"""
        sql2 = """DELETE FROM build WHERE problem_id = %s;"""
        sql3 = """DELETE FROM notifying WHERE problem_id = %s;"""
        sql4 = """DELETE FROM ended WHERE problem_id = %s;"""
        conn = None
        try:
            params = self.config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql2, (problem_key,))
            cur.execute(sql3, (problem_key,))
            cur.execute(sql4, (problem_key,))
            cur.execute(sql, (problem_key,))
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()


    def get_problem(self, problem_key):
        sql = """SELECT title, description, number_of_seen 
                 FROM problem WHERE problem_id = %s;"""
        conn = None
        title = None
        description = None
        n_seen = None
        s_problem = None
        try:
            params = self.config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (problem_key,))
            title, description, n_seen = cur.fetchone()
            s_problem = Problem(title, description, n_seen=n_seen)
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return s_problem

    
    def get_problems(self):
        sql = """SELECT problem_id, title, description, number_of_seen 
                 FROM problem ORDER BY problem_id;"""
        conn = None
        problems = []
        try:
            params = self.config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            for problem_key, title, desc, n_s in rows:
                problems.append((problem_key, Problem(title, desc, n_seen=n_s)))
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return problems

    def add_student(self, student):
        sql = """SELECT student_id FROM student WHERE email = %s;"""
        sql2 = """INSERT INTO student(email, first_name, last_name, password)
                  VALUES(%s, %s, %s, %s) RETURNING student_id;"""
        conn = None
        s_id = None
        try:
            params = self.config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (student.email,))
            s_id = cur.fetchone()
            if s_id is None:
                cur.execute(sql2, (student.email, student.first_name,
                                   student.last_name, student.password,))
                s_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def get_student(self, student_email):
        sql = """SELECT student_id, email, password FROM student WHERE email = %s;"""
        conn = None
        s_id = None
        try:
            params = self.config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (student_email,))
            s_id = cur.fetchone()
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return s_id

    def add_authorized(self, authorized):
        sql = """SELECT id_number FROM authorized_person WHERE email = %s;"""
        sql2 = """INSERT INTO authorized_person(email, first_name, last_name, password)
                  VALUES(%s, %s, %s, %s) RETURNING id_number;"""
        conn = None
        a_id = None
        try:
            params = self.config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (authorized.email,))
            a_id = cur.fetchone()
            print(a_id)
            if a_id is None:
                cur.execute(sql2, (authorized.email, authorized.f_name,
                                   authorized.l_name, authorized.passw,))
                a_id = cur.fetchone()[0]
            print(a_id)
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def get_authorized(self, auth_email):
        sql = """SELECT id_number, email, password FROM authorized_person 
                 WHERE email = %s;"""
        conn = None
        a_id = None
        try:
            params = self.config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (auth_email, ))
            a_id = cur.fetchone()
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return a_id

