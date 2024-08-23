from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from pypdf import PdfReader

def GUI():
    def upload_file():
        global article
        # article = ""
        # Function to handle file upload
        filename = filedialog.askopenfilename(
            initialdir=".",
            title="Select A File",
            filetypes=(("All files", "*.*"), ("Text files", "*.txt"), ("PDF files", "*.pdf"))
        )
        if filename:
            file_label.config(text=f"File selected: {filename}")
            print(f"File selected: {filename}")
        # mylabel = Label(file_frame, text=filename, font=('Arial',12)).pack()
        filelist = filename.split('/')
        ext = filelist[-1].split('.')
        # print(ext)
        if ext[-1] == "pdf":
            reader = PdfReader(f'{filename}') 
            article = ""
            for i in range(len(reader.pages)):
                page = reader.pages[i]
                article += page.extract_text()
            
        elif ext[-1] == "txt":
            f = open(f"{filename}", "r")
            article = ""
            article = f.read()
            # print(len(article))
        else:
            print("Filetype Not Supported")
        # print(len(article))

    def submit_text():
        # Function to handle text submission
        text_data = text_input.get(1.0, END).strip()  # Get text and strip newline characters
        text_label.config(text=f"Text submitted: {text_data[:50]}...")  # Show first 50 chars for brevity
        print(f"Submitted text: {text_data}")

    # Create the main window
    # article = ""
    window = Tk()
    window.title("Text Input and File Upload")
    window.geometry('600x500')

    # Create frames for layout
    input_frame = ttk.Frame(window, padding="10")
    input_frame.pack(fill='both', expand=True)

    file_frame = ttk.Frame(window, padding="10")
    file_frame.pack(fill='both', expand=True)

    # Text input section
    text_label = Label(input_frame, text='Enter your text:', font=('Arial', 16))
    text_label.pack(pady=5)

    text_input = Text(input_frame, width=70, height=10, font=('Arial', 12))
    text_input.pack(pady=5)

    submit_button = Button(input_frame, text='Submit Text', command=submit_text, font=('Arial', 12))
    submit_button.pack(pady=10)

    text_label = Label(input_frame, text="", font=('Arial', 12))
    text_label.pack(pady=5)

    # File upload section
    upload_button = Button(file_frame, text="Upload File", command=upload_file, font=('Arial', 12))
    upload_button.pack(pady=10)

    file_label = Label(file_frame, text="", font=('Arial', 12))
    file_label.pack(pady=5)

    # Start the Tkinter event loop
    window.mainloop()
    return article
ar = GUI()
# print(ar)