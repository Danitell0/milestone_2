#!/usr/bin/env python3

def secure_archive(file: str, action: str="", content: str="") -> tuple[bool, str]:
    try:
        with open(file, action) as in_file:
            if action == "r":
                read_content = in_file.read()
                print(read_content)
            



        if action == "w":
            with open(file, "w") as in_file:
                in_file.write(content)
            return (True, "Content sucessfully written to file")
        elif action == "r":
            with open(file, "r") as in_file:
                read_content = in_file.read()
            return (True, read_content)
    except Exception as e:
        return (False, str(e))


def main() -> None:
    print("=== Cyber Archives Security ===")

    test1 = secure_archive("text.txt", "r")
    print (test1)


if __name__ == "_main__":
    main()
