import pandas as pd
# import os
import pickle

def make_submat(sheet_name, sheet_nparr, mat):
    # the 8 layers of nodes. A combo of them forms a "path" from level 0 to 6.
    component = "component"
    function = "function"
    phase = "phase"
    fmode = "fmode"

    # update the nodes on our path whenever there is no empty entry.
    for i in range(0, len(sheet_nparr)):
        if type(sheet_nparr[i][0]) != float:
            component = sheet_nparr[i][0]
        if type(sheet_nparr[i][1]) != float:
            function = sheet_nparr[i][1]
        if type(sheet_nparr[i][2]) != float:
            phase = sheet_nparr[i][2]
        if type(sheet_nparr[i][4]) != float:
            fmode = sheet_nparr[i][4]

        key = component + ' ' + fmode
        harm = sheet_nparr[i][9] * sheet_nparr[i][10]
        pb = 0.02 if sheet_nparr[i][11] == 'Low' else 0.15
        rid = sheet_nparr[i][3]
        sight = sheet_nparr[i][13].replace("\n", "").replace(".", "")
        response = sheet_nparr[i][14]

        # add such 'path' to the dictionary. All duplications are prevented.
        add_row(mat, sheet_name, key, phase, pb, harm, sight, response)


# adds a path to the dictionary, as mentioned in the previous method.
def add_row(rows, name, key, phase, pb, harm, sight, response):
    if phase in ['Launch', 'Transit', 'Landing']: 
        phase = 'PreDeployment'
    if phase == 'Surface Ops':
        phase = 'SurfaceOps'
    rows.append([name, key, phase, pb, harm, sight, response])
    

# generates a matrix based on the input excel file.
def generate_matrix(path):
    names = read_xlsx(path)[0]
    arrs = read_xlsx(path)[1]
    mat = []
    for sheet_num in range(2, len(arrs), 1):
        make_submat(names[sheet_num], arrs[sheet_num], mat)
    return mat


# reads a xlsx filename as input and return an array of numpy arrays, each
# representing a unique sheet (ordered) or the xlsx file.
def read_xlsx(filename):
    # reads sheets of the xlsx file into a dictionary, each as a sheet item.
    sheets = pd.read_excel(filename+".xlsx", sheet_name=None)

    # an array that contains all sheet names (string) of the file
    sheet_names = []
    for item in sheets:
        sheet_names.append(item)

    # an array that contains all of the sheets, each of which as a numpy array.
    sheets_nparr = []
    for sheet_name in sheet_names:
        sheets_nparr.append(sheets[sheet_name].to_numpy())

    return sheet_names, sheets_nparr


result = generate_matrix("fmea_chart")

with open(r'fmea_mat', 'wb') as f:
    pickle.dump(result, f, pickle.HIGHEST_PROTOCOL)

print('done\n', len(result))

