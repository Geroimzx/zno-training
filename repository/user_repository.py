class UserRepository:
    def __init__(self, conn):
        self.conn = conn

    # Create query
    def addUser(self, user_id, user_name, first_name, last_name, registered_date, last_time_online_date):
        with self.conn.cursor() as cursor:
            cursor.execute("INSERT INTO public.\"User\"(\"User_id\", \"UserName\", \"FirstName\", \"LastName\", \"RegisteredDate\") VALUES(%s, %s, %s, %s, %s)",
                           (user_id, user_name, first_name, last_name, registered_date))

    def updateUserTimeOnlineDate(self, user_id, last_time_online_date):
        with self.conn.cursor() as cursor:
            cursor.execute("UPDATE  public.\"User\" SET \"LastTimeOnlineDate\"=%s WHERE \"User_id\"=%s",
                           (last_time_online_date, user_id))

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


