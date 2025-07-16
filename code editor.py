
root = Tk()
root.title("Python editor")

text_editor = Text(root)
text_editor.pack(fill=BOTH, expand=True)

# Create a function to handle opening a file
def open_file():
    file_path = filedialog.askopenfilename()
    with open(file_path, 'r') as file:
        text = file.read()
        text_editor.delete('1.0', END)
        text_editor.insert('1.0', text)

# Create a function to handle saving a file
def save_file():
    file_path = filedialog.asksaveasfilename()
    with open(file_path, 'w') as file:
        text = text_editor.get('1.0', END)
        file.write(text)

# Create a function to run the code
def run_code():
    # Clear any existing error highlighting
    text_editor.tag_remove("error", "1.0", END)

    code = text_editor.get('1.0', END)
    process = subprocess.Popen(['python', '-c', code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = process.communicate()

    # Display the output in a new window
    output_window = Toplevel()
    output_window.title("Output")
    output_text = Text(output_window)
    output_text.pack(fill=BOTH, expand=True)
    output_text.insert('1.0', output.decode("utf-8"))
    output_text.insert(END, errors.decode("utf-8"))

    # Highlight any error messages in the code
    error_lines = [int(line.split(":")[1]) - 1 for line in errors.decode("utf-8").splitlines()]
    for line in error_lines:
        text_editor.tag_add("error", f"{line+1}.0", f"{line+1}.end")
    text_editor.tag_config("error", background="red")

# Create a menu bar
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Create a file menu
file_menu = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Create a run menu
run_menu = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Run", menu=run_menu)
run_menu.add_command(label="Run", command=run_code)

# Create a tag for error highlighting
text_editor.tag_configure("error", background="red")

root.mainloop()
