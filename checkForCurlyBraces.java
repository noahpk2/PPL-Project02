def checkForCurlyBraces(line, file):
    wordList = ["if", "else", "switch", "for", "while", "do"]
    curlyStack = []
    temp = line.split(" ", 1)[0]
    lastChar = line.split()[-1:]
    if temp in wordList:
        if "{" == lastChar:
            curlyStack.push()
        else:
            file.write(line + "{")
    if lastChar == "}":
        curlyStack.pop()

