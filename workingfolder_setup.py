
import os

def get_user_exec():
    
    
    user = os.getlogin()

    if user.lower() == 'pkundurthy':
        ExecStatements =["MainPath = \'/astro/store/student-scratch1/pkundurthy/final_apostle/\'",\
                        "PicklePath = MainPath+'PickleStuff/\'",\
                        "ObjectList = [\'WASP2\',\'XO2\',\'TRES3\',\'GJ1214\']",\
                        "DataPrepPath = MainPath+\'DataPrep/\'",\
                        "FigurePath = MainPath+\'OtherFigures/\'",\
                        "PaperFiguresPath = MainPath+\'PaperFigures/\'"]
    elif user.lower() == 'acbecker':
        ExecStatements =["MainPath = \'/astro/users/acbecker/APOSTLE/runs/WASP2_new/WASP2/\'",\
                        "PicklePath = MainPath+'PickleStuff/\'",\
                        "ObjectList = [\'WASP2\',\'XO2\',\'TRES3\',\'GJ1214\']",\
                        "DataPrepPath = MainPath+\'DataPrep/\'",\
                        "FigurePath = MainPath+\'OtherFigures/\'",\
                        "PaperFiguresPath = MainPath+\'PaperFigures/\'"]
    else:
        raise NameError("Unknown user %s" % user)
    
    #ExecStatements =["MainPath = \'/astro/store/student-scratch1/pkundurthy/final_apostle/\'",\
                        #"PicklePath = MainPath+'PickleStuff/\'",\
                        #"ObjectList = [\'WASP2\',\'XO2\',\'TRES3\',\'GJ1214\']",\
                        #"DataPrepPath = MainPath+\'DataPrep/\'",\
                        #"FigurePath = MainPath+\'OtherFigures/\'",\
                        #"PaperFiguresPath = MainPath+\'PaperFigures/\'"]

    return ExecStatements