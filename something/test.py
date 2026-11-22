public class Employee {
    map<Integer, employee> record = new HashMap<>();

    void saveEmployee(Employee e) throws dupliacteed Employee
    if(record.containsKey(e.getId())) {
        throw new DuplicateEmployeeException("Employee with ID " + e.getId() + " already exists.");
    }
    record.put(e.getId(), e);

}
void search employeebyid(int empid) throws EmployeeNotFoundException {
    if(!record.containsKey(empid)) {
        throw new EmployeeNotFoundException("Employee with ID " + empid + " not found.");
    }
    return record.get(empid);
}