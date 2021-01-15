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

    def add_problem(self, problem, build, email):
        """ insert a new problem into the problem table"""
        sql = """INSERT INTO problem(title, description, privacy, solution_r, number_of_seen)
                 VALUES(%s, %s, %s, %s, %s) RETURNING problem_id; """

        sql2_1 = """INSERT INTO notifying(problem_id, student_id)
                    VALUES(%s, %s);"""
        sql3 = """INSERT INTO build(problem_id, name)
                  VALUES(%s, %s); """
        sql4 = """SELECT student_id FROM student WHERE email = %s;"""

        conn = None
        p_id = None
        s_id = None
        try:
            params = self.config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (problem.title, problem.description,
                              problem.privacy, problem.solution_r, problem.n_seen,))
            p_id = cur.fetchone()[0]
            cur.execute(sql4, (email,))
            s_id = cur.fetchone()[0]
            cur.execute(sql2_1, (p_id, s_id,))
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
        sql = """SELECT title, description, privacy, solution_r, number_of_seen 
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
            title, description, privacy, solution_r, n_seen = cur.fetchone()
            s_problem = Problem(title, description, privacy,
                                solution_r, n_seen=n_seen)
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return s_problem

    def cancel_problem(self, problem_key):
        sql = """DELETE FROM ended WHERE problem_id = %s;"""
        conn = None
        try:
            params = self.config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (problem_key,))
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def finish_problem(self, problem_key):
        sql = """UPDATE ended SET ended_date = CURRENT_DATE
                 WHERE problem_id = %s;"""
        conn = None
        try:
            params = self.config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (problem_key,))
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    
    def get_problems(self):
        sql = """SELECT problem_id, title, description, privacy, solution_r, number_of_seen 
                 FROM problem ORDER BY problem_id;"""
        conn = None
        problems = []
        try:
            params = self.config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            for problem_key, title, desc, pri, sol, n_s in rows:
                problems.append((problem_key, Problem(title, desc, pri, sol, n_seen=n_s)))
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return problems

    def get_user_problems(self, email, check):
        if check:
            sql = """SELECT student_id FROM student WHERE email = %s;"""
            sql2 = """SELECT problem_id FROM notifying WHERE student_id = %s;"""

        else:
            sql = """SELECT id_number FROM authorized_person WHERE email = %s;"""
            sql2 = """SELECT problem_id FROM ended 
                      WHERE id_number = %s AND ended_date is null;"""

        sql3 = """SELECT problem_id, title, description, privacy, solution_r, number_of_seen
                  FROM problem WHERE problem_id = %s;"""
        conn = None
        u_id = None
        p_ids = None
        problems = []
        try:
            params = self.config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (email,))
            u_id = cur.fetchone()
            cur.execute(sql2, (u_id,))
            p_ids = cur.fetchall()

            for p_id in p_ids:
                cur.execute(sql3, (p_id,))
                problem = cur.fetchone()
                problems.append((problem[0], Problem(problem[1], problem[2],
                                                     problem[3], problem[4],
                                                     n_seen=problem[5])))
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return problems

    def get_not_started_problems(self):
        sql = """SELECT problem_id FROM ended"""
        sql2 = """SELECT problem_id, title, description, privacy, solution_r, number_of_seen
                  FROM problem WHERE problem_id = %s"""
        sql3 = """SELECT problem_id FROM problem;"""
        
        conn = None
        p_ids = None
        np_ids = None
        problems = []
        try:
            params = self.config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql)
            p_ids = cur.fetchall()
            cur.execute(sql3)
            np_ids = cur.fetchall()
            for np_id in np_ids:
                if np_id not in p_ids:
                    cur.execute(sql2, (np_id,))
                    problem = cur.fetchone()
                    problems.append((problem[0], Problem(problem[1], problem[2],
                                                         problem[3], problem[4],
                                                         n_seen=problem[5])))
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return problems


    def add_student(self, student):
        sql = """SELECT student_id FROM student WHERE email = %s;"""
        sql2 = """INSERT INTO student(email, first_name, last_name, password, 
                  faculty, s_question)
                  VALUES(%s, %s, %s, %s, %s, %s) RETURNING student_id;"""
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
                                   student.last_name, student.password,
                                   student.faculty, student.s_question,))
                s_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def get_student(self, student_email):
        sql = """SELECT student_id, email, password, first_name, last_name, faculty, s_question 
                 FROM student WHERE email = %s;"""
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
        sql2 = """INSERT INTO authorized_person(email, first_name, last_name, password,
                  s_question, code)
                  VALUES(%s, %s, %s, %s, %s, %s) RETURNING id_number;"""
        conn = None
        a_id = None
        try:
            params = self.config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (authorized.email,))
            a_id = cur.fetchone()
            if a_id is None:
                cur.execute(sql2, (authorized.email, authorized.f_name,
                                   authorized.l_name, authorized.passw,
                                   authorized.s_question, authorized.code))
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
        sql = """SELECT id_number, email, password, first_name, last_name, s_question
                 FROM authorized_person WHERE email = %s;"""
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

    def select_problem(self, problem_key, email):
        sql = """INSERT INTO ended(problem_id, id_number)
                 VALUES(%s, %s);"""
        sql2 = """SELECT id_number FROM authorized_person WHERE email = %s;"""
        conn = None
        a_id = None
        try:
            params = self.config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql2, (email,))
            a_id = cur.fetchone()[0]
            cur.execute(sql, (problem_key, a_id,))
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def change_password(self, email, n_password, is_student):
        if is_student:
            sql = """UPDATE student SET password = %s WHERE email = %s;"""
        else:
            sql = """UPDATE authorized_person SET password = %s WHERE email = %s;"""

        conn = None
        try:
            params = self.config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (n_password, email,))
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
