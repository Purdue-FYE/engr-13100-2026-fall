def attendance(status):
    if status == "yes":
        return "Present"
    else:
        return "Absent"

status = "yes"
result = attendance(status)
print(result)
