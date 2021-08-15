# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
from pathlib import Path

import DataFetcher

current_class = ""

class_fields = {}
class_methods = {}
class_constructors = []
export = {}

class_spigot_mappings = {}
method_spigot_mappings = {}
class_mc_to_spigot = {}


def _map_classname(classname):
    return class_mc_to_spigot[classname].replace("/", ".") if classname in class_mc_to_spigot.keys() else "_"


def parse_arguments(arguments):
    args = []
    reading_class = False
    array = False
    clazz = ""
    for char in arguments:
        if reading_class:
            if char == ';':
                args.append(clazz.replace("/", "."))
                reading_class = False
                clazz = ""
                continue
            clazz = clazz + char
            continue
        elif char == 'D':
            char = "double"
        elif char == 'F':
            char = "float"
        elif char == 'I':
            char = "int"
        elif char == 'S':
            char = "short"
        elif char == 'B':
            char = "byte"
        elif char == 'J':
            char = "long"
        elif char == 'Z':
            char = "boolean"
        elif char == "V":
            char = "void"
        elif char == "C":
            char = "char"
        elif char == "[":
            array = True
            continue
        elif not char == 'L':
            print("Unknown char {} from {}".format(char, arguments))
            continue
        else:
            reading_class = True
            continue

        if array:
            array = False
            args.append("{}[]".format(char))
            continue
        args.append(char)

    return args


def map_classname(old_classname):
    _classname = _map_classname(old_classname)
    new_classname = old_classname if _classname == "_" else _classname
    if ":" in new_classname:
        new_classname = new_classname[new_classname.rindex(":") + 1:]
    if "." not in new_classname and new_classname != "float" and new_classname != "byte" and new_classname != "int" and \
            new_classname != "double" and new_classname != "long" and new_classname != "short" \
            and new_classname != "char":
        return "new.minecraft.server.{}".format(new_classname)
    return new_classname


def initialise_spigot(bukkit, bukkit_methods):
    with open(bukkit, 'r') as f:
        for line in f.readlines():
            line = line.replace("\n", "")
            if line.startswith("#"):
                continue
            info = line.split(" ")
            class_spigot_mappings[info[0]] = info[1]
    with open(bukkit_methods, 'r') as f:
        for line in f.readlines():
            line = line.replace("\n", "")
            if line.startswith("#"):
                continue
            info = line.split(" ")
            class_name = info[0].replace("/", ".")

            if "(" not in line:  # Skip over fields as we already know what's new
                continue
            args = parse_arguments(info[2][1:info[2].index(")")])

            if class_name in method_spigot_mappings.keys():
                array = method_spigot_mappings[class_name]
                array.append([info[1], args, info[3]])
                method_spigot_mappings[class_name] = array
            else:
                method_spigot_mappings[class_name] = [[info[1], args, info[3]]]


def initialise_mc(mojang):
    with open(mojang) as f:
        for line in f.readlines():
            line = line.replace("\n", "").replace(":", "")
            if line.startswith("#") or line.startswith("    "):
                continue

            class_details = line.split(" -> ")
            if class_details[1] in class_spigot_mappings.keys():
                class_name = class_spigot_mappings[class_details[1]]
            else:
                class_name = class_details[0]

            class_mc_to_spigot[class_details[0]] = class_name.replace("/", ".")


def start(bukkit, bukkit_members, mojang, ex, docfile, version):
    initialise_spigot(bukkit, bukkit_members)
    initialise_mc(mojang)
    global current_class, class_fields, class_methods, export, class_constructors

    exportfile = open(ex, 'w')
    document = open(docfile, 'w')
    document.write("<html><head><title>{} Docs</title></head><body>".format(version))
    num = 0
    with open(mojang) as f:

        for line in f.readlines():
            num += 1

            line = line.replace("\n", "")
            if line.startswith("#"):
                continue

            if not (current_class == "") and line.startswith("    "):
                args = line[4:].split(" ")
                if '(' in line:
                    return_type = map_classname(args[0])
                    function = args[1]
                    function_name = function[:function.index("(")]
                    if ":" in function_name:
                        function_name = function_name[function.rindex(":") + 1:]
                    obfuscated_name = args[3]

                    function_arguments = function[function.index("(") + 1:function.index(")")].split(",")
                    if function_arguments[0] == "":
                        function_arguments = ["_"]

                    if '<clinit>' in function:  # not sure what clinit is tbh
                        continue
                    if '<init>' in function:
                        class_constructors.append({"a": function_arguments})
                        continue

                    spigot_mapping = method_spigot_mappings[map_classname(current_class)]
                    found = False
                    for _method in spigot_mapping:
                        if not _method[0] == obfuscated_name:
                            continue
                        if _method[1] == function_arguments:
                            found = True

                    if not found:
                        continue

                    class_methods[function_name] = {"t": return_type, "o": obfuscated_name,
                                                    "a": function_arguments}
                    continue

                field_type = map_classname(args[0])
                field_name = args[1]
                obfuscated_name = args[3]

                class_fields[field_name] = {"t": field_type, "o": obfuscated_name}
                continue

            if not current_class == "":
                exportfile.write("{}\n".format(map_classname(current_class)))
                document.write("<h2>{}</h2>".format(map_classname(current_class)))

                document.write("<h3>Fields</h3>")
                for field in class_fields:
                    f = class_fields[field]
                    exportfile.write("  {} {} {}\n".format(f['t'], field, f['o']))
                    exportfile.flush()
                    document.write("<span><strong>{} ({})</strong> - Returns {}</span><br>".format(field, f['o'], f['t']))
                    document.flush()
                document.write("<h3>Methods</h3>")
                for method in class_methods:
                    m = class_methods[method]
                    exportfile.write("  {} {} {} {}\n".format(m['t'], method, ",".join(m['a']), m['o']))
                    exportfile.flush()
                    document.write(
                        "<span><strong>{} ({})</strong> - Returns {}</span><br><strong>Arguments</strong> - {}<br><br>".format(
                            field, f['o'], f['t'], ",".join(m['a'])))
                    document.flush()
                for constructor in class_constructors:
                    exportfile.write("  _ {}\n".format(",".join(constructor['a'])))
                    exportfile.flush()
                exportfile.flush()
                document.flush()
            class_fields = {}
            class_methods = {}
            class_constructors = []

            class_details = line.split(" -> ")
            current_class = class_details[0]

            if map_classname(current_class) not in method_spigot_mappings.keys():
                current_class = ""

    document.write("</body></html>")
    document.flush()
    document.close()
    exportfile.close()


if __name__ == '__main__':
    Path("sources").mkdir(exist_ok=True)
    Path("out").mkdir(exist_ok=True)
    Path("docs").mkdir(exist_ok=True)

    DataFetcher.fetch_all()
    print("Starting mapping process...")
    for x in DataFetcher.MINECRAFT_VERSIONS:
        start("sources/{}-class.s_".format(x), "sources/{}-method.s_".format(x), "sources/{}-all.m_".format(x),
              "out/{}.map".format(x), "docs/{}.html".format(x), x)
        print("Created map for {} :))".format(x))
