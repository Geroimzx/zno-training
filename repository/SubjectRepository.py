class SubjectRepository:
    def __init__(self, conn):
        self.conn = conn

    def addSubject(self, name):
        with self.conn.cursor() as cursor:
            cursor.execute(F"INSERT INTO public.\"Subject\"(\"Name\") VALUES ('{name}')")

    def findAllSubjects(self):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM public.\"Subject\"")
            return cursor.fetchall()

    def findIdSubject(self, name):
        with self.conn.cursor() as cursor:
            cursor.execute(F"SELECT \"Subject_id\" FROM public.\"Subject\" WHERE public.\"Subject\".\"Name\"='{name}'")
            return cursor.fetchall()[0][0]
            