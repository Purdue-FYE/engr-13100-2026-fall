import json
import unittest

from generic_grader.utils.file_set_up import file_set_up
from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner
from post import post_processor as pp
from tests.test_config import file_set_up_options

if __name__ == "__main__":
    with open("../results/results.json", "w+") as f:
        with file_set_up(file_set_up_options):
            attempts = 1
            while attempts < 5:
                suite = unittest.TestLoader().discover("tests")
                JSONTestRunner(visibility="visible", stream=f, post_processor=pp).run(
                    suite
                )
                current_attempt = attempts
                f.seek(0)
                json_data = json.load(f)
                f.seek(0)
                f.truncate()
                tests = json_data["tests"]
                for test in tests:
                    if (
                        "Check for submission of required files" in test["name"]
                        and test["status"] == "failed"
                    ):
                        """If the file is not found, break out of the loop."""
                        attempts = current_attempt
                        break
                    output = test.get("output", "")
                    if "ModuleNotFound" in output and attempts == current_attempt:
                        """If a ModuleNotFound error is found, increase the number of attempts."""
                        attempts += 1

                if attempts == current_attempt:
                    """If no new errors were found, break out of the loop."""
                    break
        for test in tests:
            """Append the number of attempts to the output of TestFilePresence."""
            if "Check for submission of required files" in test["name"]:
                test["output"] += f"\nAttempts: {attempts}"
                break
        """Remove the old data and write the new data to the file.""" ""
        json.dump(json_data, f, indent=4)
