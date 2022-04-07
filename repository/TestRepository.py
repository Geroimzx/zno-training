class TestRepository:
    def __init__(self, conn):
        self.conn = conn

    # Create query
    def addUser(self, user_id, user_name, first_name, last_name):
        with self.conn.cursor() as cursor:
            cursor.execute("INSERT INTO public.\"User\"(\"User_id\", \"UserName\", \"FirstName\", \"LastName\") VALUES(%s, %s, %s, %s)",
                           (user_id, user_name, first_name, last_name))

    # Read query
    def findAllSubject(self):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM public.\"Subject\"")
            return cursor.fetchall()

    def findSubjectById(self, subject_id):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM public.\"Subject\" WHERE \"Subject_id\" = %s", (subject_id,))
            return cursor.fetchall()

    def findAllYear(self):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM public.\"Subject\"")
            return cursor.fetchall()

    def findAllYearBySubjectId(self, subject_id):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM public.\"Year\" WHERE \"Subject_id\" = %s", (subject_id,))
            return cursor.fetchall()

    def existsYearSubjectId(self, subject_id):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT EXISTS(SELECT \"Year\" FROM public.\"Year\" WHERE \"Subject_id\" = %s)", (subject_id,))
            return cursor.fetchone()[0]

    # Update query

    # Delete query


