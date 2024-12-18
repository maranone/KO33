def file_to_variable(file_name, db_total, db_variable, encoding='utf-8'):
    try:
        with open(file_name, 'r', encoding=encoding) as file:
            lines = file.readlines()
            db_variable.extend([line.strip() for line in lines])  # Add each line to the list, stripping the newline
            db_total[0] = len(lines)  # Update the total count (as a list to make it mutable)
    except UnicodeDecodeError:
        print(f"Error reading file {file_name}: UnicodeDecodeError, trying different encoding")
        # Try a different encoding if the default fails
        try:
            with open(file_name, 'r', encoding='latin1') as file:
                lines = file.readlines()
                db_variable.extend([line.strip() for line in lines])
                db_total[0] = len(lines)
        except Exception as e:
            print(f"Error reading file {file_name}: {e}")
