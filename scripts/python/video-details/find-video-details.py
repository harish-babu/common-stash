import requests
import json
import math
import sys

def make_http_request(session_details, viewing_time, component_id):
    """
    Make an HTTP request to update video status.

    :param viewing_time: The viewing time of the video component
    :param component_id: The ID of the video component
    """
    url = "https://learnerprogress.upgrad.com/progress/video/status"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en;q=0.5",
        "auth-token": session_details['auth-token'],
        "content-type": "application/json;charset=UTF-8",
        "courseid": "4701",
        "origin": "https://learn.upgrad.com",
        "priority": "u=1, i",
        "referer": "https://learn.upgrad.com/",
        "sec-ch-ua": "\"Chromium\";v=\"124\", \"Brave\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "sessionid": session_details['session-id'],
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    data = {"seekTime": str(math.floor(viewing_time)), "componentId": component_id}
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Updated video status for component {component_id} successfully!")
    else:
        print(f"Error updating video status for component {component_id}: {response.text}")

def mark_component_complete(session_details, userId, component_id):
    # Set the API endpoint URL
    url = "https://learnerprogress.upgrad.com/progress"
    payload = {"completed": True, "componentId": component_id, "percentComplete": 100}

    # Set the request headers
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-GB,en;q=0.8",
        "auth-token": session_details['auth-token'],
        "Content-Type": "application/json;charset=UTF-8",
        "CourseId": "4701",
        "Origin": "https://learn.upgrad.com",
        "Referer": "https://learn.upgrad.com/",
        "Sec-Ch-Ua": '"Brave";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "macOS",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Sec-Gpc": "1",
        "SessionId": session_details['session-id'],
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    # Set the request data
    data = {"completed": True, "componentId": component_id, "percentComplete": 100}

    # Convert the data to JSON
    json_data = json.dumps(data)

    # Make the PUT request
    response = requests.put(url, headers=headers, data=json_data, params={"userId": userId})

    # Check the response status code
    if response.status_code == 200:
        print("Request successful!")
    else:
        print("Error:", response.status_code)



def find_video_components(auth_token, json_obj, userId, segment_id):
    """
    Given a JSON object and a session ID, find all components of type 'video'
    and print their ID, name property, and viewingTime property.

    :param json_obj: The JSON object to search
    :param segment_id: The ID of the session to search for
    """
    for module in json_obj['modules']:
        for session in module['sessions']:
            for segment in session['segments']:
                if segment['id'] == int(segment_id):
                    print('found segment')
                    for component in segment['components']:
                        if component['type'] == 'video':
                            print(component['type'])
                            print(f"ID: {component['id']}")
                            print(f"Name: {component['name']}")
                            print(f"Viewing Time: {component['video']['viewingTime']}")
                            viewing_time = component['video']['viewingTime']
                            component_id = component['id']
                            make_http_request(auth_token, viewing_time, component_id)
                            mark_component_complete(auth_token, userId, component_id)
                            print("---")

# Example usage:

userId = 5436172
session_details = {
    "auth-token": 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI1NDM2MTcyIiwiaWF0IjoxNzEzODU3Njg5LCJleHAiOjE3MTkwNDE2ODksImVtYWlsIjoiaGFyaXNoLmJhYnVAZ21haWwuY29tIiwicm9sZXMiOlsiUk9MRV9TVFVERU5UIl0sInJlZmVycmFsQ29kZSI6IklNU0lIWiIsImlzc3VlZFRlbmFudCI6IlVHQjJDIn0.kWoe-WWyT8EfWYY6C-zi1AjQxqMN4dTn-L1x7gsx0zbngwEEu1tIgwX2GbXojRTvZEWKMKBCYYRjbzVrCpU3qw',
    "session-id": 'hJP5Z3JeXDQSqVu8X88TbXp7DiCU2oGH'
}



def read_json_file(file_path):
    """
    Reads a JSON file and returns its content as a Python dictionary.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: The content of the JSON file.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not a valid JSON.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}")
        return None

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <json_file> <segment_id>")
        sys.exit(1)

    file_path = sys.argv[1]
    segment_id = int(sys.argv[2])
    data = read_json_file(file_path)
    if data is not None:
        # print("JSON data:")
        # print(data)
        find_video_components(session_details, data, userId, segment_id)

if __name__ == "__main__":
    main()