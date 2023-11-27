import subprocess
import sys


image_tag = sys.argv[1]

subprocess.run(
    [
        "pack",
        "build",
        "--builder",
        "gcr.io/buildpacks/builder:v1",
        "--env",
        "GOOGLE_FUNCTION_SIGNATURE_TYPE=http",
        "--env",
        "GOOGLE_FUNCTION_TARGET=serve",
        image_tag,
    ]
)
