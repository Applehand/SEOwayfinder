import sqlite3
import json
from .schemas import PageData
from .utils import get_default_db_location

DB_FILE = str(get_default_db_location())


def create_tables():
    """Create the projects and pages tables if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_name TEXT UNIQUE NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        url TEXT NOT NULL,
        title TEXT,
        meta_description TEXT,
        canonical TEXT,
        robots TEXT,
        noindex BOOLEAN,
        non_200_links TEXT,
        missing_alt_images TEXT,
        structured_data TEXT,
        headings TEXT,
        links TEXT,
        internal_links TEXT,
        external_links TEXT,
        hreflang TEXT,
        images TEXT,
        paragraphs TEXT,
        scripts TEXT,
        stylesheets TEXT,
        slug TEXT,
        url_parts TEXT,
        FOREIGN KEY (project_id) REFERENCES projects(id)
    )
    ''')
    print(f'Created database tables at {DB_FILE}')
    conn.commit()
    conn.close()


def save_page_data(project_name: str, page_data: PageData):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("INSERT OR IGNORE INTO projects (project_name) VALUES (?)", (project_name,))
        cursor.execute("SELECT id FROM projects WHERE project_name = ?", (project_name,))
        project_id = cursor.fetchone()[0]

        cursor.execute('''
        INSERT OR REPLACE INTO pages (project_id, url, title, meta_description, canonical, robots, noindex, 
                                      non_200_links, missing_alt_images, structured_data, headings, links, 
                                      internal_links, external_links, hreflang, images, paragraphs, scripts, 
                                      stylesheets, slug, url_parts)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            project_id,
            page_data.url,
            page_data.title,
            page_data.meta_description,
            page_data.canonical,
            page_data.robots,
            page_data.noindex,
            json.dumps(page_data.non_200_links),
            json.dumps(page_data.missing_alt_images),
            json.dumps(page_data.structured_data),
            json.dumps(page_data.headings),
            json.dumps(page_data.links),
            json.dumps(page_data.internal_links),
            json.dumps(page_data.external_links),
            json.dumps(page_data.hreflang),
            json.dumps([image.dict() for image in page_data.images]),
            json.dumps(page_data.paragraphs),
            json.dumps(page_data.scripts),
            json.dumps(page_data.stylesheets),
            page_data.slug,
            json.dumps(page_data.url_parts)
        ))

        conn.commit()
    except Exception as e:
        print(f"Error saving data: {e}")
    finally:
        conn.close()


def fetch_all_project_names():
    """Fetch all project names from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('SELECT project_name FROM projects')
    project_names = cursor.fetchall()

    conn.close()

    return [name[0] for name in project_names]


def fetch_pages_by_project(project_name: str):
    """
    Fetch all pages for a specific project from the database.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT *
    FROM pages
    JOIN projects ON projects.id = pages.project_id
    WHERE projects.project_name = ?
    ''', (project_name,))

    rows = cursor.fetchall()
    conn.close()

    return rows


def clear_all_data():
    """Remove all data from the projects and pages tables."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM pages')
        cursor.execute('DELETE FROM projects')

        conn.commit()
        print("All data removed from projects and pages tables.")
    except Exception as e:
        print(f"Error occurred while deleting data: {e}")
    finally:
        conn.close()


def fetch_page_data_by_id(page_id: int):
    """
    Fetch the data for a specific page by its id, including the project_name.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT pages.*, projects.project_name
    FROM pages
    JOIN projects ON pages.project_id = projects.id
    WHERE pages.id = ?
    ''', (page_id,))

    page = cursor.fetchone()
    conn.close()

    if page:
        return {
            'id': page[0],
            'project_id': page[1],
            'url': page[2],
            'title': page[3],
            'meta_description': page[4],
            'canonical': page[5],
            'robots': page[6],
            'noindex': page[7],
            'non_200_links': json.loads(page[8]),
            'missing_alt_images': json.loads(page[9]),
            'structured_data': json.loads(page[10]),
            'headings': json.loads(page[11]),
            'links': json.loads(page[12]),
            'internal_links': json.loads(page[13]),
            'external_links': json.loads(page[14]),
            'hreflang': json.loads(page[15]),
            'images': json.loads(page[16]),
            'paragraphs': json.loads(page[17]),
            'scripts': json.loads(page[18]),
            'stylesheets': json.loads(page[19]),
            'slug': page[20],
            'url_parts': json.loads(page[21]),
            'project_name': page[22]
        }
    return None


def remove_project_by_name(project_name: str):
    """Remove a specific project and its related data by project name."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT id FROM projects WHERE project_name = ?', (project_name,))
        project = cursor.fetchone()

        if not project:
            return False

        project_id = project[0]

        cursor.execute('DELETE FROM pages WHERE project_id = ?', (project_id,))
        cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))

        conn.commit()
        return True
    except Exception as e:
        print(f"Error occurred while deleting project '{project_name}': {e}")
        return False
    finally:
        conn.close()
