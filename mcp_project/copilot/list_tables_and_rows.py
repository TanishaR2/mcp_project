import psycopg2
import json

# Load DB credentials from mcp.json
with open('mcp.json') as f:
    config = json.load(f)
    env = config['env']

conn = psycopg2.connect(
    host=env['DB_HOST'],
    port=env['DB_PORT'],
    user=env['DB_USER'],
    password=env['DB_PASSWORD'],
    dbname=env['DB_NAME']
)

cur = conn.cursor()

# List all tables
cur.execute("""
    SELECT table_name FROM information_schema.tables 
    WHERE table_schema = 'public' AND table_type='BASE TABLE';
""")
tables = [row[0] for row in cur.fetchall()]
print(f"Total tables: {len(tables)}")
for table in tables:
    print(f"\nTable: {table}")
    cur.execute(f'SELECT * FROM {table} LIMIT 2;')
    rows = cur.fetchall()
    for row in rows:
        print(row)

# Query: For view_ai_credits_dd, count students with more than 15 credits from each lp
print("\n---\nStudents with more than 15 credits in each LP from view_ai_credits_dd:")
cur.execute('''
    SELECT lp, COUNT(*) as student_count
    FROM view_ai_credits_dd
    WHERE credits > 15
    GROUP BY lp
    ORDER BY lp;
''')
results = cur.fetchall()
for lp, count in results:
    print(f"LP: {lp}, Students: {count}")

# Query: For view_ai_credits_sis, count students with more than 15 credits from each learning plan (lp)
print("\n---\nStudents with more than 15 credits in each LP from view_ai_credits_sis:")
cur.execute('''
    SELECT lp, COUNT(*) as student_count
    FROM view_ai_credits_sis
    WHERE credits > 15
    GROUP BY lp
    ORDER BY lp;
''')
results_sis = cur.fetchall()
for lp, count in results_sis:
    print(f"LP: {lp}, Students: {count}")

# Query: Number of students enrolled from 'hispanic' group in view_ai_student_enrollment
print("\n---\nNumber of students enrolled from 'hispanic' group in view_ai_student_enrollment:")
cur.execute('''
    SELECT COUNT(*) FROM view_ai_student_enrollment
    WHERE 'hispanic' = ANY(ethnicity);
''')
result = cur.fetchone()
if result:
    count_hispanic = result[0]
    print(f"Hispanic students enrolled: {count_hispanic}")
else:
    print("No data found or error in query.")

cur.close()
conn.close()
