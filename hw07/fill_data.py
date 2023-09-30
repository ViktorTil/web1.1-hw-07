from datetime import date, datetime, timedelta
from random import randint, choice
from faker import Faker
from sqlalchemy import select

from src.models import Teacher, Student, Discipline, Grade, Group
from src.db import session

DISCIPLINES = [
    "Высшая математика",
    "История Украины",
    "Философия",
    "Английский язык",
    "Программирование",
    "Физкультура",
    "Дифференциальная геометрия",
    "ЕНПД"
]

GROUPS = ["МТБ-08", "ДГБ-099", "ТПК404"]
NUMBER_TEACHERS = 5
NUMBER_STUDENTS = 50
NUMBER_GRADES_DISCIPLINE = 6
min_grade = 1
max_grade = 12
start_date = datetime.strptime("2022-09-01", "%Y-%m-%d")
end_date = datetime.strptime("2023-06-20", "%Y-%m-%d")

fake = Faker(("uk-UA"))

def get_list_date(start: date, end: date):
        result = []
        current_date = start
        while current_date <= end:
            if current_date.isoweekday() < 6:
                result.append(current_date)
            current_date += timedelta(1)
        return result
    
def fill_teachers(number_of_teachers):
    for _ in range(number_of_teachers):
        teacher = Teacher(fullname = fake.name())
        session.add(teacher)
    session.commit()
    
    
def fill_disciplines(list_of_disciplines):
    teacher_ids = session.scalars(select(Teacher.id)).all()
    for discipline in list_of_disciplines:
        session.add(Discipline(name=discipline, teacher_id=choice(teacher_ids)))
    session.commit()
    
def fill_groups(list_of_groups):
    for group in list_of_groups:
        session.add(Group(name=group))
    session.commit
    
def fill_students(number_of_students):
    group_ids = session.scalars(select(Group.id)).all()
    for _ in range(number_of_students):
        session.add(Student(fullname=fake.name(), group_id=choice(group_ids)))      
    session.commit()

def fill_grades(number_grades_discipline, start_date, end_date):
    data_list = get_list_date(start_date, end_date)
    discipline_ids = session.scalars(select(Discipline.id)).all()
    student_ids = session.scalars(select(Student.id)).all()
    
    for data in data_list:   
        random_ids_student = [choice(student_ids) for _ in range(number_grades_discipline)]
        for student_id in random_ids_student:
            grade = Grade(
                grade = randint(min_grade,max_grade),
                date_of = data,
                student_id = student_id,
                discipline_id=choice(discipline_ids)
            )
            session.add(grade)
    session.commit()
    

if __name__ == "__main__":
    fill_teachers(NUMBER_TEACHERS)
    fill_disciplines(DISCIPLINES)
    fill_groups(GROUPS)
    fill_students(NUMBER_STUDENTS)
    fill_grades(NUMBER_GRADES_DISCIPLINE, start_date, end_date)
