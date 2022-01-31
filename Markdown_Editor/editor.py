
class MarkdownEditor:
    """ A class functioning as a Markdown editor. Input text is converted to Markdown formatting"""
    
    def __init__(self):
        self.available_formatters = {
            "plain": self.plain,
            "bold": self.bold,
            "italic": self.italic,
            "header": self.header,
            "link": self.link,
            "inline-code": self.inline_code,
            "new-line": self.new_line,
            "ordered-list": self.ordered_list,
            "unordered-list": self.unordered_list
        }
        self.special_commands = ["!help", "!done"]
        self.accumulated_text = []

    def plain(self):
        text = input("Text: ")
        self.accumulated_text.append(text)
    
    def bold(self):
        text = input("Text: ")
        bold_text = f"**{text}**"
        self.accumulated_text.append(bold_text)
    
    def italic(self):
        text = input("Text: ")
        italic_text = f"*{text}*"
        self.accumulated_text.append(italic_text)
    
    def header(self):
        while True:
            level = int(input("Level: "))
            if not 1 <= level <= 6:
                print("The level should be within the range of 1 to 6")
            else:
                break
        text = input("Text: ")
        header_text = f"{'#' * level} {text}\n"
        self.accumulated_text.append(header_text)
    
    def link(self):
        label = input("Label: ")
        url = input("URL: ")
        link_text = f"[{label}]({url})"
        self.accumulated_text.append(link_text)
    
    def inline_code(self):
        text = input("Text: ")
        inline_code_text = f"`{text}`"
        self.accumulated_text.append(inline_code_text)
    
    def new_line(self):
        new_line_text = "\n"
        self.accumulated_text.append(new_line_text)
    
    def ordered_list(self):
        while True:
            number_of_rows = int(input("Number of rows: "))
            if number_of_rows <= 0:
                print("The number of rows should be greater than zero")
            else:
                break
        for n in range(number_of_rows):
            row = input(f"Row #{n + 1}: ")
            row_text = f"{n + 1}. {row}\n"
            if n + 1 == 1:
                try:
                    if self.accumulated_text[-1][-1] != "\n":
                        row_text = f"\n{row_text}"
                except IndexError:
                    pass
            self.accumulated_text.append(row_text)
    
    def unordered_list(self):
        while True:
            number_of_rows = int(input("Number of rows: "))
            if number_of_rows <= 0:
                print("The number of rows should be greater than zero")
            else:
                break
        for n in range(number_of_rows):
            row = input(f"Row #{n + 1}: ")
            row_text = f"* {row}\n"
            if n + 1 == 1:
                try:
                    if self.accumulated_text[-1][-1] != "\n":
                        row_text = f"\n{row_text}"
                except IndexError:
                    pass
            self.accumulated_text.append(row_text)
    
    def save_text(self):
        with open("output.md", "w") as output_file:
            output_file.writelines("".join(self.accumulated_text))


def main():
    md_editor = MarkdownEditor()
    available_formatters = md_editor.available_formatters
    while True:
        formatter = input("Choose a formatter: ")
        if formatter in available_formatters:
            available_formatters[formatter]()
            print("".join(md_editor.accumulated_text))
        elif formatter == "!help":
            formatters = " ".join(available_formatters.keys())
            commands = " ".join(md_editor.special_commands)
            print(f"Available formatters: {formatters}\nSpecial commands: {commands}")
        elif formatter == "!done":
            md_editor.save_text()
            exit()
        else:
            print("Unknown formatting type or command")


if __name__ == "__main__":
    main()
