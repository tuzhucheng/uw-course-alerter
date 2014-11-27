import subprocess
import urllib

def main():
    api_url = 'https://uw-alert.herokuapp.com/check_availability'
    courses = [{'level': 'under',
                'session': 1151,
                'subject': 'CS',
                'number': 341,
                'email': 'youremail@example.com'}]
    for course in courses:
        encoded_query = urllib.urlencode(course)
        subprocess.call(['curl', '-X', 'POST', '-H', 'Cache-Control: no-cache', '-H', 'Content-Type: application/x-www-form-urlencoded', '-d', encoded_query, api_url])

if __name__ == '__main__':
    main()

