import os
import csv

class ReportGenerator:
    
    def __init__(self, f_name):
        self.f_name = f_name
        self.table = self.process_marks("./backend-assessment/marks.csv")
        self.students_report = self.generate_student_report(self.table)
        self.courseMap = self.courses_map("./backend-assessment/courses.csv")
        self.s_name = self.students_map("./backend-assessment/students.csv")
        self.display_report(self.students_report)

    ''' method to store tests.csv in a HashMap . 
        key: id 
        value : list which has course_id, weight
    '''
    def preprocess_tests_csv(self, filename):
        data = {}
        with open(filename) as f:
            reader = csv.DictReader(f)
            for row in reader:
                data[row["id"]] = [row["course_id"]]

                data[row["id"]].append(row["weight"])
            # print(data)
        return data
    
    ''' method to store marks.csv in a list by joining the data from given csv files with tes_id as reference 
        2D list
    '''
    def process_marks(self, marks_file):
        test_map = self.preprocess_tests_csv("./backend-assessment/tests.csv")
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
    
    ''' core logic to process and store the student data in a nested HashMap.
        { student_id : { course_id: avg_course_mark}}
        This method would return a hashmap with updated values for each student in the csv file.     

    '''
    def generate_student_report(self, table):
        student = {}
        for row in table:
            try:
                #keep track of the course marks
                running_sum = 0.0
                temp = {}
                #populating the HashMap by checking the keys and updating the values accordingly.
                if(row[1] not in student):
                    student[row[1]] = temp
                    if(row[3] not in temp):
                        running_sum+=(int(row[-1]) * int(row[2])/100)
                        temp[row[3]] = running_sum
                    else:
                        temp[row[3]]+=(int(row[-1]) * int(row[2])/100)
                else:
                    course_map = student[row[1]]
                    if(row[3] not in course_map):
                        running_sum+=(int(row[-1]) * int(row[2])/100)
                        course_map[row[3]] = running_sum
                    else:
                        course_map[row[3]]+=(int(row[-1]) * int(row[2])/100)

            except:
                print("Exception occured while generating the student's report!")

        return student

    '''
    The below method used to store the courses csv in a HashMap.
    {id : [name,teacher]}
    '''    
    def courses_map(self, course_file):
        course_map = {}
        with open(course_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                course_map[row["id"]] = [row["name"]]
                course_map[row["id"]].append(row["teacher"])
            # print(course_map)
        return course_map
    
    ''' 
    The below method stores the students.csv file in a HashMap
    { id : name } 
    '''
    def students_map(self, student_file):
        student_map = {}
        with open(student_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                student_map[row["id"]] = row["name"]
            # print(student_map)
        return student_map
    
    '''
    The below method is used to calculate the average score of each course taken by the student
    returns average score.
    '''
    def calculate_average(self, student_course_map):
        local_sum = 0.0
        for k in student_course_map.keys():
            local_sum+=student_course_map[k]
        return float(local_sum)/len(student_course_map)
    '''
    The below method is used to write to the file i.e. report generation. 
    The Report is populated with each student's information.  
    '''
    def display_report(self, students_report):
        f = open(self.f_name,"w+")
        cnt = 0 
        for student_id in sorted(students_report.keys()):
            avg = self.calculate_average(students_report[student_id])
            if(cnt!=0):
                f.write("\n")
                f.write("\n")
            cnt+=1
            f.write("Student Id: %d" %(int(student_id)))
            f.write(", name: %s" %(self.s_name[student_id]))
            f.write("\n")
            f.write("Total Average: %.2f" %(avg))
            f.write("%")
            c_map = students_report[student_id]
            for course in c_map.keys():
                f.write("\n")
                f.write("\n")
                f.write("\t")
                f.write("Course:%s" %(self.courseMap[course][0]))
                f.write(", Teacher: %s" %(self.courseMap[course][1]))
                f.write("\n")
                f.write("\t")
                f.write("Final Grade: %.2f" %(c_map[course]))
                f.write("%")
            f.write("\n")
            f.write("\n")
        f.close()
        # print("Done..")

'''creating the instance of the class, whose constructor will perform all the operations
   and writes it to the specified file passes as argument.
'''
report = ReportGenerator("Students_Report.txt")
#change the argument to create a new report of your name of choice.
































        







