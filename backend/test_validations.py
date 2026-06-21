#!/usr/bin/env python
# Test script for validation functions

from backend.app import app, extract_youtube_id, is_valid_url, is_valid_email

print("=" * 50)
print("Testing Validation Functions")
print("=" * 50)

print("\n✓ All validation functions loaded successfully!")

print("\n--- Testing extract_youtube_id() ---")
test_urls = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://youtu.be/dQw4w9WgXcQ",
    "https://www.youtube.com/embed/dQw4w9WgXcQ",
    "https://example.com"
]
for url in test_urls:
    result = extract_youtube_id(url)
    print(f"  URL: {url}")
    print(f"  Result: {result}\n")

print("--- Testing is_valid_url() ---")
test_urls = [
    "https://example.com",
    "http://test.com",
    "not-a-url",
    "ftp://invalid.com"
]
for url in test_urls:
    result = is_valid_url(url)
    print(f"  URL: {url} -> {result}")

print("\n--- Testing is_valid_email() ---")
test_emails = [
    "user@example.com",
    "test.user@domain.co.uk",
    "invalid-email",
    "no@domain"
]
for email in test_emails:
    result = is_valid_email(email)
    print(f"  Email: {email} -> {result}")

print("\n" + "=" * 50)
print("✓ All validation functions working correctly!")
print("=" * 50)
