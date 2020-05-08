if __name__ == "__main__":

    # Import pandas as "pd"
    import pandas as pd

    # Import OS to walk through directory
    import os

    # Import xlsxwriter for count file
    import xlsxwriter

    # Import numpy for math
    import numpy as np

    # Import scikit-learn for machine learning
    from sklearn.svm import LinearSVC
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.pipeline import Pipeline
    from sklearn import metrics

    # Get the path of this python file
    my_path = os.path.dirname(os.path.abspath(__file__))

    # Initialize file variables
    found_file = False
    input_file = ""
    input_root = ""
    file_name = ""

    # Initialize Loop Variables
    verified_while = 0
    add_to_training_while = 0

    # Initialize Count Variables
    total_count = 0
    sheet_counter = 1
    final_count_string = ""

    # Initialize Table Variables
    full_table = pd.DataFrame()
    new_training_table = pd.DataFrame()
    training_df = pd.DataFrame()
    temp_training_df = pd.DataFrame()

    # Initialize bool variables
    add_to_training_decision = False

    for root, dirs, files in os.walk(my_path):
        for file in files:
            if file.endswith(".xlsx"):
                input_path = root
                input_file = file
                file_name = os.path.splitext(input_file)[0]
                # print(os.path.join(root, file))

    if input_file == "":
        found_file = False
    else:
        found_file = True

    # File is found
    if found_file:
        # While loop handling input
        while verified_while != 1:
            file_verified = input("Is " + input_file + " the name of the file dropped by the client? (y/n) ")
            if file_verified == "y":
                verified_while = 1  # End loop
            elif file_verified == "n":
                print("Please remove all excess xlsx files from the directory and restart the script.")
                input("Press enter to stop this script.")
                exit()  # Exit script if input file is not correct
            else:
                print("Please enter either \"y\" for yes or \"n\" for no.")  # Retry for input

        # Update headers in file using machine learning
        print("Initializing machine learning module...")
        # Name the ML training file
        training_file = "TRAINING INFO.csv"

        # Load the ML training file
        try:
            training_df = pd.read_csv(training_file, header=0)
        except Exception as e:
            print("Something went wrong with the Machine Learning Training File. "
                  "Please check to make sure it is in this directory and named \"TRAINING INFO.csv\"")
            print("Error: " + str(e))
            input("Press enter to stop this script.")
            exit()  # Exit script if training file is not correct
        X = training_df['Given_Header']
        y = training_df['Adjusted_Header']
        if y.isnull().any():
            print("Some fields are missing in the training file.")
            print("Please write in the correct values into the \'Adjusted Header\' column in \"" + training_file + "\".")
            input("Press enter to stop this script.")
            exit()  # Exit script if training file has blank lines which would corrupt the machine learning

        # Build a vectorizer that splits strings into sequence of 1 to 3
        # characters instead of word tokens
        vectorizer = TfidfVectorizer(ngram_range=(1, 3), analyzer='char', use_idf=True)

        pipeline = Pipeline([
            ('vect', vectorizer),
            ('clf', LinearSVC()),
        ])

        # Fit pipeline to training data
        pipeline.fit(X, y)

        # While loop handling input
        while add_to_training_while != 1:
            training_verified = input("Would you like to add these headers to the machine learning training? (y/n) ")
            if training_verified == "y":
                print("Predicted headers will be added to the machine learning training.")
                add_to_training_decision = True
                add_to_training_while = 1  # End loop
            elif training_verified == "n":
                print("Predicted headers will NOT be added to the machine learning training.")
                add_to_training_while = 1  # End loop
            else:
                print("Please enter either \"y\" for yes or \"n\" for no.")  # Retry for input

        print("Finished initializing machine learning module.")

        # Get mailing date as input from user
        mail_date = input(
            "Enter the mailing date of this job(format is \"Month Day Year\" with no comma after day): ")

        print("Now combining jobs...")

        # Read input excel file
        sheets_dict = pd.read_excel(input_file, sheet_name=None)

        # Create text file to display job counts
        # count_file = open(file_name + "_Counts.txt", "w+")

        # Create xlsx file to display job counts
        workbook = xlsxwriter.Workbook(file_name + '_Counts.xlsx')
        worksheet = workbook.add_worksheet()

        # Format some columns to make the text clearer.
        worksheet.set_column('A:A', 15)
        worksheet.set_column('C:C', 17)
        worksheet.set_column('D:D', 7)
        worksheet.set_column('E:E', 5)
        worksheet.set_column('F:F', 21)

        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': True})

        # Add an outline to be used to check off steps
        check = workbook.add_format({'border': 2})

        # Add a yellow fill to be used to mark final count
        yellow_fill = workbook.add_format({'bg_color': 'FFFF00'})

        # Add a header to the Excel Count File
        worksheet.write(0, 0, "ATS " + mail_date, bold)

        # Iterate through all the sheets in the input file
        for name, sheet in sheets_dict.items():
            # Append given columns to training excel table
            if add_to_training_decision:
                temp_training_df['Given_Header'] = list(sheet.columns)
            # Use machine learning to approximate the column names
            columns_predicted = pipeline.predict(list(sheet.columns))
            sheet.columns = list(columns_predicted)
            if add_to_training_decision:
                # Append predicted columns to training excel table
                temp_training_df['Adjusted_Header'] = ""
                temp_training_df['Predicted_Header'] = list(sheet.columns)
                new_training_table = new_training_table.append(temp_training_df, sort=False)
                # Clear temporary dataframe
                temp_training_df.drop(temp_training_df.index, inplace=True)

            # Add sheet's name as a column in table
            sheet['Sheet'] = name

            # Rename each sheet
            sheet = sheet.rename(columns=lambda x: x.split('\n')[-1])

            # Detect the current working directory
            current_path = os.getcwd()

            # Define the name of the directory to be created
            path = current_path + "/" + name

            # Make a folder for the tables once separated
            try:
                os.mkdir(path)
            except OSError:
                print("Creation of the directory %s failed" % path)
            else:
                print("Successfully created the directory %s " % path)

            # Add a seed to each individual data list
            sheet = sheet.append({'First': 'Joey', 'Last': 'Spero', 'Fullname': 'Joey Spero',
                                  'Address': '908 N Hollywood Way', 'City': 'Burbank', 'St': 'CA', 'Zip': 91505,
                                  'Filingdate': pd.to_datetime('today'), 'County': 'Los Angeles',
                                  'Respondby': pd.to_datetime('today'), 'Sheet': name}, ignore_index=True)

            # Write chart to Excel Count File
            worksheet.write(sheet_counter, 0, name, bold)
            worksheet.write(sheet_counter + 1, 0, "Initial Count")
            worksheet.write(sheet_counter + 1, 1, len(sheet))
            worksheet.write(sheet_counter + 2, 0, "Invalid Zips")
            worksheet.write(sheet_counter + 2, 1, 0)
            worksheet.write(sheet_counter + 3, 0, "Character Length")
            worksheet.write(sheet_counter + 3, 1, 0)
            worksheet.write(sheet_counter + 4, 0, "Non Printables")
            worksheet.write(sheet_counter + 4, 1, 0)
            worksheet.write(sheet_counter + 5, 0, "No Address")
            worksheet.write(sheet_counter + 5, 1, 0)
            worksheet.write(sheet_counter + 6, 0, "No First or Last")
            worksheet.write(sheet_counter + 6, 1, 0)
            worksheet.write(sheet_counter + 7, 0, "Dupes")
            worksheet.write(sheet_counter + 7, 1, 0)
            worksheet.write(sheet_counter + 8, 0, "Final Count", bold)
            # worksheet.write(sheet_counter + 8, 1, "=SUM(INDIRECT(ADDRESS(" + str((sheet_counter + 2)) +
            #                ",2)):INDIRECT(ADDRESS(" + str((sheet_counter + 8)) + ",2)))")
            worksheet.write(sheet_counter + 8, 1,
                            "=SUM(B" + str(sheet_counter + 2) + ":B" + str((sheet_counter + 8)) +
                            ")")
            worksheet.write(sheet_counter + 1, 2, "Sent Approval")
            worksheet.write(sheet_counter + 1, 3, "", check)
            worksheet.write(sheet_counter + 2, 2, "Received Approval")
            worksheet.write(sheet_counter + 2, 3, "", check)
            worksheet.write(sheet_counter + 3, 2, "Start Printing")
            worksheet.write(sheet_counter + 3, 3, "", check)
            worksheet.write(sheet_counter + 4, 2, "Finished Printing")
            worksheet.write(sheet_counter + 4, 3, "", check)
            # final_count_string += "INDIRECT(ADDRESS(" + str((sheet_counter + 9)) + ",2)),"
            final_count_string += "B" + str((sheet_counter + 9)) + ","
            sheet_counter += 10

            # Iterate total count with each sheet count
            total_count += (len(sheet))

            # Append each table to the final table
            full_table = full_table.append(sheet, sort=False)

        # Write Final counts chart to Excel Count File
        worksheet.write(1, 5, "Total Initial Count", bold)
        worksheet.write(1, 6, total_count)
        worksheet.write(2, 5, "Total Final Count", bold)
        worksheet.write(2, 6, "=SUM(" + final_count_string + ")", yellow_fill)
        worksheet.write(3, 5, "Total Records Removed", bold)
        worksheet.write(3, 6, "=G2-G3")
        workbook.close()

        # Reset the index of the final table
        full_table.reset_index(inplace=True, drop=True)

        # Format Date fields
        full_table['Filingdate'] = pd.to_datetime(full_table['Filingdate'], errors='coerce')
        full_table['Filingdate'] = full_table['Filingdate'].dt.strftime('%m/%d/%Y')
        full_table['Respondby'] = pd.to_datetime(full_table['Respondby'], errors='coerce')
        full_table['Respondby'] = full_table['Respondby'].dt.strftime('%m/%d/%Y')

        # Format Phone Field
        full_table['Phone'] = full_table['Phone'].astype(str).apply(
            lambda x: np.where((len(x) >= 10) & set(list(x)).issubset(list('.0123456789')),
                               '1(' + x[:3] + ')' + x[3:6] + '-' + x[6:10],
                               x))
        full_table.replace("nan", "", inplace=True)

        # Set mail date to previous user input
        full_table['Mail_date'] = mail_date

        print("Exporting table to excel file (CSV)...")
        full_table.to_csv("accuzip_importCSV.csv", index_label="count")  # Export to CSV

        if add_to_training_decision:
            training_df_output = training_df.append(new_training_table)
            training_df_output.to_csv(training_file, index=False)

    # File is not found
    else:
        print("File not found. Please make sure the file is a XLSX")

    print("Script is finished.")
    input("Press enter to stop the script.")
