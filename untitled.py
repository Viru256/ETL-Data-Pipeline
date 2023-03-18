import streamlit as st
import pandas as pd
import pypyodbc

sql_query = "INSERT INTO Orders (order_date, cust_name, sp, cp) VALUES (?,?,?,?)"

st.set_page_config(page_title="File Uploader", page_icon=":file_folder:")
st.title("File Uploader App")

uploaded_file = st.file_uploader("Choose a file", type=["sql", "csv", "xlsx"])

if uploaded_file is not None:
    # Read file contents and create DataFrame
    if uploaded_file.type == 'application/vnd.ms-excel':
        df = pd.read_excel(uploaded_file)
    elif uploaded_file.type == 'text/csv':
        df = pd.read_csv(uploaded_file)
       
       
        
    elif uploaded_file.type == 'application/sql':
        # Replace with appropriate SQL reader
        st.write("SQL file detected. Please provide an appropriate reader to create DataFrame.")
        df = None
    else:
        st.write("Unsupported file type.")
        df = None

    # Display DataFrame
    if df is not None:
        st.write(df)
        # Establish connection to SQL Server
        DRIVER_NAME = 'SQL Server'
        SERVER_NAME = 'DESKTOP-K2MJ54H'
        DATABASE_NAME = 'P1'

        conn_string = f"""
            Driver={{{DRIVER_NAME}}};
            Server={SERVER_NAME};
            Database={DATABASE_NAME};
            Trusted_Connection=yes;
        """

        try:
            conn = pypyodbc.connect(conn_string)
        except Exception as e:
            st.write(e)
            st.write('Task is terminated')
        else:
            cursor = conn.cursor()
            st.write('Connected to the database')

            # Check column names and data types
            orders = pd.read_sql("SELECT TOP 0 * FROM Orders", conn)
            if df.columns.equals(orders.columns):
                for col1, col2 in zip(df.columns, orders.columns):
                    if col1 == col2:
                        st.write(f"{col1} and {col2} match")
                        if col1 == 'order_date':
                            try:
                                pd.to_datetime(df[col1], format='%Y-%m-%d')
                            except ValueError:
                                st.write(f"{col1} data type does not match. Please ensure the format is YYYY-MM-DD.")
                                vr1 = pd.read_csv(r"C:\Users\Viraj Humbre\Desktop\Orient\new2.csv")
                                st.write(vr1)
                                df = None
                            else:
                                st.write(f"{col1} and {col2} datatype match")
                                vr1 = pd.read_csv(r"C:\Users\Viraj Humbre\Desktop\Orient\new.csv")
                                st.write(vr1)
                      
                    else:
                        st.write(f"{col1} and {col2} columns do not match")
                        df = None
                        break  # Exit the loop if there is a column name error

                if df is not None:
                    # Iterate over rows and insert into SQL Server table
                    for index, row in df.iterrows():
                        values = tuple(row)
                        cursor.execute(sql_query, values)

                    conn.commit()
                    st.write("Data inserted in SQL Server table.")
                   
            else:
                st.write("Column name error.")
                vr1 = pd.read_csv(r"C:\Users\Viraj Humbre\Desktop\Orient\new3.csv")
                st.write(vr1)
               
           

            # Close connection
            conn.close()
else:
    st.write("Please upload a file.")