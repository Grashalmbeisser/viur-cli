import click, os, shutil
from . import cli, echo_error, get_config


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("action")
@click.argument("name", default="")
@click.argument("additional_args", nargs=-1)
def flare(action, name, additional_args):
    """build or watch a flare frontend"""
    projectConfig = get_config()
    additional_args = list(additional_args)

    if action == "release":
        if shutil.which("zip") is None:
            echo_error(f'Please install "zip" to bundle a flare application.')
            return

        additional_args = ["-mzc"]
    elif action == "debug":
        pass
    elif action == "watch":
        additional_args = ["-w"]

    if not name:
        if len(projectConfig["default"]["flare"]) == 0:
            echo_error(f"No flare app configured")
        else:
            name = list(projectConfig["default"]["flare"].keys())[0]

    elif name not in projectConfig["default"]["flare"]:
        echo_error(f"{name} is not a valid flare app name.")
        return

    conf = projectConfig["default"].copy()

    os.system(
        f'flare -n={name} -s={conf["flare"][name]["source"]} -t={conf["flare"][name]["target"]} {" ".join(additional_args)}')
