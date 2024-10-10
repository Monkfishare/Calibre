file_path = "month.txt"
months = [f"{i:02d}" for i in range(9, 0, -1) if i != 8]
# months = [f"{i:02d}" for i in range(9, 0, -1)]

with open(file_path, "w") as file:
    file.write("\n".join(months))

print(f"All months have been written to '{file_path}'.")
