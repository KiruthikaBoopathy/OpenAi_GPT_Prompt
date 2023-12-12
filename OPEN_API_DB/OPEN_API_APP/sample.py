import fitz
import openai
import mysql.connector


class PDFProcessor:

    def extract_text_from_pdf(self, pdf_paths):
        text = ""
        try:
            for pdf_path in pdf_paths:
                with fitz.open(pdf_path) as pdf_document:
                    for page_num in range(pdf_document.page_count):
                        page = pdf_document[page_num]
                        text += page.get_text("text")
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")

        return text

    def get_field_names_from_db(self, db_config):
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Assuming your table name is 'open_api_app_pdf_fields'
            table_name = 'open_api_app_pdf_fields'

            # Execute the query to get column names
            cursor.execute(f"SHOW COLUMNS FROM {table_name}")

            # Fetch all column names and filter out 'id'
            columns = [column[0] for column in cursor.fetchall() if column[0].lower() != 'id']

            # Close the connection
            conn.close()

            return columns

        except Exception as e:
            print(f"Error retrieving field names from the database: {e}")
            return []

    def extract_and_generate_information(self, pdf_paths):
        # Extract text from PDF
        pdf_text = self.extract_text_from_pdf(pdf_paths)

        # Fetch field names from the MySQL database table
        db_field_names = self.get_field_names_from_db(db_config)

        # Use GPT-3 to generate information based on the prompt
        openai.api_key = "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"

        prompt = f"Extract the following information from the given PDF:\n\n{pdf_text}\n\nDatabase fields: {', '.join(db_field_names)}\n\n"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500
        )

        # Extract and parse the generated text
        generated_text = response.choices[0].text.strip()
        extracted_information = self.parse_generated_text(generated_text, db_field_names)

        # Insert into the database
        self.insert_into_db(extracted_information, db_config, table_name)
        print("db_field_names:",db_field_names)
        return extracted_information


    def parse_generated_text(self, generated_text, db_field_names):
        lines = generated_text.split('\n')
        result_dict = {}

        for line in lines:
            if ':' in line:
                key, value = map(str.strip, line.split(':', 1))
                # Convert the key to lowercase to match the case of database field names
                key_lower = key.lower()
                # Check if the lowercase key exists in the database field names
                if key_lower in db_field_names:
                    result_dict[key_lower] = value

        # print(result_dict)
        return result_dict


    def insert_into_db(self, extracted_information, db_config, table_name):
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # print(extracted_information)

            columns = ', '.join(key for key in extracted_information.keys())
            # print(columns)
            values = ', '.join(['%s'] * len(extracted_information))
            # print(values)

            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"

            print(f"SQL Query: {insert_query}")
            print(f"Values: {tuple(extracted_information.values())}")

            cursor.execute(insert_query, tuple(extracted_information.values()))

            conn.commit()
            conn.close()

        except Exception as e:
            print(f"Error inserting data into the database: {e}")


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'vrdella!6',
    'database': 'openai_prompt'
}

table_name = "open_api_app_pdf_fields"
