"""
This is a program to test a single task. It accepts a single argument - 
the task code.
First it will call get_lab_filenames.py from tests directory
to obtain a mapping from task codes to test filenames in tests directory.
It will then copy filename(s) for the task given as runtime argument
to the student repo dir, optionally make that dir a node package, 
and run npm install and npm test against the tests. 
"""

import sys, shutil, os, logging, subprocess

NODE_PACKAGE_ROOT = '../lab'
TESTS_DESTINATION = 'test'

logging.basicConfig(
    level=logging.INFO, 
    format='%(levelname)s:%(message)s'
)

TROOT, PROOT, TDEST = map(os.path.abspath, 
                          (
                           './tests', 
                           NODE_PACKAGE_ROOT, 
                           os.path.join(NODE_PACKAGE_ROOT, TESTS_DESTINATION)
                          )
                      )

if 1:#try:
    # Find out the test filename(s)
    if 1:# try:
        if len(sys.argv)!=2:
            raise Exception("Must pass exactly one task key to test")
        the_task = sys.argv[1]
        from tests.get_lab_filenames import get_lab_filenames
        tests = get_lab_filenames(PROOT)
        test_filenames = tests[the_task]
    # except ImportError:
    #     raise Exception("Cannot find the mapper from repo name to test filenames")
    # except Exception as e:
    #     raise Exception(f"Task {the_task} not found")

    # Assume that the first result after replacing ("run-"->"arr-"), 
    # gives solution name. Check that it exists, otherwise nothing to do
    if type(test_filenames) == str:
        test_filenames = [test_filenames]
    solution_filename = test_filenames[0].replace('run-', 'arr-')
    if not os.path.isfile(os.path.join(PROOT, solution_filename)):
        raise Exception(f"Файл решения {solution_filename} НЕ НАЙДЕН")

    try:
        if os.path.isfile(TDEST):
            os.unlink(TDEST)
        if not os.path.isdir(TDEST):
            os.mkdir(TDEST)
    except:
        raise Exception(f"Could not create dir {TDEST}")

    # Copy the test file(s) to test dir
    logging.info(f'Копирую {" ".join(test_filenames)}')
    try:
        for fn in test_filenames:
            shutil.copy(os.path.join(TROOT, fn), TDEST)
    except FileNotFoundError:
        raise Exception(f"No tests found for problem {the_task}")
    except OSError:
        raise Exception(f"Could not copy the test file {fn} to {TDEST}")

    # Go to package dir and install node packages if we have package.json
    os.chdir(PROOT)
    package_json = os.path.join(TROOT, 'package.json')
    copy_npm = os.path.isfile(package_json)
    if copy_npm:
        try:
            shutil.copy(package_json, PROOT)
        except:
            raise Exception(f"Could not copy package.json to {os.path.abspath('.')}")
        try:
            shutil.copy(os.path.join(TROOT, 'package-lock.json'), PROOT)
        except:
            pass
        output = None
        logging.info("Запуск npm install...")
        try:
            output = subprocess.check_output('npm install', stderr=subprocess.STDOUT, shell=True)
        except:
            raise Exception("Could not install packages with npm:{'\n'+out if out else ''}")
    else:
        logging.info("No package.json found in 'tests/'")

    # Run npm test
    logging.info("Запуск npm test:")
    res = subprocess.check_call(['npm', '--silent', 'test'])
    logging.info("РЕЗУЛЬТАТ: тест(ы) пройден(ы)")
    sys.exit(0)

# except subprocess.CalledProcessError as e:
#     logging.error("РЕЗУЛЬТАТ: тест(ы) НЕ пройден(ы)")
#     sys.exit(e.returncode)

# except Exception as e:
#     logging.error(e.args[0])
#     sys.exit(1)