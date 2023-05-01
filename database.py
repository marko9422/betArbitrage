import mysql.connector


def save_data(table_name,name, match, date, odds):
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
        database='python'
    )
    mycursor = db.cursor()

    # Push data into table.
    mycursor.execute(f"INSERT INTO {table_name} (name, game, odds, date ) VALUES (%s, %s, %s ,%s)",
                     (name, match, date, odds))
    db.commit()



def delete_all_data(table_name):
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
        database='python'
    )

    mycursor = db.cursor()
    # delete my previous data from table
    mycursor.execute(f"DELETE FROM {table_name}")
    print('Sucessfuly deleted data')

    db.commit()
