'''Python program to "parse" java files'''
# Assumption: Indentation is already correct
def PPL_Projecr02_main():
    with open('test.java') as f:
        print(f.read())

if __name__ == '__main__':
    PPL_Projecr02_main()
