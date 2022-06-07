import sqlite3

# 1: CREATE/CONNECT a database with a table created
# create a db 
con = sqlite3.connect('emails.db')
cursor = con.cursor()

# starting 'count_email' table fresh each time
cursor.execute('DROP TABLE IF EXISTS count_email')
# create an emtpy table of two columns
cursor.execute('''
CREATE TABLE count_email (email TEXT, count INTEGER)
''')

# 2. 
# open email text file get email address
filehandle = open('emaildb.txt')
for ln in filehandle:
    if not ln.startswith('From'): continue
    email = ln.split()[1]

    # get the 'count' from db where email column match this email address, 
    # TO move the cursor to the right definition
    cursor.execute('SELECT count FROM count_email WHERE email = ?', (email, ) )
    # fetch one row 
    row = cursor.fetchone()
    # if no such row existing in the db, insert this email into db and put a 1 as count value
    if row is None:
        cursor.execute('''INSERT INTO count_email (email, count) VALUES (?, 1)''', (email, ))
    # if this row has been inside the db, then update the count to 1 bigger
    else: 
        cursor.execute('''UPDATE count_email SET count = count + 1 WHERE email = ?''', (email, ))

# save the changes to the disk
con.commit()

#  display top 4 emails in the db
# the db needs to be sorted by desc count of emails -> create a cursor
results =cursor.execute('SELECT email, count FROM count_email ORDER BY count DESC LIMIT 5')
all = results.fetchall()
for row in all:
        print(f'email: {row[0]}  count:{ row[1]}')

con.close()