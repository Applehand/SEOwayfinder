from flask import render_template
from cli.commands import handle_get_command


def show_project_report(project_name):
    """
    Fetch the project data and render it using an HTML template.

    Args:
        project_name (str): The name of the project to fetch data for.

    Returns:
        Rendered HTML or error page.
    """
    pages = handle_get_command(project_name)

    return render_template('report_template.html', project_name=project_name, pages=pages)
