from langchain_text_splitters import RecursiveCharacterTextSplitter , Language

text = """

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Student:
    name: str
    age: int
    marks: Dict[str, float]

    def average(self):
        return sum(self.marks.values()) / len(self.marks)

    def grade(self):
        avg = self.average()

        if avg >= 90:
            return "A+"
        elif avg >= 80:
            return "A"
        elif avg >= 70:
            return "B"
        elif avg >= 60:
            return "C"
        else:
            return "F"


class Course:
    def __init__(self, name: str, instructor: str):
        self.name = name
        self.instructor = instructor
        self.students: List[Student] = []

    def add_student(self, student: Student):
        self.students.append(student)

    def get_top_student(self):
        if not self.students:
            return None
        return max(self.students, key=lambda s: s.average())

    def statistics(self):
        if not self.students:
            return {}

        averages = [student.average() for student in self.students]

        return {
            "total_students": len(self.students),
            "highest": max(averages),
            "lowest": min(averages),
            "class_average": sum(averages) / len(averages)
        }


def create_students():
    return [
        Student(
            "Alice",
            20,
            {"Python": 92, "Math": 88, "AI": 95}
        ),
        Student(
            "Bob",
            21,
            {"Python": 78, "Math": 82, "AI": 74}
        ),
        Student(
            "Charlie",
            19,
            {"Python": 96, "Math": 91, "AI": 89}
        ),
        Student(
            "David",
            22,
            {"Python": 67, "Math": 72, "AI": 70}
        )
    ]


def generate_report(course: Course):
    top_student = course.get_top_student()
    stats = course.statistics()

    print(f"Course: {course.name}")
    print(f"Instructor: {course.instructor}")
    print(f"Students: {stats['total_students']}")
    print(f"Class Average: {stats['class_average']:.2f}")
    print(f"Highest Average: {stats['highest']:.2f}")
    print(f"Lowest Average: {stats['lowest']:.2f}")

    if top_student:
        print(f"Top Student: {top_student.name}")
        print(f"Top Grade: {top_student.grade()}")


def student_generator(students):
    for student in students:
        yield student


students = create_students()

course = Course(
    name="Python and Artificial Intelligence",
    instructor="Dr. Sharma"
)

for student in students:
    course.add_student(student)

for student in student_generator(students):
    print(
        student.name,
        student.average(),
        student.grade()
    )

generate_report(course)


"""

splitter = RecursiveCharacterTextSplitter.from_language(
    language = Language.PYTHON,
    chunk_size = 400,
    chunk_overlap = 0
)

chunks = splitter.split_text(text)

for i , chunk in enumerate(chunks):
    print(f"Chunk {i} : \n{chunk}\n\n")