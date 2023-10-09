'''Python program to "parse" java files'''
# Assumption: Indentation is already correct
def PPL_Project02_main():

    java_file = 'test.java'
    txt_file = 'test-file.txt'

    with open(java_file, 'r') as java_file:
        java_content = java_file.read()

    with open(txt_file, 'w') as txt_file:
        txt_file.write(java_content)

    with open("test-file.txt") as file:
        print(file.read())

if __name__ == '__main__':
    PPL_Project02_main()
