def function_without_return():
    # print("This function does not have a return statement.")
    return
# Calling the function and storing the result in a variable
result = function_without_return()

# Checking the type of the result
type_of_result = type(result)

# This would print: (None, <class 'NoneType'>)
print(f'{result}\n{type_of_result}')
