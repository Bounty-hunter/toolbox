import argparse
from datetime import datetime
import random
import json



MIN_MAX_TOKENS = 2000
MAX_MAX_TOKENS = 3000
MIN_IMAGE_COUNT = 4
MAX_IMAGE_COUNT = 6
MIN_IMAGE_ID = 0
MAX_IMAGE_ID = 100
MIN_QUESTION_LEN = 100
MAX_QUESTION_LEN = 500
QUESTION_REPEATE_TIMES = 2
MIN_REPEATE_REQUEST_INTERVAL = 64
NUM_REQUESTS = 1000


IMGAGE_PREFIX = "xxx"
OUPUT_JSONL_PATH = "output.jsonl"
QUEWSTION_ID = 34602
ANSWER = "woman and dog"


def generate_question_prompt(n: int) -> str:
    base = f"explain about the images"
    if n <= len(base):
        return base[:n]

    digits = 0
    while True:
        segment = f", {digits}"
        base += segment
        if len(base) >= n:
            return base[:n]
        digits += 1

def generate_unique_requests():
    unique_requests = []
    for _ in range(unique_requests_count):
        max_tokens = random.randint(MIN_MAX_TOKENS, MAX_MAX_TOKENS)
        image_count = random.randint(MIN_IMAGE_COUNT, MAX_IMAGE_COUNT)
        images = [f"{IMGAGE_PREFIX}_{random.randint(MIN_IMAGE_ID, MAX_IMAGE_ID)}.png" for _ in range(image_count)]
        image_str = ",".join(images)
        question_len = random.randint(MIN_QUESTION_LEN, MAX_QUESTION_LEN)
        question = generate_question_prompt(question_len)
        req = {
            "max_tokens": max_tokens,
            "image": image_str,
            "question": question,
            "question_id": QUEWSTION_ID,
            "answer": ANSWER
        }
        unique_requests.append(req)
    return unique_requests

def generate_full_requests(unique_requests):
    full_request = [None] * NUM_REQUESTS
    first_pos = 0
    for request in unique_requests:
        while full_request[first_pos] is not None and first_pos < NUM_REQUESTS:
            first_pos += 1
        
        full_request[first_pos] = request
        last_pos = first_pos
        for _ in range(QUESTION_REPEATE_TIMES - 1):
            next_interval = random.randint(MIN_REPEATE_REQUEST_INTERVAL, min(MIN_REPEATE_REQUEST_INTERVAL* 2, NUM_REQUESTS - 1))
            next_pos = (last_pos + next_interval) % NUM_REQUESTS
            while full_request[next_pos] is not None:
                next_pos = (next_pos + 1) % NUM_REQUESTS
            full_request[next_pos] = request
            last_pos = next_pos
    return full_request



unique_requests_count = NUM_REQUESTS // QUESTION_REPEATE_TIMES
NUM_REQUESTS = unique_requests_count * QUESTION_REPEATE_TIMES  # Adjust n to be a multiple of k
print(f"Adjusted total lines n to {NUM_REQUESTS} (multiple of k={QUESTION_REPEATE_TIMES})")

unique_requests = generate_unique_requests()
full_requests = generate_full_requests(unique_requests)

with open(OUPUT_JSONL_PATH, 'w') as f:
    for req in full_requests:
        json.dump(req, f)
        f.write('\n')

print(f"Generated JSONL file at {OUPUT_JSONL_PATH}")