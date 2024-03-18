import requests
import threading

def make_request(url):
    # Make an HTTP GET request to the given URL
    response = requests.get(url)
    return response.status_code

def thread_function(word_list, base_url):
    # Iterate through the word list assigned to the current thread
    for word in word_list:
        # Construct the complete URL by appending the word to the base URL
        url = base_url + word
        # Make the HTTP request and get the response code
        response_code = make_request(url)
        # Check if the response code indicates a successful request (200 or 500)
        if response_code == 200 or response_code == 500:
            # Print the URL and response code if a successful response is received
            print(f"Found: {url} (Status Code: {response_code})")

def main():
    base_url = "http://127.0.0.1:5000/"
    word_list = []

    # Read the word list from the file
    with open("dir_list.txt", "r") as file:
        word_list = file.read().splitlines()

    num_threads = 3
    word_list_size = len(word_list)
    words_per_thread = word_list_size // num_threads

    threads = []
    for i in range(num_threads):
        start_index = i * words_per_thread
        end_index = (i + 1) * words_per_thread if i < num_threads - 1 else word_list_size
        thread_words = word_list[start_index:end_index]

        # Create a new thread, passing the assigned word list and the base URL
        thread = threading.Thread(target=thread_function, args=(thread_words, base_url))
        # Start the thread
        thread.start()
        # Add the thread to the list of active threads
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()