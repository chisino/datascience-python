# Author: Artiom Dolghi

def main():

    try:

        in_file_name = input("Enter the name of a file: ")
        in_file = open(in_file_name, "r")
        contents = in_file.read()

        out_file_name = "nodups-" + in_file_name

        out_file = open(out_file_name, "w")

        contents = contents.lower()
        contents = contents.split()

        wordList = []

        for word in contents:
            if word not in wordList:
                wordList.append(word)
        contents = ' '.join(wordList)

        out_file.write(contents)

        print(out_file_name + " has been created")

        in_file.close()
        out_file.close()

    except IOError:
        print("Error accessing the files")

main()

        

        

    
