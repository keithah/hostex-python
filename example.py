#!/usr/bin/env python3
"""
Example usage of the Hostex Python client library.

This script demonstrates basic usage of the main features.
Make sure to set your access token before running.
"""

import os
from datetime import datetime, timedelta
from hostex import HostexClient
from hostex.exceptions import HostexAPIError, RateLimitError


def main():
    """Main example function."""
    # Initialize client with your access token
    access_token = os.environ.get("HOSTEX_ACCESS_TOKEN")
    if not access_token:
        print("Please set HOSTEX_ACCESS_TOKEN environment variable")
        return
    
    client = HostexClient(access_token=access_token)
    
    try:
        # Example 1: List properties
        print("=== Listing Properties ===")
        properties = client.properties.list(limit=5)
        print(f"Found {properties['data']['total']} properties:")
        
        for prop in properties['data']['properties']:
            print(f"  - {prop['title']} (ID: {prop['id']})")
            if prop.get('address'):
                print(f"    Address: {prop['address']}")
            print(f"    Channels: {', '.join([ch['channel_type'] for ch in prop['channels']])}")
        
        # Example 2: List recent reservations
        print("\n=== Recent Reservations ===")
        today = datetime.now().date()
        last_week = today - timedelta(days=7)
        
        reservations = client.reservations.list(
            start_check_in_date=last_week.isoformat(),
            limit=10
        )
        
        print(f"Found {len(reservations['data']['reservations'])} recent reservations:")
        for res in reservations['data']['reservations'][:5]:
            guest_name = res.get('guest_name', 'N/A')
            print(f"  - {res['reservation_code']} - {guest_name}")
            print(f"    Check-in: {res['check_in_date']} - Check-out: {res['check_out_date']}")
            print(f"    Status: {res['status']} | Guests: {res['number_of_guests']}")
        
        # Example 3: Check availability for first property
        if properties['data']['properties']:
            property_id = properties['data']['properties'][0]['id']
            
            print(f"\n=== Availability for Property {property_id} ===")
            next_week = today + timedelta(days=7)
            
            availabilities = client.availabilities.list(
                property_ids=str(property_id),
                start_date=today.isoformat(),
                end_date=next_week.isoformat()
            )
            
            if availabilities['data']['listings']:
                availability_data = availabilities['data']['listings'][0]['availabilities']
                available_count = sum(1 for day in availability_data if day['available'])
                total_days = len(availability_data)
                
                print(f"Available: {available_count}/{total_days} days")
                
                # Show unavailable dates
                unavailable = [day['date'] for day in availability_data if not day['available']]
                if unavailable:
                    print(f"Unavailable dates: {', '.join(unavailable)}")
        
        # Example 4: List conversations
        print("\n=== Recent Conversations ===")
        conversations = client.conversations.list(limit=5)
        
        print(f"Found {len(conversations['data']['conversations'])} conversations:")
        for conv in conversations['data']['conversations']:
            guest_name = conv['guest'].get('name', 'Unknown Guest')
            print(f"  - {conv['id']} with {guest_name} ({conv['channel_type']})")
            print(f"    Last message: {conv['last_message_at']}")
        
        # Example 5: List reviews
        print("\n=== Recent Reviews ===")
        reviews = client.reviews.list(limit=5)
        
        print(f"Found {len(reviews['data']['reviews'])} reviews:")
        for review in reviews['data']['reviews']:
            print(f"  - {review['reservation_code']} (Property: {review['property_id']})")
            if review.get('guest_review'):
                score = review['guest_review'].get('score', 'N/A')
                print(f"    Guest rating: {score}/5")
            if review.get('host_review'):
                score = review['host_review'].get('score', 'N/A')
                print(f"    Host rating: {score}/5")
        
        # Example 6: List webhooks
        print("\n=== Webhooks ===")
        webhooks = client.webhooks.list()
        
        if webhooks['data']['webhooks']:
            print(f"Found {len(webhooks['data']['webhooks'])} webhooks:")
            for webhook in webhooks['data']['webhooks']:
                manageable = "✓" if webhook['manageable'] else "✗"
                print(f"  - {webhook['url']} (Manageable: {manageable})")
        else:
            print("No webhooks configured")
    
    except RateLimitError as e:
        print(f"Rate limit exceeded: {e}")
        if e.retry_after:
            print(f"Retry after {e.retry_after} seconds")
    
    except HostexAPIError as e:
        print(f"API Error {e.error_code}: {e.message}")
        if e.request_id:
            print(f"Request ID: {e.request_id}")
    
    except Exception as e:
        print(f"Unexpected error: {e}")


def oauth_example():
    """Example of OAuth authentication flow."""
    # This would typically be used in a web application
    client_id = os.environ.get("HOSTEX_CLIENT_ID")
    client_secret = os.environ.get("HOSTEX_CLIENT_SECRET")
    redirect_uri = "https://your-app.com/callback"
    
    if not client_id or not client_secret:
        print("Please set HOSTEX_CLIENT_ID and HOSTEX_CLIENT_SECRET environment variables")
        return
    
    client = HostexClient(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri
    )
    
    # Step 1: Get authorization URL
    auth_url = client.oauth.get_authorization_url(state="random_state_123")
    print(f"Visit this URL to authorize: {auth_url}")
    
    # Step 2: After user authorization, you'd get a code from the callback
    # authorization_code = "code_from_callback"
    # tokens = client.oauth.get_access_token(authorization_code)
    # print(f"Access token: {tokens['access_token']}")
    
    # Step 3: Use the client normally
    # properties = client.properties.list()


if __name__ == "__main__":
    print("Hostex Python Client Example")
    print("=" * 30)
    
    # Run the main example
    main()
    
    # Uncomment to see OAuth example
    # print("\n" + "=" * 30)
    # print("OAuth Example")
    # oauth_example()