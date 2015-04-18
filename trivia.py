import random
import uuid
import math

QUESTIONS_PER_GAME = 5


class Answer:

    def __init__(self, answer, id):
        self.answer = answer
        self.id = id
        self.correct_answer = False

    def flag_as_correct_answer(self):
        self.correct_answer = True

    def __str__(self):
        return self.answer


class Question:
    delimiter = '~'

    def __init__(self, question_string):
        self.parse_question(question_string)

    def parse_question(self, question_string):
        q = question_string.split(Question.delimiter)
        self.question = q[0]
        self.answers = [Answer(ans, uuid.uuid4()) for ans in q[1:-1]]
        correct_answer_index = int(q[-1]) - 1
        self.correct_answer = self.answers[correct_answer_index]

    def number_of_answers(self):
        return len(self.answers)

    def __str__(self):
        random.shuffle(self.answers)
        indexed_answers = zip(range(self.number_of_answers()), self.answers)
        return self.question + '\n' + '\n'.join("\t{}) {}".format(i + 1, a)
                                                for (i, a) in indexed_answers)


class Trivia:

    def __init__(self):
        self.questions = []

    def check_user_answer(self, user_answer, question):
        if question.answers[user_answer - 1] is question.correct_answer:
            print("Correct answer!")
            return True
        else:
            print("Incorrect answer! The correct answer is {}"
                  .format(question.correct_answer))
            return False

    def is_valid_answer(answer, question):
        return 1 <= answer <= len(question.answers)

    def parse_question_file(self, filename):
        with open(filename, 'r', encoding="utf8") as f:
            for line in f:
                self.questions.append(Question(line))

    def run(self):
        self.parse_question_file("ConcertTriviaUTF8.dat")
        number_of_questions = len(self.questions)

        if number_of_questions < QUESTIONS_PER_GAME:
            raise ValueError('Not enough questions in file! requested: {}, '
                             'available: {}'.format(QUESTIONS_PER_GAME,
                                                    number_of_questions))
        random_question_set = random.sample(self.questions, QUESTIONS_PER_GAME)
        correct_answers = 0
        for q, idx in zip(random_question_set, range(QUESTIONS_PER_GAME)):
            print("{}. {}".format(idx + 1, q))
            user_answer = input('Enter the number of the correct answer: ')
            while not self.is_valid_answer(int(user_answer), q):
                print('Invalid answer, try again!')
                user_answer = input('Enter the number of the correct answer: ')
            if self.check_user_answer(int(user_answer), q):
                correct_answers += 1
            print()
        final_score = math.ceil(correct_answers / QUESTIONS_PER_GAME * 100)
        print("""Game over! Summary:
                 Total questions: {}
                 Correct answers: {}
                 Score: {}""".format(QUESTIONS_PER_GAME, correct_answers,
                                     final_score))


def main():
    Trivia().run()

if __name__ == "__main__":
    main()
