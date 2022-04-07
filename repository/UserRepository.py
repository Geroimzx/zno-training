class UserRepository:
    def __init__(self, conn):
        self.conn = conn

    # Create query
    def addUser(self, user_id, user_name, first_name, last_name):
        with self.conn.cursor() as cursor:
            cursor.execute("INSERT INTO public.\"User\"(\"User_id\", \"UserName\", \"FirstName\", \"LastName\") VALUES(%s, %s, %s, %s)",
                           (user_id, user_name, first_name, last_name))

    # Read query
    def findAllUsers(self):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM public.\"User\"")
            return cursor.fetchall()

    def findUserById(self, user_id):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM public.\"User\" WHERE \"User_id\" = %s", (user_id,))
            return cursor.fetchall()

    def existsUserById(self, user_id):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT EXISTS(SELECT 1 FROM public.\"User\" WHERE \"User_id\" = %s)", (user_id,))
            return cursor.fetchone()[0]

    # Update query

    # Delete query


