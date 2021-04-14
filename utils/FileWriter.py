import os
def writeFile(df, fileName, mode='a'):
    # if not os.path.isfile(fileName):
    #         df.to_csv(fileName)
    #         print("Data write to "+fileName)
    # else:
    #     if mode == 'a':
    #         df.to_csv(fileName, mode='a', header=False)
    #         print("Data append to "+fileName)
    if mode == 'a':
        if not os.path.isfile(fileName):
           df.to_csv(fileName, index=False)
           return
        df.to_csv(fileName, mode='a', header=False, index=False)
        print("Data append to "+fileName)
    else:
        df.to_csv(fileName, index=False)
        print("Data write to "+fileName)