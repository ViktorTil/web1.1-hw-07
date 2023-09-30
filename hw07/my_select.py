from pprint import pprint
from sqlalchemy import and_, func, desc, select

from fill_data import DISCIPLINES, GROUPS
from src.models import Teacher, Student, Discipline, Grade, Group
from src.db import session

TEACHERS = session.scalars(select(Teacher.fullname)).all()
STUDENTS = session.scalars(select(Student.fullname)).all()

number_choices = 12
filename = 'my_select.txt'


def choose_id_item(items, item_name):
    for id, item in enumerate(items,1):
        print("id-{}:  {}".format(id, item))
    while True:       
        try:
            id_result = int(input(f"Please choose id-number {item_name} from the previous list(only number!!! from range: (1 - {len(items)})) > "))
            if id_result in range(1,len(items)+1):
                return id_result
        except ValueError:
            print(f"Enter number(not letters or symbols)")


#--1-- Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1():   
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade),2).label('avg_grade'))\
            .select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    return result


#--2-- Знайти студента із найвищим середнім балом з певного предмета.
def select_2():
    discipline_id = choose_id_item(DISCIPLINES)
    result = session.query(Student.fullname, 
                           Discipline.name, 
                           func.round(func.avg(Grade.grade), 2).label('avg_grade')
                            )\
                    .select_from(Grade) \
                    .join(Student)\
                    .join(Discipline)\
                    .filter(Discipline.id == discipline_id)\
                    .group_by(Student.id, Discipline.name)\
                    .order_by(desc('avg_grade'))\
                    .limit(1).all()
    return result


#--3-- Знайти середній бал у групах з певного предмета.
def select_3():
    discipline_id = choose_id_item(DISCIPLINES, 'discipline')
    result = session.query(Group.name,
                           Discipline.name,
                           func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
                            .select_from(Grade)\
                            .join(Discipline)\
                            .join(Student)\
                            .join(Group)\
                            .filter(Discipline.id == discipline_id)\
                            .group_by(Group.name, Discipline.name)\
                            .order_by(desc('avg_grade')).all()
    return result


#--4-- Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4():
    result = session.query(func.round(func.avg(Grade.grade),2)).all()
    return result


#--5-- Знайти які курси читає певний викладач.
def select_5():
    teacher_id = choose_id_item(TEACHERS, 'teacher')
    result = session.query(Teacher.fullname, Discipline.name)\
        .select_from(Teacher)\
        .join(Discipline)\
        .filter(Teacher.id == teacher_id).all()
    return result


#--6-- Знайти список студентів у певній групі.
def select_6():
    group_id = choose_id_item(GROUPS, 'group')
    result = session.query(Group.name, Student.fullname)\
        .select_from(Student)\
        .join(Group)\
        .filter(Group.id == group_id)\
        .order_by(Student.fullname).all()
    return result


#--7-- Знайти оцінки студентів у окремій групі з певного предмета.
def select_7():
    group_id = choose_id_item(GROUPS, 'group')
    discipline_id = choose_id_item(DISCIPLINES, 'discipline')
    result = session.query(Group.name, Discipline.name, Student.fullname, Grade.grade)\
        .select_from(Grade)\
        .join(Discipline)\
        .join(Student)\
        .join(Group)\
        .filter(and_(Group.id == group_id, Discipline.id == discipline_id))\
        .order_by(Student.fullname).all()
    return result


#--8-- Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8():
    teacher_id = choose_id_item(TEACHERS, 'teacher')
    result = session.query(Teacher.fullname, Discipline.name, func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
        .select_from(Grade)\
        .join(Discipline)\
        .join(Teacher)\
        .filter(Teacher.id == teacher_id)\
        .group_by(Teacher.fullname, Discipline.name)\
        .all()
    return result


#--9-- Знайти список курсів, які відвідує студент.
def select_9():
    student_id = choose_id_item(STUDENTS, 'student')
    result = session.query(Student.fullname, Discipline.name)\
        .select_from(Student)\
        .join(Grade)\
        .join(Discipline)\
        .filter(Student.id == student_id)\
        .group_by(Student.fullname,Discipline.name).all()
    return result


#--10-- Список курсів, які певному студенту читає певний викладач..
def select_10():
    teacher_id = choose_id_item(TEACHERS, 'teacher')
    student_id = choose_id_item(STUDENTS, 'student')
    result = session.query(Student.fullname, Teacher.fullname,
                           Discipline.name)\
        .select_from(Grade)\
        .join(Discipline)\
        .join(Teacher)\
        .join(Student)\
        .filter(and_(Teacher.id == teacher_id, Student.id == student_id ))\
        .group_by(Student.fullname, Teacher.fullname, Discipline.name).all()
    return result


#--11-- Середній бал, який певний викладач ставить певному студентові.
def select_11():
    teacher_id = choose_id_item(TEACHERS, 'teacher')
    student_id = choose_id_item(STUDENTS, 'student')
    result = session.query(Student.fullname, Teacher.fullname,
                           Discipline.name, func.round(func.avg(Grade.grade), 2)\
                          .label('avg_grade'))\
        .select_from(Grade)\
        .join(Discipline)\
        .join(Teacher)\
        .join(Student)\
        .filter(and_(Teacher.id == teacher_id, Student.id == student_id ))\
        .group_by(Student.fullname, Teacher.fullname, Discipline.name).all()
    return result   


#--12-- Оцінки студентів у певній групі з певного предмета на останньому занятті.
def select_12():
    group_id = choose_id_item(GROUPS, 'group')
    discipline_id = choose_id_item(DISCIPLINES, 'discipline')
    subquery = (select(Grade.date_of).join(Student).join(Group).where(
        and_(Grade.discipline_id == discipline_id, Group.id == group_id)
        ).order_by(desc(Grade.date_of)).limit(1).scalar_subquery())
    result = session.query(Group.name,
                           Student.fullname,
                           Discipline.name,
                           Grade.grade,
                           Grade.date_of)\
                .select_from(Grade)\
                .join(Student)\
                .join(Discipline)\
                .join(Group)\
                .filter(and_( Discipline.id == discipline_id, Group.id == group_id, Grade.date_of == subquery))\
                .order_by(desc(Grade.date_of))\
                .all()
    return result  


if __name__ == '__main__':  
    with open (filename, 'r') as fh:
        list_choice = fh.readlines()
        for line in list_choice:
            print(line)  
    while True:
        try:
            num = input(f"{chr(10)}Input number of select function: > ")
            print(f"{list_choice[int(num)-1] if int(num) in range(1,number_choices+1) else ''}")
            pprint(globals()['select_'+num]())
            break
        except (KeyError, IndexError, ValueError):
            print(f"Input number in range: (1 - {number_choices})!!!")

