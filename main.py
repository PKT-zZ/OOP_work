#********************/
# MSSV: 202418996
# Ho ten: Nguyễn Khánh Toàn
#********************/


class Employee:
    def __init__(self, id="UNKNOWN", fullName="Unnamed employee", baseSalary=0):
        if id == "":
            raise ValueError("Invalid id")
        if fullName == "":
            raise ValueError("Invalid name")
        if baseSalary < 0:
            raise ValueError("Invalid salary")

        self._id = id
        self._fullName = fullName
        self._baseSalary = baseSalary

    def getId(self):
        return self._id

    def getFullName(self):
        return self._fullName

    def getBaseSalary(self):
        return self._baseSalary

    def increaseSalary(self, value, byPercentage=False):
        if value <= 0:
            raise ValueError("Invalid increase value")
        if byPercentage:
            self._baseSalary += self._baseSalary * value / 100
        else:
            self._baseSalary += value

    def calculateMonthlyCost(self):
        return self._baseSalary

    def displayInfo(self):
        print(f"Employee | ID: {self._id} | Name: {self._fullName} | Base salary: {self._baseSalary:.2f}")

    def __del__(self):
        if hasattr(self, "_id"):
            print(f"Deleting Employee {self._id} ({self._fullName})")


class SoftwareEngineer(Employee):
    #(id, fullName, primaryLanguage) / (id, fullName, baseSalary, primaryLanguage, technicalAllowance)
    def __init__(self, id, fullName, *args):
        if len(args) == 1:
            baseSalary = 0
            primaryLanguage = args[0]
            technicalAllowance = 0
        elif len(args) == 3:
            baseSalary, primaryLanguage, technicalAllowance = args
        else:
            raise TypeError("Wrong number of arguments")

        if primaryLanguage == "":
            raise ValueError("Invalid language")
        if technicalAllowance < 0:
            raise ValueError("Invalid allowance")

        super().__init__(id, fullName, baseSalary)

        self._primaryLanguage = primaryLanguage
        self._technicalAllowance = technicalAllowance

    def getPrimaryLanguage(self):
        return self._primaryLanguage

    def getTechnicalAllowance(self):
        return self._technicalAllowance

    def calculateMonthlyCost(self):
        return self._baseSalary + self._technicalAllowance

    def displayInfo(self):
        print(f"Software Engineer | ID: {self._id} | Name: {self._fullName} | Base salary: {self._baseSalary:.2f} | "
              f"Language: {self._primaryLanguage} | Allowance: {self._technicalAllowance:.2f}")

    def __del__(self):
        if hasattr(self, "_primaryLanguage"):
            print(f"Deleting SoftwareEngineer {self._id} ({self._fullName})")
        super().__del__()


class ProjectTeam:
    def __init__(self, projectCode, projectName, leader=None):
        self._projectCode = projectCode
        self._projectName = projectName
        self._members = []
        self._leader = None

        #neu co leader ngay tu dau thi them vao members luon
        if leader is not None:
            self.addMember(leader, True)

    def getProjectCode(self):
        return self._projectCode

    def getProjectName(self):
        return self._projectName

    def getLeader(self):
        return self._leader

    def getMembers(self):
        return list(self._members)

    def findMember(self, employeeId):
        for member in self._members:
            if member.getId() == employeeId:
                return member
        return None

    def contains(self, employeeId):
        return self.findMember(employeeId) is not None

    def addMember(self, employee, makeLeader=False):
        if self.contains(employee.getId()):
            print("Employee already exists")
            return False

        self._members.append(employee)
        if makeLeader:
            self._leader = employee
            print("Employee added as leader")
        else:
            print("Employee added")
        return True

    def removeMember(self, employeeId):
        member = self.findMember(employeeId)
        if member is None:
            print("Employee not found")
            return False

        #khong cho xoa leader, phai doi leader truoc
        if member is self._leader:
            print("Cannot remove the leader")
            return False

        self._members.remove(member)
        print("Member removed")
        return True

    def changeLeader(self, employee):
        member = self.findMember(employee.getId())
        if member is None:
            #leader moi chua la member thi them vao truoc
            self._members.append(employee)
        elif member is not employee:
            print("Employee already exists")
            return False

        self._leader = employee
        print("Leader changed")
        return True

    def calculateTotalMonthlyCost(self):
        total = 0
        for member in self._members:
            total += member.calculateMonthlyCost() #goi da hinh, employee hay engineer deu duoc
        return total

    def displayTeam(self):
        print(f"Project {self._projectCode}: {self._projectName}")
        if self._leader is None:
            print("Leader: none")
        else:
            print(f"Leader: {self._leader.getFullName()} ({self._leader.getId()})")
        print(f"Members: {len(self._members)}")
        for member in self._members:
            member.displayInfo()

    def __del__(self):
        if hasattr(self, "_projectCode"):
            print(f"Deleting ProjectTeam {self._projectCode}")
            #chi go danh sach lien ket cua team, khong dong den employee
            self._members.clear()


#buoc 13 va 14: team2 chi song trong ham nay, het ham la bi huy
def demoSecondTeam(sharedEmployee, engineer):
    print("\n----- Step 13: Second team shares an employee with team1 -----")
    team2 = ProjectTeam("P02", "Mobile App", engineer)
    team2.addMember(sharedEmployee)
    print(sharedEmployee.getId(), "is in team2:", team2.contains(sharedEmployee.getId()))
    team2.displayTeam()
    print("Total monthly cost of team2:", team2.calculateTotalMonthlyCost())

    print("\n----- Step 14: End demoSecondTeam -----")


def main():
    print("----- Step 1: Create Employees with the constructors -----")
    defaultEmp = Employee()
    shortEmp = Employee("E00", "Tam")
    emp1 = Employee("E01", "An", 1000)
    emp2 = Employee("E02", "Binh", 1500)
    defaultEmp.displayInfo()
    shortEmp.displayInfo()
    emp1.displayInfo()
    emp2.displayInfo()

    print("\n----- Step 2: Create SoftwareEngineers with the constructors -----")
    se1 = SoftwareEngineer("E03", "Chi", "Python")
    se2 = SoftwareEngineer("E04", "Dung", 2000, "Java", 500)
    se1.displayInfo()
    se2.displayInfo()
    print("se2 is an Employee:", isinstance(se2, Employee))
    print("se1 monthly cost:", se1.calculateMonthlyCost(), "(0 + 0)")
    print("se2 monthly cost:", se2.calculateMonthlyCost(), "(2000 + 500)")

    print("\n----- Step 3: Increase salary by a fixed amount (emp1) -----")
    emp1.increaseSalary(200)
    print("Increase by 200:", emp1.getBaseSalary())
    emp1.increaseSalary(300, False)
    print("Increase by 300 (byPercentage=False):", emp1.getBaseSalary())

    print("\n----- Step 4: Increase salary by percentage (emp2) -----")
    emp2.increaseSalary(10, True)
    print("Increase by 10 percent:", emp2.getBaseSalary())

    print("\n----- Step 5: Create a team without a leader -----")
    team1 = ProjectTeam("P01", "Student Management")
    team1.displayTeam()

    print("\n----- Step 6: addMember(employee) -----")
    team1.addMember(emp1)
    team1.addMember(emp2)
    team1.addMember(se1)

    print("\n----- Step 7: addMember(employee, makeLeader=True) -----")
    team1.addMember(se2, True)
    print("Leader:", team1.getLeader().getFullName())

    print("\n----- Step 8: Add an existing member again -----")
    print("Returned:", team1.addMember(emp1))
    print("Members:", len(team1.getMembers()))

    print("\n----- Step 9: Display the team (polymorphism) -----")
    team1.displayTeam()

    print("\n----- Step 10: Total monthly cost -----")
    print("Total monthly cost:", team1.calculateTotalMonthlyCost(), "(1500 + 1650 + 0 + 2500)")

    print("\n----- Step 11: Try to remove the current leader -----")
    print("Returned:", team1.removeMember("E04"))
    print("E04 is still in team1:", team1.contains("E04"))

    print("\n----- Step 12: Change the leader, then remove the old leader -----")
    team1.changeLeader(emp2)
    print("Returned:", team1.removeMember("E04"))
    print("E04 is in team1:", team1.contains("E04"))
    team1.displayTeam()

    demoSecondTeam(emp1, se2)

    print("\n----- Step 15: Employees still exist after team2 is destroyed -----")
    emp1.displayInfo()
    se2.displayInfo()
    print("emp1 is still in team1:", team1.contains("E01"))

    print("\n===== Edge case 1: Invalid data =====")
    print("Empty id:")
    try:
        Employee("", "Nobody", 100)
    except ValueError as e:
        print("Error:", e)
    print("Empty name:")
    try:
        Employee("E90", "", 100)
    except ValueError as e:
        print("Error:", e)
    print("Negative salary:")
    try:
        Employee("E90", "Nobody", -100)
    except ValueError as e:
        print("Error:", e)
    print("Empty language:")
    try:
        SoftwareEngineer("E91", "Nobody", "")
    except ValueError as e:
        print("Error:", e)
    print("Negative allowance:")
    try:
        SoftwareEngineer("E91", "Nobody", 1000, "Go", -50)
    except ValueError as e:
        print("Error:", e)

    print("\n===== Edge case 2: Duplicate member and leader =====")
    print("Add emp1 again:")
    print("Returned:", team1.addMember(emp1))
    twin = Employee("E01", "Twin An", 500)
    print("Add a different object with the same id as emp1:")
    print("Returned:", team1.addMember(twin))
    print("Add an existing member (se1) with makeLeader=True:")
    print("Returned:", team1.addMember(se1, True))
    print("Leader is still:", team1.getLeader().getFullName())
    print("Change leader to an existing member (se1):")
    print("Returned:", team1.changeLeader(se1))
    print("Leader:", team1.getLeader().getFullName(), "| Members:", len(team1.getMembers()))
    print("Old leader (emp2) is still a member:", team1.contains("E02"))

    print("\n===== Edge case 3: New leader is not a member yet =====")
    se3 = SoftwareEngineer("E05", "Hoa", 1800, "C++", 300)
    print("se3 is in team1:", team1.contains("E05"))
    print("Returned:", team1.changeLeader(se3))
    print("se3 is in team1:", team1.contains("E05"))
    print("Leader:", team1.getLeader().getFullName(), "| Members:", len(team1.getMembers()))
    print("Remove the old leader (se1):")
    print("Returned:", team1.removeMember("E03"))
    print("se1 is not in team1 but still exists:")
    se1.displayInfo()
    team1.displayTeam()

    print("\n===== End of program =====")


if __name__ == "__main__":
    main()
