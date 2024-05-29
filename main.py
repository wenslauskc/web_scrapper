import re
from bs4 import BeautifulSoup
import requests
import os
import time

print("Type skills you want to learn")
familiar_skills = input('> ')
print(f"Searching through, please wait for courses related to {familiar_skills} .....")


def extract_review_count(review_text):
    # Regular expression to extract numeric part of review count
    pattern = r'\d+(\.\d+)?'
    match = re.search(pattern, review_text)
    if match:
        try:
            # Convert the matched group to float and round it
            review_count = float(match.group())
            # Check if the review count contains decimal places
            if review_count.is_integer():
                return int(review_count)
            else:
                # Convert the review count to an integer (representing thousands)
                return int(review_count * 1000)
        except ValueError:
            print(f"Invalid review count: {review_text}")
    return None


def find_courses():
    try:
        html_text = requests.get(f'https://www.coursera.org/search?query={familiar_skills}').text
        soup = BeautifulSoup(html_text, 'lxml')
        courses = soup.find_all('li', class_='cds-9 css-0 cds-11 cds-grid-item cds-56 cds-64 cds-76 cds-90')
        courses_saved = 0
        for index, course in enumerate(courses):
            course_reviews = course.find('div', class_='product-reviews css-pn23ng').p.text
            course_review_count = extract_review_count(course_reviews)
            if course_review_count is None:
                continue

            if course_review_count > 1000:
                course_name = course.find('div', class_='cds-ProductCard-header').a.text.strip()
                skills = course.find('div', class_='cds-CommonCard-bodyContent').p.text.strip()
                more_info = 'https://www.coursera.org' + course.find('a')['href']
                with open(os.path.join('posts', 'index.txt'), 'a') as f:
                    f.write(f"Course Title: {course_name}\n")
                    f.write(f" {skills}\n")
                    f.write(f"More Information: {more_info}\n")
                    f.write('\n')
                courses_saved += 1
                print(f'Course saved: {course_name}')
        print(f'Search completed. {courses_saved} courses saved to index.txt.')
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    while True:
        find_courses()
        time_wait = 60  # Search every minute
        print(f'Waiting {time_wait} seconds (1 minute).....')
        time.sleep(time_wait)
