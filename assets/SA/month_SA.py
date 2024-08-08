file_path = "month.txt"
months = [f"{i:02d}" for i in range(6, 0, -1)]

with open(file_path, "w") as file:
    file.write("\n".join(months))

print(f"All months have been written to '{file_path}'.")
