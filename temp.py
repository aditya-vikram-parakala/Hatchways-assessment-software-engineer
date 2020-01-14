import os
import csv

class ReportGenerator:
    def __init__():


    #method to store tests.csv in a HashMap. {key:[value]} 
    def preprocess_tests_csv(filename):
        data = {}
        with open(filename) as f:
            reader = csv.DictReader(f)
            for row in reader:
                data[row["id"]] = [row["course_id"]]
                data[row["id"]].append(row["weight"])
            # print(data)
        return data
    
    def process_marks(marks_file):
        test_map = preprocess_tests_csv(r"C:\Users\aditya vikram\Desktop\Hatchways\backend-assessment\backend-assessment\tests.csv")
        final_marks_data = []
        with open(marks_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                marks_data = []
                marks_data.append(row["test_id"])
                marks_data.append(row["student_id"])
                marks_data.append(row["mark"])
                marks_data.extend(test_map.get(marks_data[0]))
                final_marks_data.append(marks_data)
        # print("final",final_marks_data)
        # print(len(final_marks_data))
        return final_marks_data
    table = process_marks(r"C:\Users\aditya vikram\Desktop\Hatchways\backend-assessment\backend-assessment\marks.csv")

    def generate_student_report(table):
        student = {}
        for row in table:
            running_sum = 0.0
            temp = {}
            if(row[1] not in student):
                student[row[1]] = temp
                if(row[3] not in temp):
                    running_sum+=(int(row[-1])* int(row[2])/100)
                    temp[row[3]] = running_sum
                else:
                    temp[row[3]]+=(int(row[-1])* int(row[2])/100)
            else:
                course_map = student[row[1]]
                if(row[3] not in course_map):
                    running_sum+=(int(row[-1])* int(row[2])/100)
                    course_map[row[3]] = running_sum
                else:
                    course_map[row[3]]+=(int(row[-1])* int(row[2])/100)
        # print("FUCK YOU !!!",student)
        return student
    students_report = generate_student_report(table)


    def courses_map(course_file):
        course_map = {}
        with open(course_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                course_map[row["id"]] = [row["name"]]
                course_map[row["id"]].append(row["teacher"])
            # print(course_map)
        return course_map
    courseMap = courses_map(r"C:\Users\aditya vikram\Desktop\Hatchways\backend-assessment\backend-assessment\courses.csv")

    def students_map(student_file):
        student_map = {}
        with open(student_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                student_map[row["id"]] = row["name"]
            # print(student_map)
        return student_map
    s_name = students_map(r"C:\Users\aditya vikram\Desktop\Hatchways\backend-assessment\backend-assessment\students.csv")

    def calculate_average(student_course_map):
        local_sum = 0
        for k in student_course_map.keys():
            local_sum+=student_course_map[k]
        return local_sum/len(student_course_map)

    def display_report(students_report):
        f = open("Report.txt","w+")
        for student_id in sorted(students_report.keys()):
            avg = calculate_average(students_report[student_id])
            f.write("\n")
            f.write("\n")
            f.write("Student Id: %d" %(int(student_id)))
            f.write(", name: %s" %(s_name[student_id]))
            f.write("\n")
            f.write("Total Average: %d" %(avg))
            f.write("%")
            c_map = students_report[student_id]
            for course in c_map.keys():
                f.write("\n")
                f.write("\n")
                f.write("\t")
                f.write("Course:%s" %(courseMap[course][0]))
                f.write(", Teacher: %s" %(courseMap[course][1]))
                f.write("\n")
                f.write("\t")
                f.write("Final Grade: %s" %(c_map[course]))
                f.write("%")
        f.close()
        print("Done..!!...")

display_report(students_report)





























        







