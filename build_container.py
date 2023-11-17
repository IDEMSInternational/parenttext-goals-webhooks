import subprocess

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
        "pt-goals-api:0.1.0",
    ]
)
