import sqlite3


def create_view(path, name):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    cursor.execute(f'''
    CREATE VIEW IF NOT EXISTS {name} AS
    SELECT 
        pt.title AS title,
        pt.text as text,
        m.campus AS campus,
        m.date AS date,
        m.section AS section,
        t.name AS tag,
        p.name AS person,
        b.name AS branch,
        m.link as link,
        m.parent_link as parent_link
    FROM meta AS m
        LEFT JOIN post AS pt 
            ON m.id = pt.id
        LEFT JOIN meta_tag AS mt 
            ON m.id = mt.meta_id
        LEFT JOIN tag AS t 
            ON t.id = mt.tag_id
        LEFT JOIN meta_person AS mp 
            ON m.id = mp.meta_id
        LEFT JOIN person AS p 
            ON p.id = mp.person_id
        LEFT JOIN meta_branch AS mb 
            ON m.id = mb.meta_id
        LEFT JOIN branch AS b 
            ON b.id = mb.branch_id;
    ''')

    conn.commit()
    conn.close()
