#!/usr/bin/python3

import argparse
import mysql.connector


def parse_arguments():
    parser = argparse.ArgumentParser(description="List entries from Swissprot file based on given keywords.")
    parser.add_argument("--keyword", nargs='+', help="List of keywords for filtering", required=True)
    # 'nargs': + since we accept one or more values
    parser.add_argument("--swissprot", type=argparse.FileType('r'), help="Swissprot file")
    parser.add_argument("--db", help="Database")
    return parser.parse_args()


def parse_entry_line_type(line, line_type):
    if line_type == 'AC':
        # KW ends with '.', while AC ends with ';'
        # -> remove last semicolon so that the loop is done after the last ac number (else appends '')
        line = line[:-1]

    line_type_list = []
    line = line.strip(f'{line_type}   ')

    for line_type in line.split(';'):
        line_type = line_type.strip().strip('.')
        line_type_list.append(line_type)
    return line_type_list


def update_ac_output_list(list_of_entry_keywords, keywords, all_ac_numbers, list_of_entry_ac):
    found_matching_keywords = False
    for current_keyword in list_of_entry_keywords:
        for input_keyword in keywords:
            # condition is met, when at least one key from our input matches with one of the entries keyword
            if current_keyword == input_keyword:
                found_matching_keywords = True

    if found_matching_keywords:
        all_ac_numbers.update(list_of_entry_ac)

    return all_ac_numbers


def print_result(result):
    for entry in result:
        print(entry)


def execute_database_query(database, keywords):
    cursor = database.cursor()

    # If there is only one keyword, create a single %s placeholder
    if len(keywords) == 1:
        placeholders = '%s'
    else:
        # Create a list of %s placeholders for each keyword
        placeholder_list = ['%s' for keyword in keywords]
        # Join the placeholders with commas and create a string
        placeholders = ', '.join(placeholder_list)

    # Create the SQL query
    # Insert the placeholders into the SQL query
    query = '''
    SELECT DISTINCT accession_nr 
    FROM has_function 
    WHERE function IN ({}) 
    ORDER BY accession_nr;
    '''.format(placeholders)

    # Execute the SQL query with keywords as parameters
    cursor.execute(query, keywords)

    # Fetch the results from the database
    result = cursor.fetchall()

    # Close the cursor
    cursor.close()

    return result


def main():
    args = parse_arguments()

    # Get keywords & save as set to remove duplicates
    keywords = set(args.keyword)

    # Check for swissprot input
    if args.swissprot:

        # List of all AC numbers
        all_ac_numbers = set()

        list_of_entry_keywords = []
        list_of_entry_ac = []

        # Get each entry from the Swissprot file
        # Each entry is seperated by '//'
        for line in args.swissprot.read().splitlines():

            if line.startswith('KW'):
                list_of_entry_keywords.extend(parse_entry_line_type(line, 'KW'))

            if line.startswith('AC'):
                list_of_entry_ac.extend(parse_entry_line_type(line, 'AC'))

            if line.startswith('//'):
                all_ac_numbers = update_ac_output_list(list_of_entry_keywords, keywords, all_ac_numbers,
                                                       list_of_entry_ac)

                list_of_entry_keywords = []
                list_of_entry_ac = []

        all_ac_numbers = update_ac_output_list(list_of_entry_keywords, keywords, all_ac_numbers, list_of_entry_ac)

        # Convert the set to a sorted list
        cleaned_ac_numbers = sorted(all_ac_numbers)

        # Print the results
        print_result(cleaned_ac_numbers)

    # Handle Database
    else:
        '''
        Database name: has_function(accession_nr, function) 
                        -> unique entries: contains each function (keyword) for it's accession_nr
        Query:
            SELECT DISTINCT accession_nr
            FROM has_function
            WHERE function IN (keyword1, ..., keywordX) -> have to insert keywords from input (as list)
            ORDER BY accession_nr
        '''

        # Connect to the database
        has_function = mysql.connector.connect(
            host="mysql2-ext.bio.ifi.lmu.de",
            user="bioprakt13",
            password="$1$S4kE4pw1$8ANT55zOf1nKHgoau9K0A0",
            database="has_function"
        )

        try:
            # Execute the database query
            result = execute_database_query(has_function, args.keyword)

            # Print the results
            print_result(result)

        finally:
            # Close the database connection
            has_function.close()


if __name__ == "__main__":
    main()
