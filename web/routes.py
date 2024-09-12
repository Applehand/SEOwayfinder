from flask import render_template
from spider.storage import fetch_all_project_names, fetch_pages_by_project, fetch_page_data_by_id
from web import report_view


def init_routes(app):
    @app.route('/')
    def index():
        project_names = fetch_all_project_names()
        return render_template('index.html', project_names=project_names)

    @app.route('/report/<project_name>')
    def show_report(project_name):
        return report_view.show_project_report(project_name)

    @app.route('/page/<int:page_id>')
    def show_page_data(page_id):
        """
        This route will show detailed data for a specific page by its id.
        """
        page_data = fetch_page_data_by_id(page_id)
        if not page_data:
            return "Page not found", 404

        return render_template('page_detail.html', page_data=page_data)

