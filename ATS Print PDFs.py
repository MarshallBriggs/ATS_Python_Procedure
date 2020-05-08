# Import PyPDF2 to print pdfs
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject


def extract_information(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()

    txt = f"""
    Information about {pdf_path}: 

    Author: {information.author}
    Creator: {information.creator}
    Producer: {information.producer}
    Subject: {information.subject}
    Title: {information.title}
    Number of pages: {number_of_pages}
    """

    print(txt)
    return information


def split(path, name_of_split):
    pdf = PdfFileReader(path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))

        output = f'{name_of_split}{page}.pdf'
        with open(output, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)
        # USE THIS FUNCTION
        # path = 'Jupyter_Notebook_An_Introduction.pdf'
        # split(path, 'jupyter_page')


def get_first_three(path, name_of_split):
    pdf = PdfFileReader(path)
    # pdf_writer = PdfFileWriter()
    for page in range(pdf.getNumPages()):
        if page == 3:
            break
        pdf_writer.addPage(pdf.getPage(page))
    # output = f'{name_of_split}.pdf'
    # with open(output, 'wb') as output_pdf:
        # pdf_writer.write(output_pdf)


# Corrects an error with the form fillable fields
def set_need_appearances_writer(writer: PdfFileWriter):
    # See 12.7.2 and 7.7.2 for more information: http://www.adobe.com/content/dam/acom/en/devnet/acrobat/pdfs/PDF32000_2008.pdf
    try:
        catalog = writer._root_object
        # get the AcroForm tree
        if "/AcroForm" not in catalog:
            writer._root_object.update({
                NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)
            })

        need_appearances = NameObject("/NeedAppearances")
        writer._root_object["/AcroForm"][need_appearances] = BooleanObject(True)
        # del writer._root_object["/AcroForm"]['NeedAppearances']
        return writer

    except Exception as e:
        print('set_need_appearances_writer() catch : ', repr(e))
        return writer


if __name__ == "__main__":

    # Import OS to walk through directory
    import os

    # Get the path of this python file
    my_path = os.path.dirname(os.path.abspath(__file__))

    # Initialize file variables
    found_file = False
    input_path = ""
    input_file = ""
    file_name = ""
    folder_name = ""
    cwd = ""

    # Initialize count variables
    eDoc_count = 0

    # Initialize pdf writer
    pdf_writer = PdfFileWriter()
    set_need_appearances_writer(pdf_writer)

    for root, dirs, files in os.walk(my_path):
        for file in files:
            if file.endswith(".pdf"):
                input_path = root
                input_file = file
                file_name = os.path.splitext(input_file)[0]
                # print(os.path.join(root, file))
                if file_name == "eDocumentation":
                    path = os.path.join(root, file)
                    # extract_information(path)
                    cwd = os.getcwd()
                    # print(cwd)
                    # print(os.path.dirname(path))
                    # print(os.path.basename(path))
                    folder_name = os.path.split(os.path.dirname(path))[-1]
                    pdf = PdfFileReader(path)
                    for page in range(pdf.getNumPages()):
                        if page == 3:
                            break
                        pdf_writer.addPage(pdf.getPage(page))
                    # get_first_three(path, folder_name)
                    eDoc_count += 1

    if input_file == "":
        found_file = False
    else:
        found_file = True

    # File is found
    if found_file:
        output = f'{os.path.basename(my_path)}_eDocumentation_Combined.pdf'
        with open(output, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)
        print("Found " + str(eDoc_count) + " instance(s) of eDocumentation.pdf")
    # File is not found
    else:
        print("File not found. Please make sure the file is present in folders")

    print("Script is finished.")
    input("Press enter to stop the script.")
