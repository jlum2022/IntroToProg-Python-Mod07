1# ------------------------------------------------- #
# Title: Module 07 – Creating Applications
# Desc: This assignment demonstrates using data classes with structured error handling
# ChangeLog: (Who, When, What)
# JLum,2.26.2024 Created for A07
# ------------------------------------------------- #

import json

# ======================================================================
# Define the Data Constants

# Set up menu to display for the user
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:
    1. Register a Student for a Course
    2. Show current data
    3. Save data to a file
    4. Exit the program
-----------------------------------------
'''

FILE_NAME: str = "Enrollments.json"     # This is the data file we will read from and write to

# ======================================================================
# Define the Data Variables
menu_choice: str = ""   # initialize user's menu choice to empty string.
students: list = []     # initialize an empty list for holding a list of student records

# ======================================================================
# Define the classes


# TODO Create a Person Class
class Person:
    """
    A class representing person data.

    Properties:
        first_name (str): The person's first name.
        last_name (str): The person's last name.

    ChangeLog:
    JLum, 2.26.2024: Created for A07
    """

    # TODO Add first_name and last_name properties to the constructor
    def __init__(self, first_name: str = "", last_name: str = ""):
        """
        Constructor for the Person class. Initializes the first & last name properties to an empty string.
        """
        self.first_name = first_name
        self.last_name = last_name

    # TODO Create a getter and setter for the first_name property
    # There is a known bug which manifests itself if an empty string is disallowed for first or last name.
    # I was unable to fix it in time so I left it in.

    # The @property decorator indicates that this function is a getter (also called accessor)
    # it lets you access the data and optionally add formatting code.
    @property
    def first_name(self):
        """
        Getter for the student's first name.
        """
        return self.__first_name.title()  # title() formats the data in Title case

    # Setter property functions let you add code for both validation and error handling.
    # If a valid value is passed into the function, then it is assigned to the attribute.
    # The decorator syntax is '@' + property_name + '.setter'
    @first_name.setter
    def first_name(self, value: str):
        """
        Setter for the student's first name.
        """
        if value.isalpha() or value == "":
            self.__first_name = value
        else:
            raise ValueError("First name must be alphabetic only. Please re-enter.")

    # TODO Create a getter and setter for the last_name property
    @property
    def last_name(self):
        """
        Getter for the student's last name.
        """
        return self.__last_name.title()  # title() formats the data in Title case

    @last_name.setter
    def last_name(self, value: str):
        """
        Setter for the student's last name.
        """
        if value.isalpha() or value == "":
            self.__last_name = value
        else:
            raise ValueError("Last name must be alphabetic only. Please re-enter.")

    # TODO Override the __str__() method to return Person data
    def __str__(self):
        """
        String method for the Person class. Returns a human-friendly string representation of the Person object.
        """
        return f'{self.first_name},{self.last_name}'


# TODO Create a Student class the inherits from the Person class 
class Student(Person):
    """
    A class representing student data which inherits from Person class.

    Properties:
    - first_name (str): The student's first name.
    - last_name (str): The student's last name.
    - course_name (str): The name of the course the student is registered for.

    ChangeLog: (Who, When, What)
    JLum, 2.26.2024: Created for A07
    """

    # TODO call to the Person constructor and pass it the first_name and last_name data
    def __init__(self, first_name: str = "", last_name: str = "", course_name: str = ""):
        """
        Constructor for the Student class. Calls the initializer of the super class (Person)
        to set values for the student's first and last name
        """
        super().__init__(first_name=first_name,last_name=last_name)

        # TODO add an assignment to the course_name property using the course_name parameter
        # initialize the course name property which is not inherited from the Person class 
        self.course_name = course_name

    # The Student class has 1 additional property not available in Person, so we have to get & set it here.

    # TODO add the getter for course_name 

    @property
    def course_name(self):
        """
        Getter for student's course name.
        """
        return self.__course_name

    # TODO add the setter for course_name 
    @course_name.setter
    def course_name(self, value: str):
        """
        Setter for student's course name.
        """
        self.__course_name = value

    # TODO Override the __str__() method to return the Student data 
    # This method returns a human-friendly string representation of the object
    def __str__(self):
        """
        String method for the Student class. Returns a human-friendly string representation of the Student object.
        """
        return f"{self.first_name},{self.last_name},{self.course_name}"
    

class FileProcessor:
    """
    A collection of processing layer functions that work with json files

    ChangeLog: (Who, When, What)
    JLum, 2.26.2024: Created for A07
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """ This function reads data from a json file and loads it into a list of dictionary rows

        ChangeLog: (Who, When, What)
        JLum,2.26.2024 Created for A07

        :param file_name: string data with name of file to read from
        :param student_data: list of dictionary rows to be filled with file data

        :return: list
        """
        try:
            with open(file_name, "r") as file:
                list_of_dictionary_data = json.load(file)  # the load function returns a list of dictionary rows.
                for student in list_of_dictionary_data:
                    student_object: Student = Student(first_name=student["FirstName"],
                                                      last_name=student["LastName"],
                                                      course_name=student["CourseName"])
                    student_data.append(student_object)
        except FileNotFoundError as e:
            IO.output_error_messages("Text file must exist before running this script!", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)
        return student_data

    # When a method is used directly from the class, you leave out the "self" parameter 
    # and mark the method with the @staticmethod decorator as we have seen in earlier modules.
    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """ This function writes data to a json file with data from a list of dictionary rows

        ChangeLog: (Who, When, What)
        JLum,2.26.2024,Created for A07

        :param file_name: string data with name of file to write to
        :param student_data: list of dictionary rows to be writen to the file

        :return: None
        """
        try:
            list_of_dictionary_data: list = []
            for student in student_data:  # Convert List of Student objects to list of dictionary rows.
                student_json: dict = {"FirstName": student.first_name,
                                      "LastName": student.last_name,
                                      "CourseName": student.course_name}
                list_of_dictionary_data.append(student_json)

            with open(file_name, "w") as file:
                json.dump(list_of_dictionary_data, file)
        except TypeError as e:
            IO.output_error_messages("Please check that the data is a valid JSON format", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)


class IO:
    """
    A collection of presentation layer functions that manage user input and output

    ChangeLog: (Who, When, What)
    JLum,2.26.2024,Created for A07
    """
    pass

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ Displays custom error messages

        ChangeLog: (Who, When, What)
        JLum,2.26.2024,Created for A07

        :param message: string with message data to display
        :param error: Exception object with technical message to display

        :return: None
        """

        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message on print() function -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ Display the menu of choices for this program.

        ChangeLog: (Who, When, What)
        JLum,2.26.2024,Created for A07

        :return: None
        """
        # print()    # too much white space
        print(menu)
        # print()    # too much white space

    @staticmethod
    def input_menu_choice():
        """ Prompt the user to enter their choice from the menu

        ChangeLog: (Who, When, What)
        JLum,2.26.2024,Created for A07

        :return: string with the user's choice
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):  # Note these are strings
                raise Exception("Please enter only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # passing the exception object to avoid the technical message

        return choice

    @staticmethod
    def output_student_data(student_data: list):
        """ This function displays the student data to the user

        ChangeLog: (Who, When, What)
        JLum,2.26.2024,Created for A07

        :param student_data: list of student object data to be displayed

        :return: None
        """
        try:
            message: str = ''
            print()
            print("-" * 50)
            for student in student_data:
                message = "First name: {}, Last name: {}, Course Name: {}"

                print(message.format(student.first_name, student.last_name, student.course_name))
            print("-" * 50)
            print()
        except Exception as e:
            IO.output_error_messages(e.__str__())  # passing the exception object to avoid the technical message

    @staticmethod
    def input_student_data(student_data: list):
        """ This function gets the first name, last name, and course name from the user

        ChangeLog: (Who, When, What)
        JLum,2.26.2024,Created for A07

        :param student_data: list of dictionary rows to be filled with input data

        :return: list
        """

        try:
            # Input the data
            student = Student()
            student.first_name = input("Enter the student's first name: ")
            if not student.first_name.isalpha():
                raise ValueError("First name must be alphabetic only. Please try again.")
            student.last_name = input("Enter the student's last name: ")
            if not student.last_name.isalpha():
                raise ValueError("Last name must be alphabetic only. Please try again.")
            student.course_name = input("Enter the student's course name:")         
            if not student.last_name.isalnum():
                raise ValueError("Last name must be alphabetic only. Please try again.")

            student_data.append(student)

        except ValueError as e:
            IO.output_error_messages("That value is not the correct type of data.", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error.", e)
        return student_data


# -----------------------------------------
# Beginning of the main body of this script
# When the application starts, the contents of the file "Enrollments.json" are
# automatically read into a 2-dimensional list table (a list of Student object rows).

students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Repeat the follow tasks
while True:
    # display the menu
    IO.output_menu(menu=MENU)

    # prompt user for a choice
    menu_choice = IO.input_menu_choice()

    if menu_choice == "1":  # Get new data ( and display the change)
        students = IO.input_student_data(student_data=students)
        IO.output_student_data(student_data=students)
        continue

    elif menu_choice == "2":  # Display current data
        IO.output_student_data(student_data=students)
        continue

    elif menu_choice == "3":  # Save data back to the file
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    elif menu_choice == "4":  # End the program
        break  # out of the while loop
