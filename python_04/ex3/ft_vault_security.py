#!/usr/bin/env python3

def secure_archive(file: str, action: str = "",
                   content: str = "") -> tuple[bool, str]:
    try:
        with open(file, action) as in_file:
            if action == "r":
                read_content = in_file.read()
                return (True, read_content)
            elif action == "w":
                in_file.write(content)
                return (True, "Content successfully written to file")
    except Exception as e:
        return (False, str(e))
    return (False, "mypy satisfier")


def main() -> None:
    print("=== Cyber Archives Security ===\n")

    print("Using 'secure_archive' to read from a nonexistent file:")
    test1 = secure_archive("/not/existing/file", "r")
    print(test1)

    print("Using 'secure_archive' to read from an inaccessible file:")
    test2 = secure_archive("/etc/master.passwd", "r")
    print(test2)

    print("Using 'secure_archive' to read from a regular file:")
    test3 = secure_archive("text.txt", "r")
    print(test3)

    print("Using 'secure_archive' to write previous content to a new file:")
    test4 = secure_archive("new.txt", "w", test3[1])
    print(test4)


if __name__ == "__main__":
    main()
