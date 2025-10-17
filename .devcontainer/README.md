Place your corporate interception certificate (for example zscaler.crt) in this folder as `.devcontainer/zscaler.crt` before rebuilding the devcontainer.

Why: The Dockerfile copies `.devcontainer/zscaler.crt` into the image and runs `update-ca-certificates` so that SDKMAN and other tools can download JDKs and packages through your corporate proxy.

If you prefer to keep the cert elsewhere, update `.devcontainer/Dockerfile` and `.devcontainer/devcontainer.json` accordingly.

## Automation helpers

If the Dev Containers extension still injects a COPY for a workspace-root certificate, the build may expect `./zscaler.crt` at the workspace root. Use the helper scripts to automate a temporary workspace-root copy:

1. Prepare the build (temporary copy):

   .devcontainer/prepare-devcontainer-build.sh

   This copies `.devcontainer/zscaler.crt` to `./zscaler.crt` and prints next steps.

2. Rebuild the container in VS Code: Command Palette -> "Dev Containers: Rebuild Container"

3. Clean up the temporary root copy after success:

   .devcontainer/cleanup-devcontainer-build.sh

The scripts are safe: `prepare` will fail if `.devcontainer/zscaler.crt` is missing. `cleanup` simply removes `./zscaler.crt` if present.

## Importing cert into JVM cacerts

After features run (SDKMAN installs the JDK), some Java tools may still reject SSL because the JDK truststore (`cacerts`) isn't updated. We added a post-create script that will attempt to import `.devcontainer/zscaler.crt` into any JDK `cacerts` it can find.

This script runs automatically as part of the `postCreateCommand` and is safe to re-run.

## Quick helper scripts

If the devcontainer build still fails because the extension auto-injects a COPY from the workspace root, use the helper scripts to temporarily copy the cert to the workspace root and clean it up afterward.

Usage:

1. Copy the cert to repo root (temporary):

   .devcontainer/prepare-devcontainer-build.sh

2. Rebuild container in VS Code: Command Palette -> Dev Containers: Rebuild Container

3. Remove temporary copy after successful build:

   .devcontainer/cleanup-devcontainer-build.sh

These scripts simply automate the temporary copy/remove steps so you don't have to do them by hand.
