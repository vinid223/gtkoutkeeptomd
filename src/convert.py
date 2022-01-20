import errno
import json
import os
from os import walk
import argparse
import logging
import textwrap


def load_json_file(path: str):
    f = open(path, "r")
    data = f.read()
    f.close()

    return json.loads(data)


def save_markdown_file(path: str, data):
    f = open(path, "w")
    f.writelines(data)
    f.close()


def convert_list_content(list_content):
    data = ""
    for item in list_content:
        checked = "x" if item["isChecked"] else " "
        text = item["text"]
        data = data + f"- [{checked}] {text}\n"

    return data


def convert_to_markdown(json_data, note_name):
    archived = json_data["isArchived"]
    data = f"# {note_name}\n\n"

    if "listContent" in json_data:
        data = data + convert_list_content(json_data["listContent"])

    if "textContent" in json_data:
        data = data + json_data["textContent"]

    return archived, data


def set_path_to_file_names(dir, filenames):
    new_files = []
    for file in filenames:
        new_files.append(os.path.join(dir, file))

    return new_files


def get_folder_files(path, recursive):
    dirpath, dirnames, filenames = next(walk(path), (None, None, []))
    filenames = set_path_to_file_names(path, filenames)
    if recursive and dirnames:
        for dir in dirnames:
            filenames = filenames + get_folder_files(os.path.join(path, dir), recursive)

    return filenames


def convert_file(
    input,
    output=None,
    archived=False,
    archivedoutput=None,
    from_folder=False,
    force_file=False,
):
    print(f"\n\nConverting file {input}")
    file_name, extension = os.path.splitext(os.path.basename(input))

    if extension != ".json" and not force_file:
        print(
            "Skipping file, not json format. Use flag --force to force the file to be used. WARNING: This script may throw an error."
        )
        return

    json_data = load_json_file(input)
    note_name = json_data["title"] if json_data["title"] else file_name
    note_archived, markdown = convert_to_markdown(json_data, note_name)
    print(f"Archived: {note_archived}")
    print(f"Note name: {note_name}")
    print(f"File name: {file_name}")
    if from_folder:
        archive = "archived" if archived and note_archived else ""
        archive = archivedoutput if archivedoutput and archived else archive
        output_file = os.path.join(output, archive, f"{note_name}.md")
    else:
        output_file = output if output else f"{note_name}.md"

    print(f"Outputing file to {output_file}")
    save_markdown_file(output_file, markdown)


def convert_folder(
    path,
    recursive=False,
    output=None,
    archived=False,
    archivedoutput=None,
    force_file=False,
):
    filenames = get_folder_files(path, recursive)

    for file in filenames:
        try:
            convert_file(file, output, archived, archivedoutput, True, force_file)
        except Exception as e:
            print(f"Error converting file: {file}")
            logging.error(e)


description_lines = [
    "Convert Google Takeout Keep files to Markdown",
    "",
    "\tconvert.py --input some_exported_file.json --output converted.md",
    "",
    "\tconvert.py --input /path/to/input --output /path/to/output -r",
]

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
        """\
         Convert Google Takeout Keep files to Markdown.
         ----------------------------------------------
             convert.py -i some_exported_file.json --o converted.md
             convert.py -i /path/to/input -o /path/to/output -r -a
         """
    ),
)
parser.add_argument(
    "-i",
    "--input",
    dest="input",
    type=str,
    required=True,
    help="Path to input file or directory.",
)
parser.add_argument(
    "-o", "--output", dest="output", type=str, help="Path to output file or directory."
)
parser.add_argument(
    "-r",
    "--recursive",
    dest="recursive",
    action="store_true",
    help="Directory only. Enable recursive convertion for directories. Not used for individual files. The subdirectories structures will be lost in the output folder.",
)
parser.add_argument(
    "-a",
    "--archived",
    dest="archived",
    action="store_true",
    help='Directory only. Separate archived notes to a separate directory. Default directory "archived"',
)
parser.add_argument(
    "-f",
    "--force",
    dest="force_file",
    action="store_true",
    help="Force the file to be read if the extension is not .json. This may break the conversion.",
)
parser.add_argument(
    "--archivedoutput",
    dest="archivedoutput",
    type=str,
    help="Path to archived output directory.",
)


if __name__ == "__main__":
    args = parser.parse_args()
    if os.path.isdir(args.input):

        if args.output:
            try:
                os.mkdir(args.output)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
                pass

        if args.archived:
            archive_path = (
                os.path.join(args.output, args.archivedoutput)
                if args.archivedoutput
                else os.path.join(args.output, "archived")
            )
            try:
                print(f"Making dir {archive_path}")
                os.mkdir(archive_path)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
                pass

        convert_folder(
            args.input,
            args.recursive,
            args.output,
            args.archived,
            args.archivedoutput,
            args.force_file,
        )

    elif os.path.isfile(args.input):
        if args.recursive:
            print("Recursive flag will be ignored. Input not a folder.")

        convert_file(args.input, args.output)

    else:
        parser.error("The input parameter is not a folder or usable file")
