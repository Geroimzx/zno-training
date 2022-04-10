class SubjectRepository:
    def __init__(self, conn):
        self.conn = conn

    def addSubject(self, name):
        with self.conn.cusror() as cursor:
            cursor.execute(F"INSERT INTO public.\"Subject\"(\"Name\") VALUES ('{name}')")

    def selectAllSubjects(self):
        with self.conn.cusror() as cursor:
            cursor.excute("SELECT * FROM public.\"Subject\"")
            return cursor.fetchall()
            