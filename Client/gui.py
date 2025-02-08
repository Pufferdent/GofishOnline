class gui:
    def log(text):
        with open("logs", "a") as file:
            file.write(text + "\n")

    def print(text):
        print(text)
        gui.log("PRINTED: " + text)

    def input(text):
        return input(text)
    
    def error(text):
        print("Error: " + text)
        gui.log("ERROR: " + text)

if __name__ == "__main__":
    gui.print("Tested gui.py")