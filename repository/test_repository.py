class TestRepository:
    def __init__(self, conn):
        self.conn = conn

    # Create query

    # UserTest Create query
    def createUserTest(self, user_test_id, user_id):
        with self.conn.cursor() as cursor:
            cursor.execute("INSERT INTO public.\"UserTest\"(\"UserTest_id\", \"User_id\") VALUES(%s, %s)",
                           (user_test_id, user_id))

    def createUserAnswer(self, user_answer_id, user_test_id, question_id, answer):
        with self.conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO public.\"UserAnswer\"(\"UserAnswer_id\", \"Question_id\", \"UserTest_id\", \"Answer\") VALUES(%s, %s, %s, %s)",
                (user_answer_id, user_test_id, question_id, answer))

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
            cursor.execute("SELECT * FROM public.\"Year\" WHERE \"Subject_id\" = %s ORDER BY \"Year\" ASC",
                           (subject_id,))
            return cursor.fetchall()

    def existsYearSubjectId(self, subject_id):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT EXISTS(SELECT \"Year\" FROM public.\"Year\" WHERE \"Subject_id\" = %s)",
                           (subject_id,))
            return cursor.fetchone()[0]

    # Test Read query
    def findAllTestByYearId(self, year_id):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM public.\"Test\" WHERE \"Year_id\" = %s", (year_id,))
            return cursor.fetchall()

    def findAllTestBySubjectIdAndYear(self, subject_id, year):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT \"Year_id\" FROM public.\"Year\" WHERE \"Subject_id\" = %s AND \"Year\" = %s",
                           (subject_id, year))
            year_id = cursor.fetchall()[0][0]
            cursor.execute("SELECT * FROM public.\"Test\" WHERE \"Year_id\" = %s", (year_id,))
            return cursor.fetchall()

    # Question Read query
    def findAllQuestionByTestId(self, test_id):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM public.\"Question\" WHERE \"Test_id\" = %s ORDER BY \"Question_number\"",
                           (test_id,))
            return cursor.fetchall()

    def findQuestionByTestIdAndQuestionNumber(self, test_id, question_number):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM public.\"Question\" WHERE \"Test_id\" = %s AND \"Question_number\" = %s "
                           "ORDER BY \"Question_number\"",
                           (test_id, question_number,))
            return cursor.fetchall()

    # Answer Read query
    def findAllAnswerByQuestionId(self, question_number):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM public.\"Answer\" WHERE \"Question_number\" = %s", (question_number,))
            return cursor.fetchall()

    # UserAnswer Read query TODO: !!????????
    def findAllUserAnswerByUserTestId(self, user_test_id):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM public.\"UserAnswer\" WHERE \"UserTest_id\" = %s", (user_test_id,))
            return cursor.fetchall()

    def findAllUserAnswerByUserTestIdAndQuestionId(self, user_test_id, question_id):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM public.\"UserAnswer\" WHERE \"UserTest_id\" = %s AND \"Question_id\" = %s",
                           (user_test_id, question_id,))
            return cursor.fetchall()

    # TODO: test this
    def findAllUserAnswerByUserTestIdWithQuestion(self, user_test_id):
        with self.conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM public.\"UserAnswer\" a WHERE \"UserTest_id\" = %s LEFT JOIN public.\"Question\" q ON a.\"Question_id\" = q.\"Question_id\"",
                (user_test_id,))
            return cursor.fetchall()

    # Update query

    # UserTest Update query
    def updateUserTestScore(self, user_test_id, score):
        with self.conn.cursor() as cursor:
            cursor.execute("UPDATE public.\"UserTest\" SET \"UserTest_id\" = %s, \"Score\" = %s",
                           (user_test_id, score))

    def updateUserTestStarted(self, user_test_id, date_started):
        with self.conn.cursor() as cursor:
            cursor.execute("UPDATE public.\"UserTest\" SET \"Test_started\" = %s WHERE \"UserTest_id\" = %s",
                           (date_started, user_test_id))

    def updateUserTestFinished(self, user_test_id, date_finished):
        with self.conn.cursor() as cursor:
            cursor.execute("UPDATE public.\"UserTest\" SET \"Test_finished\" = %s WHERE \"UserTest_id\" = %s",
                           (date_finished, user_test_id))

    def updateUserAnswer(self, user_answer_id, answer):
        with self.conn.cursor() as cursor:
            cursor.execute("UPDATE public.\"UserAnswer\" SET \"Answer\" = %s WHERE \"UserAnswer_id\" = %s",
                           (answer, user_answer_id))
    # Delete query
