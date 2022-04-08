class TestRepository:
    def __init__(self, conn):
        self.conn = conn

    # Create query

    # Read query

    # Subject Read query
    def findAllSubject(self):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM public.\"Subject\"")
            return cursor.fetchall()

    def findSubjectById(self, subject_id):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM public.\"Subject\" WHERE \"Subject_id\" = %s", (subject_id,))
            return cursor.fetchall()

    # Year Read query
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

    # Test Read query
    def findAllTestByYearId(self, year_id):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM public.\"Test\" WHERE \"Year_id\" = %s", (year_id,))
            return cursor.fetchall()

    # Question Read query
    def findAllQuestionByTestId(self, test_id):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM public.\"Question\" WHERE \"Test_id\" = %s \"ORDER BY QuestionNumber\"", (test_id,))
            return cursor.fetchall()

    def findQuestionByTestIdAndQuestionNumber(self, test_id, question_number):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM public.\"Question\" WHERE \"Test_id\" = %s AND \"Question_number\" = %s ORDER BY \"Question_number\"", (test_id, question_number,))
            return cursor.fetchall()

    # Answer Read query
    def findAllAnswerByQuestionId(self, question_number):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM public.\"Answer\" WHERE \"Question_number\" = %s", (question_number,))
            return cursor.fetchall()

    # UserAnswer Read query TODO: test this
    def findAllUserAnswerByUserTestId(self, user_test_id):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM public.\"UserAnswer\" a WHERE \"UserTest_id\" = %s LEFT JOIN public.\"Question\" q ON a.\"Question_id\" = q.\"Question_id\"", (user_test_id,))
            return cursor.fetchall()

    # Update query

    # Delete query


