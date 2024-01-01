import json
import statistics
import random
import os
import concurrent.futures

class FamilyTre:
    def __init__(self, file_path, directory_path=None):
        self.file_path = file_path
        self.directory_path = directory_path
        self.family_tree = self.load_json()

    def load_json(self):
        if self.file_path:
            with open(self.file_path, 'r') as file:
                return json.load(file)['lineage']['Members']
        return None

    def process_file(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)['lineage']['Members']
        processor = FamilyTre(data)
        return processor.process_family_tree(data)

    def process_all_files(self):
        # Process each file in the directory
        if self.directory_path:
            for filename in os.listdir(self.directory_path):
                if filename.endswith('.json'):
                    file_path = os.path.join(self.directory_path, filename)
                    processor = FamilyTre(file_path)
                    lines, names_and_ages, active_period = processor.process_family_tree(processor.family_tree)
                    shortest_line = min(lines, key=lambda x: x['duration'])
                    longest_line = max(lines, key=lambda x: x['duration'])
                    ages = [age for _, age in names_and_ages]
                    mean_age = statistics.mean(ages)
                    median_age = statistics.median(ages)
                    output_data = {
                        'Shortest Line': shortest_line,
                        'Longest Line': longest_line,
                        'Mean Age': mean_age,
                        'Median Age': median_age,
                        'Active Period': active_period
                    }

                    # Save output to a file
                    output_filename = 'processed_' + filename
                    self.save_output(output_data, os.path.join(self.directory_path, output_filename))

    def process_files_in_directory(self, directory, pool_size):
        file_paths = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.json')]

        with concurrent.futures.ThreadPoolExecutor(max_workers=pool_size) as executor:
            # Submit each file to be read by the thread pool
            futures = [executor.submit(self.process_file, file_path) for file_path in file_paths]

            # Collect and process results as they are completed
            results = []
            for future in concurrent.futures.as_completed(futures):
                data = future.result()
                processed_data = self.process_family_tree(data)
                results.append(processed_data)

        return results

    def save_output(self, data, file_path):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def is_valid_member(self, member, parent_birth_year=None):
        try:
            birth_year = int(member['BirthYear'])
            death_year = int(member['DeathYear'])
            if birth_year < death_year and (parent_birth_year is None or birth_year >= parent_birth_year):
                return True
            else:
                print('Invalid member: ', member, 'either birth_year >= death_year' or 'birth_year < parent_birth_year',
                      'birth_year: ', birth_year, 'death_year: ', death_year, 'parent_birth_year: ', parent_birth_year)
                return False
        except ValueError:
            return False

    def process_family_tree(self, members, current_line=None, start_year=None, parent_birth_year=None):
        lines = []
        ages = []
        active_period = [float('inf'), float('-inf')]

        for member in members:
            birth_year = int(member['BirthYear'])
            death_year = int(member['DeathYear'])

            active_period[0] = min(active_period[0], birth_year)
            active_period[1] = max(active_period[1], death_year)

            if self.is_valid_member(member, parent_birth_year):
                age = death_year - birth_year
                ages.append((member['Name'], age))

                family_line = current_line + [member['Name']] if current_line else [member['Name']]
                min_start_year = min(start_year, birth_year) if start_year is not None else birth_year

                if 'Members' in member:
                    desc_lines, desc_ages, desc_active_period = self.process_family_tree(member['Members'],
                                                                                         family_line,
                                                                                         min_start_year,
                                                                                         birth_year)
                    lines.extend(desc_lines)
                    ages.extend(desc_ages)
                    active_period[0] = min(active_period[0], desc_active_period[0])
                    active_period[1] = max(active_period[1], desc_active_period[1])
                else:
                    line_duration = death_year - min_start_year
                    lines.append({'members': family_line, 'duration': line_duration})

        return lines, ages, active_period

    def generate_random_year(self, start_year, end_year):
        """Generates a random year between start_year and end_year."""
        return random.randint(start_year, end_year)

    def generate_name_by_depth_and_order(self, depth, order):
        """Generates a name based on the depth and order."""
        # Base names for depth levels
        base_names = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth"]

        # Select the base name based on depth (cycling through the list if depth exceeds the length)
        base_name = base_names[(depth - 1) % len(base_names)]

        # Append hyphens or pluses based on order
        suffix = "-" * order if order % 2 == 0 else "+" * order
        return base_name + suffix

    def generate_member_by_depth_and_order(self, start_year, end_year, max_depth, current_depth=1, order=1):
        """Generates a family member with descendants, naming based on depth and order."""
        if current_depth > max_depth:
            return None

        member = {
            'Name': self.generate_name_by_depth_and_order(current_depth, order),
            'BirthYear': self.generate_random_year(start_year, end_year),
            'DeathYear': self.generate_random_year(start_year, end_year)
        }

        # Generate descendants recursively
        if current_depth < max_depth:
            member['Members'] = [
                self.generate_member_by_depth_and_order(start_year, end_year, max_depth, current_depth + 1, i) for i in
                range(1, random.randint(2, 4))]

        return member

    def generate_lineage_json_by_depth_and_order(self, max_depth=3, start_year=1800, end_year=2023):
        """Generates a random family lineage as a JSON structure with names based on depth and order."""
        lineage = {
            'lineage': {
                'FamilyTree': 'Depth and Order Based Family Tree',
                'Members': [self.generate_member_by_depth_and_order(start_year, end_year, max_depth) for _ in
                            range(random.randint(1, 3))]
            }
        }
        return json.dumps(lineage, indent=4)



# For one single json file
processor = FamilyTre('family_tree.json')
lines, names_and_ages, active_period = processor.process_family_tree(processor.family_tree)
shortest_line = min(lines, key=lambda x: x['duration'])
longest_line = max(lines, key=lambda x: x['duration'])
sorted_names_and_ages = sorted(names_and_ages, key=lambda x: x[1])
ages = [age for _, age in names_and_ages]
mean_age = statistics.mean(ages)
median_age = statistics.median(ages)
print(lines, names_and_ages, active_period)


#For files in directory
directory_path = 'path/to/your/directory'  # Replace with your directory path
processor = FamilyTre(directory_path=directory_path)  # Initializing without a specific family tree
processor.process_all_files()



#Process in thread pool
directory_path = 'path/to/your/directory'  # Replace with your directory path
processor = FamilyTre(directory_path=directory_path)
# pool_size = int(input("Enter pool size: "))
for pool_size in [1, 2, 5]:
    print(f"Testing with pool size: {pool_size}")
    results = processor.process_files_in_directory(directory_path, pool_size)
    for result in results:
        print(result)