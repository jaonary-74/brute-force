import requests
import threading

def make_request(url):
    # Sends a GET request to the specified URL and returns the response's status code
    response = requests.get(url)
    return response.status_code

def thread_function(word_list, base_url):
    # Processes a list of words and checks each word by making a request to the base URL
    for word in word_list:
        url = base_url + word
        response_code = make_request(url)
        if response_code == 200 or response_code == 500:
            # Prints the URL and status code if the response is either 200 (OK) or 500 (Internal Server Error)
            print(f"Found: {url} (Status Code: {response_code})")

def main():
    # Entry point of the program
    base_url = "http://127.0.0.1:5000/"
    word_list = []

    # Reads a list of words from a file
    with open("dir_list.txt", "r") as file:
        word_list = file.read().splitlines()

    # Configures the number of threads and words per thread
    num_threads = 3
    word_list_size = len(word_list)
    words_per_thread = word_list_size // num_threads

    threads = []

    # Spawns multiple threads and assigns words to each thread for processing
    for i in range(num_threads):
        start_index = i * words_per_thread
        end_index = (i + 1) * words_per_thread if i < num_threads - 1 else word_list_size
        thread_words = word_list[start_index:end_index]

        thread = threading.Thread(target=thread_function, args=(thread_words, base_url))
        thread.start()
        threads.append(thread)

    # Waits for all threads to finish before exiting the program
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()