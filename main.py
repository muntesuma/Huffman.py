

def copy_message():
    link_code_txt = open("code.txt", "rt", encoding = "utf-8-sig")
    for str_code in link_code_txt:
        print(str_code)
    link_code_txt.close()
    return str_code

def main():
    str_code = copy_message();
    print(str_code)

main()
