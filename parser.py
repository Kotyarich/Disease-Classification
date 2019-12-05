import xlrd as x
import re


def get_data():
    xls_fl = x.open_workbook("dannye-onkologia.xls", formatting_info=True)
    sheet = xls_fl.sheet_by_index(0)

    valid_columns = [1]
    valid_columns += [i for i in range(9, 29)]
    valid_columns += [i for i in range(30, 55)]

    first_col = []
    result_mtr = []

    for i in range(1, sheet.nrows):
        cur_row = sheet.row_values(i)

        if not re.findall("C18", cur_row[0]):
            first_col.append(0)
        else:
            first_col.append(1)

        result_mtr.append([])
        for j in valid_columns:
            if cur_row[j] == "нет":
                result_mtr[i - 1].append(0)
            elif cur_row[j] == "да":
                result_mtr[i - 1].append(1)
            else:
                result_mtr[i - 1].append(cur_row[j])
    return first_col, result_mtr


if __name__ == "__main__":
    _, result_mtr = get_data()
    outFile = open("tstof.txt", "w")

    for i in result_mtr:
        outFile.write(str(i) + "\n")

    outFile.close()
