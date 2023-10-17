import subprocess
import pkg_resources

try:
    # Get a list of installed packages
    installed_packages = [pkg.key for pkg in pkg_resources.working_set]

    # Create the requirements.txt file
    with open('requirements.txt', 'w') as file:
        for package in installed_packages:
            try:
                # Get the package version
                package_version = subprocess.check_output(['pip', 'show', package]).decode().split('\n')[1].split(': ')[1].strip()

                # Write the package and version to requirements.txt
                file.write(f"{package}=={package_version}\n")
            except Exception as e:
                print(f"An error occurred while processing {package}: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
