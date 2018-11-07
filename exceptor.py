
class Exceptor:
    try:
        def catchit(self, name, exception):
            print("Error! in " + str(name) + ": " + str(exception))
            exit(1)
    except Exception as e:
        print("Error! in Exceptor.catchit(): " + str(e))
        exit(1)
