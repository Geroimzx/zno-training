class SubjectRepository:
    def __init__(self, conn):
        self.conn = conn

    def addSubject(self, name):
        with self.conn.cusror() as cursor:
            cursor.execute(F"INSERT INTO public.\"Subject\"(\"Name\") VALUES ('{name}')")
