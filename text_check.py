from datetime import datetime
from os import listdir, makedirs, path
from subprocess import run as proc_run, CalledProcessError

RFC_DIRECTORY = "rfc"
RESULTS_DIRECTORY = "text_results"


def save_xml2rfc_versions(results_dir):
    output = proc_run(
        args=["xml2rfc", "--verbose", "--version"],
        capture_output=True,
    )
    xml2rfc_version_file = path.join(results_dir, "xml2rfc.txt")
    with open(xml2rfc_version_file, "w", newline="") as version:
        version.write(output.stdout.decode("utf-8"))


def compare(rfc_dir, results_dir):
    for filename in [f for f in listdir(rfc_dir) if f.endswith(".xml")]:
        xml_file = path.join(rfc_dir, filename)
        text_file = path.join(rfc_dir, filename.replace(".xml", ".txt"))
        new_text_file = path.join(rfc_dir, filename.replace(".xml", ".new.txt"))
        diff_file = path.join(results_dir, filename.replace(".xml", ".diff.txt"))
        error_file = path.join(results_dir, filename.replace(".xml", ".error.txt"))

        output = proc_run(
            args=["xml2rfc", "--text", "--bom", "--out", new_text_file, xml_file],
            capture_output=True,
        )
        try:
            output.check_returncode()
        except CalledProcessError:
            with open(error_file, "w", newline="") as errors:
                errors.write(output.stderr.decode("utf-8"))
                continue

        output = proc_run(
            args=["diff", "-w", text_file, new_text_file], capture_output=True
        )

        diff = output.stdout.decode("utf-8")
        if len(diff) > 0:
            with open(diff_file, "w", newline="") as diffs:
                diffs.write(diff)


results_dir = f"{RESULTS_DIRECTORY}/{datetime.utcnow().strftime('%Y%m%d')}"
if not path.exists(results_dir):
    makedirs(results_dir)
    save_xml2rfc_versions(results_dir)
    compare(RFC_DIRECTORY, results_dir)
