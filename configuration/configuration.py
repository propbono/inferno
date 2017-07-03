import os
import sys
#
class Configuration(object):
    #Debug
    DIR = os.path.dirname(sys.argv[0])
    PREPPED_FILES_DIR = os.path.join(DIR, "Debug")
    OUTPUT_DIR = os.path.join(PREPPED_FILES_DIR, "OUT")
    INPUT_DIR = os.path.join(PREPPED_FILES_DIR, "IN")
    FILES_TO_PROCESS = [f for f in os.listdir(INPUT_DIR) if f.endswith(".mxml")]

    #Working
    # DIR = os.path.dirname(sys.argv[0])
    # PREPPED_FILES_DIR = "N:\\"
    # OUTPUT_DIR = os.path.join(PREPPED_FILES_DIR, "OUT")
    # INPUT_DIR = os.path.join(PREPPED_FILES_DIR, "IN")
    # FILES_TO_PROCESS = [f for f in os.listdir(INPUT_DIR) if f.endswith(".mxml")]
