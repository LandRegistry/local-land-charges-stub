# This entire file is a shim that allows existing dev-env, Puppet and S2I set ups to continue functioning in the
# absence of flask-script. Please prefer using the flask commands over manage.py based commands.
import subprocess  # nosec
import sys


def run():
    subprocess.call(["flask", "run"])  # nosec


# If the application manages a database, uncomment the following code block.

# def db():
#     if len(sys.argv) <= 2:
#         raise Exception("db expects a sub-command")

#     sub_command = sys.argv[2]
#     if sub_command == "init":
#         init()
#     elif sub_command == "migrate":
#         migrate()
#     elif sub_command == "upgrade":
#         upgrade()
#     elif sub_command == "downgrade":
#         downgrade()
#     else:
#         print("sub-command '{}' unknown".format(sub_command))


# def init():
#     subprocess.call(['flask', 'db', 'init'])  # nosec


# def migrate():
#     subprocess.call(['flask', 'db', 'revision', '--autogenerate'])  # nosec


# def upgrade():
#     try:
#         subprocess.check_output(['flask', 'db', 'upgrade', 'head'])  # nosec
#     except subprocess.CalledProcessError as grepexc:
#         sys.exit(grepexc.returncode)


# def downgrade():
#     subprocess.call(['flask', 'db', 'downgrade'])  # nosec


if __name__ == "__main__":
    # This shim doesn't import anything from the application, so has no logger configuration.
    # Print warnings to STDOUT.
    print("WARNING: use of manage.py is deprecated")
    if len(sys.argv) <= 1:
        raise Exception("Please specify a command")

    command = sys.argv[1]

    if command == "runserver":
        run()
    # If the application manages a database, uncomment the following code block.
    # elif if command == "db":
    #     db()
    else:
        raise Exception("Command unknown")
