# Hostex Python Library Examples

This document provides comprehensive examples of using the hostex-python library.

## Table of Contents

1. [Authentication](#authentication)
2. [Properties Management](#properties-management)
3. [Reservation Operations](#reservation-operations)
4. [Availability Management](#availability-management)
5. [Listing Calendar Management](#listing-calendar-management)
6. [Messaging and Conversations](#messaging-and-conversations)
7. [Reviews Management](#reviews-management)
8. [Webhook Integration](#webhook-integration)
9. [Custom Fields](#custom-fields)
10. [Error Handling](#error-handling)

## Authentication

### Basic API Token Authentication

```python
from hostex import HostexClient

# Initialize with API token
client = HostexClient(access_token="your_hostex_api_token")
```

### OAuth Authentication Flow

```python
from hostex import HostexClient
import webbrowser

# Initialize OAuth client
client = HostexClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    redirect_uri="https://yourapp.com/callback"
)

# Step 1: Generate authorization URL
auth_url = client.oauth.get_authorization_url(
    state="random_state_string"
)
print(f"Visit this URL to authorize: {auth_url}")
webbrowser.open(auth_url)

# Step 2: After user authorization, exchange code for tokens
authorization_code = input("Enter the authorization code from callback: ")
tokens = client.oauth.get_access_token(authorization_code)

# Step 3: Use the access token
client.set_access_token(tokens['access_token'])
print("Authentication successful!")

# Step 4: Refresh token when needed
new_tokens = client.oauth.refresh_access_token(tokens['refresh_token'])
```

## Properties Management

### Listing All Properties

```python
# Get all properties with pagination
def get_all_properties(client):
    all_properties = []
    offset = 0
    limit = 100
    
    while True:
        response = client.properties.list(offset=offset, limit=limit)
        properties = response['data']['properties']
        all_properties.extend(properties)
        
        if len(properties) < limit:
            break
        offset += limit
    
    return all_properties

# Usage
properties = get_all_properties(client)
print(f"Total properties: {len(properties)}")

for prop in properties[:5]:  # Show first 5
    print(f"ID: {prop['id']}, Title: {prop['title']}")
    print(f"Address: {prop.get('address', 'Not specified')}")
    print(f"Channels: {[ch['channel_type'] for ch in prop['channels']]}")
    print("---")
```

### Getting Specific Property Details

```python
# Get details for a specific property
property_id = 12345
response = client.properties.list(id=property_id)

if response['data']['properties']:
    prop = response['data']['properties'][0]
    print(f"Property: {prop['title']}")
    print(f"Location: {prop.get('latitude', 'N/A')}, {prop.get('longitude', 'N/A')}")
    
    # List all channels for this property
    print("Available on channels:")
    for channel in prop['channels']:
        print(f"  - {channel['channel_type']}: {channel['listing_id']}")
```

### Working with Room Types

```python
# Get all room types
room_types = client.room_types.list()

for room_type in room_types['data']['room_types']:
    print(f"Room Type: {room_type['title']} (ID: {room_type['id']})")
    print(f"Properties: {len(room_type['properties'])}")
    print(f"Channels: {[ch['channel_type'] for ch in room_type['channels']]}")
    print("---")
```

## Reservation Operations

### Querying Reservations

```python
from datetime import datetime, timedelta

# Get reservations for the next 30 days
today = datetime.now().date()
next_month = today + timedelta(days=30)

reservations = client.reservations.list(
    start_check_in_date=today.isoformat(),
    end_check_in_date=next_month.isoformat(),
    status="accepted",
    limit=50
)

print(f"Found {len(reservations['data']['reservations'])} accepted reservations")

for reservation in reservations['data']['reservations'][:5]:
    print(f"Reservation: {reservation['reservation_code']}")
    print(f"Guest: {reservation.get('guest_name', 'N/A')}")
    print(f"Check-in: {reservation['check_in_date']}")
    print(f"Check-out: {reservation['check_out_date']}")
    print(f"Guests: {reservation['number_of_guests']}")
    print(f"Channel: {reservation['channel_type']}")
    print("---")
```

### Creating a Direct Booking

```python
# First, get custom channels and income methods
custom_channels = client.custom_channels.list()
income_methods = client.income_methods.list()

# Create a direct booking reservation
try:
    reservation = client.reservations.create(
        property_id="12345",
        custom_channel_id=custom_channels['data']['custom_channels'][0]['id'],
        check_in_date="2024-07-01",
        check_out_date="2024-07-07",
        number_of_guests=2,
        guest_name="Jane Smith",
        email="jane.smith@example.com",
        mobile="+1234567890",
        currency="USD",
        rate_amount=84000,  # $840.00 (6 nights × $140/night)
        commission_amount=8400,  # 10% commission
        received_amount=75600,  # Amount after commission
        income_method_id=income_methods['data']['custom_channels'][0]['id'],
        remarks="Direct booking from website"
    )
    
    print(f"Reservation created successfully!")
    print(f"Reservation code: {reservation['reservation_code']}")
    
except Exception as e:
    print(f"Failed to create reservation: {e}")
```

### Managing Reservation Details

```python
# Update lock code for a stay
stay_code = "0-1234567-abcdef"
try:
    client.reservations.update_lock_code(
        stay_code=stay_code,
        lock_code="9876"
    )
    print(f"Lock code updated for stay: {stay_code}")
except Exception as e:
    print(f"Failed to update lock code: {e}")

# Cancel a direct booking
reservation_code = "0-1234567-abcdef"
try:
    client.reservations.cancel(reservation_code)
    print(f"Reservation {reservation_code} cancelled")
except Exception as e:
    print(f"Failed to cancel reservation: {e}")
```

## Availability Management

### Checking Property Availability

```python
from datetime import datetime, timedelta

# Check availability for multiple properties
property_ids = "12345,67890,11111"
start_date = datetime.now().date()
end_date = start_date + timedelta(days=30)

availabilities = client.availabilities.list(
    property_ids=property_ids,
    start_date=start_date.isoformat(),
    end_date=end_date.isoformat()
)

for listing in availabilities['data']['listings']:
    print(f"\nProperty ID: {listing['id']}")
    
    # Count available and unavailable dates
    available_count = sum(1 for day in listing['availabilities'] if day['available'])
    total_days = len(listing['availabilities'])
    
    print(f"Available: {available_count}/{total_days} days")
    
    # Show unavailable dates
    unavailable_dates = [
        day['date'] for day in listing['availabilities'] 
        if not day['available']
    ]
    if unavailable_dates:
        print(f"Unavailable dates: {', '.join(unavailable_dates[:5])}")
        if len(unavailable_dates) > 5:
            print(f"... and {len(unavailable_dates) - 5} more")
```

### Updating Property Availability

```python
# Block specific dates
blocked_dates = ["2024-07-15", "2024-07-16", "2024-07-17"]

try:
    client.availabilities.update(
        property_ids=[12345],
        dates=blocked_dates,
        available=False
    )
    print(f"Blocked dates: {', '.join(blocked_dates)}")
except Exception as e:
    print(f"Failed to update availability: {e}")

# Block a date range
try:
    client.availabilities.update(
        property_ids=[12345, 67890],
        start_date="2024-08-01",
        end_date="2024-08-07",
        available=False
    )
    print("Date range blocked for maintenance")
except Exception as e:
    print(f"Failed to block date range: {e}")

# Make dates available again
try:
    client.availabilities.update(
        property_ids=[12345],
        dates=["2024-07-15"],
        available=True
    )
    print("Date made available again")
except Exception as e:
    print(f"Failed to make date available: {e}")
```

## Listing Calendar Management

### Querying Listing Calendars

```python
# Query calendar for multiple listings
listings_to_query = [
    {
        "channel_type": "airbnb",
        "listing_id": "12345678"
    },
    {
        "channel_type": "booking.com",
        "listing_id": "hotel_123-rateplan_456"
    }
]

calendar_data = client.listings.get_calendar(
    start_date="2024-07-01",
    end_date="2024-07-31",
    listings=listings_to_query
)

for listing in calendar_data['data']['listings']:
    print(f"\nChannel: {listing['channel_type']}")
    print(f"Listing ID: {listing['listing_id']}")
    
    # Calculate average price
    prices = [day['price'] for day in listing['calendar'] if day['price'] > 0]
    if prices:
        avg_price = sum(prices) / len(prices)
        print(f"Average price: ${avg_price:.2f}")
    
    # Show inventory summary
    total_inventory = sum(day['inventory'] for day in listing['calendar'])
    print(f"Total inventory for period: {total_inventory}")
```

### Updating Listing Prices

```python
# Update prices for a listing
price_updates = [
    {
        "date": "2024-07-15",
        "price": 150.00
    },
    {
        "date": "2024-07-16", 
        "price": 175.00  # Weekend premium
    },
    {
        "date": "2024-07-17",
        "price": 175.00
    }
]

try:
    client.listings.update_prices(
        channel_type="airbnb",
        listing_id="12345678",
        prices=price_updates
    )
    print("Prices updated successfully")
except Exception as e:
    print(f"Failed to update prices: {e}")
```

### Updating Listing Inventories

```python
# Update inventory levels
inventory_updates = [
    {
        "date": "2024-07-15",
        "inventory": 0  # Fully booked
    },
    {
        "date": "2024-07-16",
        "inventory": 1  # One unit available
    }
]

try:
    client.listings.update_inventories(
        channel_type="booking.com",
        listing_id="hotel_123-rateplan_456",
        inventories=inventory_updates
    )
    print("Inventory levels updated")
except Exception as e:
    print(f"Failed to update inventory: {e}")
```

## Messaging and Conversations

### Listing and Managing Conversations

```python
# Get all conversations
conversations = client.conversations.list(limit=50)

print(f"Found {len(conversations['data']['conversations'])} conversations")

for conv in conversations['data']['conversations'][:5]:
    print(f"\nConversation ID: {conv['id']}")
    print(f"Channel: {conv['channel_type']}")
    print(f"Guest: {conv['guest'].get('name', 'N/A')}")
    print(f"Last message: {conv['last_message_at']}")
    
    if conv.get('property_title'):
        print(f"Property: {conv['property_title']}")
    
    if conv.get('check_in_date'):
        print(f"Check-in: {conv['check_in_date']} - {conv['check_out_date']}")
```

### Getting Conversation Details and Sending Messages

```python
# Get detailed conversation history
conversation_id = "conv_123456"
conversation = client.conversations.get(conversation_id)

print(f"Conversation with {conversation['data']['guest']['name']}")
print(f"Channel: {conversation['data']['channel_type']}")

# Show recent messages
messages = conversation['data']['messages'][-5:]  # Last 5 messages
for msg in messages:
    sender = msg['sender_role'].capitalize()
    content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
    print(f"{sender}: {content}")
    print(f"  Sent: {msg['created_at']}")

# Send a message
try:
    client.conversations.send_message(
        conversation_id=conversation_id,
        message="Thank you for choosing our property! We're excited to host you."
    )
    print("Message sent successfully")
except Exception as e:
    print(f"Failed to send message: {e}")

# Send a message with an image
import base64

# Assuming you have a JPEG image file
try:
    with open("welcome_image.jpg", "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')
    
    client.conversations.send_message(
        conversation_id=conversation_id,
        message="Here's a photo of your accommodation!",
        jpeg_base64=image_data
    )
    print("Message with image sent successfully")
except Exception as e:
    print(f"Failed to send message with image: {e}")
```

## Reviews Management

### Querying and Analyzing Reviews

```python
# Get recent reviews
reviews = client.reviews.list(
    start_check_out_date="2024-01-01",
    end_check_out_date="2024-06-30",
    limit=100
)

print(f"Found {len(reviews['data']['reviews'])} reviews")

# Analyze review scores
host_scores = []
guest_scores = []

for review in reviews['data']['reviews']:
    if review.get('host_review'):
        print(f"\nReservation: {review['reservation_code']}")
        print(f"Property: {review['property_id']}")
        print(f"Channel: {review['channel_type']}")
        print(f"Check-out: {review['check_out_date']}")
        
        # Host review of guest
        if review.get('host_review'):
            host_review = review['host_review']
            if 'score' in host_review:
                host_scores.append(host_review['score'])
                print(f"Host rated guest: {host_review['score']}/5")
            if host_review.get('content'):
                print(f"Host comment: {host_review['content'][:100]}...")
        
        # Guest review of property
        if review.get('guest_review'):
            guest_review = review['guest_review']
            if 'score' in guest_review:
                guest_scores.append(guest_review['score'])
                print(f"Guest rated property: {guest_review['score']}/5")
            if guest_review.get('content'):
                print(f"Guest comment: {guest_review['content'][:100]}...")
        
        # Host reply to guest review
        if review.get('host_reply'):
            print(f"Host replied: {review['host_reply']['content'][:100]}...")

# Calculate averages
if host_scores:
    avg_host_score = sum(host_scores) / len(host_scores)
    print(f"\nAverage host rating of guests: {avg_host_score:.2f}/5")

if guest_scores:
    avg_guest_score = sum(guest_scores) / len(guest_scores)
    print(f"Average guest rating of properties: {avg_guest_score:.2f}/5")
```

### Creating Reviews and Replies

```python
# Leave a review for a guest
reservation_code = "0-1234567-abcdef"

try:
    client.reviews.create(
        reservation_code=reservation_code,
        host_review_score=5.0,
        host_review_content="Excellent guest! Very respectful of the property and followed all house rules. Would welcome them back anytime."
    )
    print(f"Review created for reservation: {reservation_code}")
except Exception as e:
    print(f"Failed to create review: {e}")

# Reply to a guest's review
try:
    client.reviews.create(
        reservation_code=reservation_code,
        host_reply_content="Thank you so much for the wonderful review! We're delighted you enjoyed your stay and look forward to hosting you again soon."
    )
    print(f"Reply posted for reservation: {reservation_code}")
except Exception as e:
    print(f"Failed to post reply: {e}")
```

## Webhook Integration

### Setting Up Webhooks

```python
# List existing webhooks
webhooks = client.webhooks.list()
print(f"Current webhooks: {len(webhooks['data']['webhooks'])}")

for webhook in webhooks['data']['webhooks']:
    print(f"ID: {webhook['id']}, URL: {webhook['url']}")
    print(f"Manageable: {webhook['manageable']}")
    print(f"Created: {webhook['created_at']}")

# Create a new webhook
webhook_url = "https://yourapp.com/hostex-webhook"

try:
    new_webhook = client.webhooks.create(url=webhook_url)
    print(f"Webhook created successfully: {new_webhook}")
except Exception as e:
    print(f"Failed to create webhook: {e}")
```

### Processing Webhook Events

```python
# Example Flask webhook handler
from flask import Flask, request, jsonify
import hmac
import hashlib

app = Flask(__name__)

@app.route('/hostex-webhook', methods=['POST'])
def handle_webhook():
    # Verify webhook authenticity (if you have the secret token)
    secret_token = request.headers.get('Hostex-Webhook-Secret-Token')
    
    # Process the webhook payload
    payload = request.get_json()
    
    event_type = payload.get('event')
    timestamp = payload.get('timestamp')
    
    print(f"Received webhook: {event_type} at {timestamp}")
    
    # Handle different event types
    if event_type == 'reservation_created':
        reservation_code = payload.get('reservation_code')
        stay_code = payload.get('stay_code')
        print(f"New reservation: {reservation_code}")
        
        # Fetch full reservation details
        reservations = client.reservations.list(reservation_code=reservation_code)
        if reservations['data']['reservations']:
            reservation = reservations['data']['reservations'][0]
            # Process new reservation...
    
    elif event_type == 'reservation_updated':
        reservation_code = payload.get('reservation_code')
        print(f"Reservation updated: {reservation_code}")
        # Handle reservation update...
    
    elif event_type == 'message_created':
        conversation_id = payload.get('conversation_id')
        message_id = payload.get('message_id')
        print(f"New message in conversation: {conversation_id}")
        
        # Fetch conversation details
        conversation = client.conversations.get(conversation_id)
        # Process new message...
    
    elif event_type == 'property_availability_updated':
        property_id = payload.get('property_id')
        availabilities = payload.get('availabilities', [])
        print(f"Availability updated for property: {property_id}")
        # Handle availability changes...
    
    # Must respond within 3 seconds
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(port=5000)
```

## Custom Fields

### Managing Custom Fields for Reservations

```python
# Get custom fields for a stay
stay_code = "0-1234567-abcdef"

try:
    custom_fields = client.reservations.get_custom_fields(stay_code)
    print(f"Custom fields for {stay_code}:")
    
    fields = custom_fields['data']['custom_fields']
    if fields:
        for field_name, field_value in fields.items():
            print(f"  {field_name}: {field_value}")
    else:
        print("  No custom fields set")
        
except Exception as e:
    print(f"Failed to get custom fields: {e}")

# Update custom fields
try:
    client.reservations.update_custom_fields(
        stay_code=stay_code,
        custom_fields={
            "lock_code": "9876",
            "wifi_password": "GuestWiFi2024",
            "parking_spot": "A-15",
            "special_instructions": "Key pickup from lockbox"
        }
    )
    print("Custom fields updated successfully")
except Exception as e:
    print(f"Failed to update custom fields: {e}")

# Delete a custom field (set to null)
try:
    client.reservations.update_custom_fields(
        stay_code=stay_code,
        custom_fields={
            "old_field_to_delete": None
        }
    )
    print("Custom field deleted")
except Exception as e:
    print(f"Failed to delete custom field: {e}")
```

### Using Custom Fields in Automated Messages

Custom fields can be referenced in Hostex automated messages using the syntax `{{cf.field_name}}`:

```python
# Example: Set lock code that can be used in automated messages
stay_code = "0-1234567-abcdef"

# Set custom field
client.reservations.update_custom_fields(
    stay_code=stay_code,
    custom_fields={
        "door_code": "1234",
        "wifi_name": "PropertyWiFi",
        "wifi_password": "SecurePass123"
    }
)

# In your Hostex automated message template, you can now use:
# "Welcome! Your door code is {{cf.door_code}}. 
#  WiFi: {{cf.wifi_name}} / {{cf.wifi_password}}"
```

## Error Handling

### Comprehensive Error Handling

```python
from hostex.exceptions import (
    HostexAPIError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    NotFoundError
)
import time

def robust_api_call(client, operation, max_retries=3, base_delay=1):
    """
    Make an API call with comprehensive error handling and retries
    """
    for attempt in range(max_retries + 1):
        try:
            return operation()
            
        except RateLimitError as e:
            if attempt == max_retries:
                print(f"Rate limit exceeded after {max_retries} attempts")
                raise
            
            wait_time = getattr(e, 'retry_after', base_delay * (2 ** attempt))
            print(f"Rate limited. Waiting {wait_time} seconds before retry...")
            time.sleep(wait_time)
            
        except AuthenticationError as e:
            print(f"Authentication failed: {e.message}")
            # Try to refresh token if using OAuth
            if hasattr(client, 'refresh_token'):
                try:
                    client.refresh_access_token()
                    print("Token refreshed, retrying...")
                    continue
                except Exception:
                    print("Token refresh failed")
            raise
            
        except ValidationError as e:
            print(f"Validation error: {e.message}")
            print("Please check your request parameters")
            raise
            
        except NotFoundError as e:
            print(f"Resource not found: {e.message}")
            raise
            
        except HostexAPIError as e:
            if e.error_code >= 500:  # Server errors - retry
                if attempt == max_retries:
                    print(f"Server error after {max_retries} attempts: {e.message}")
                    raise
                wait_time = base_delay * (2 ** attempt)
                print(f"Server error. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:  # Client errors - don't retry
                print(f"API error {e.error_code}: {e.message}")
                raise
                
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            raise

# Usage examples
try:
    # Robust property listing
    properties = robust_api_call(
        client,
        lambda: client.properties.list(limit=100)
    )
    print(f"Successfully retrieved {len(properties['data']['properties'])} properties")
    
except Exception as e:
    print(f"Failed to retrieve properties: {e}")

try:
    # Robust reservation creation
    reservation = robust_api_call(
        client,
        lambda: client.reservations.create(
            property_id="12345",
            custom_channel_id=1,
            check_in_date="2024-07-01",
            check_out_date="2024-07-07",
            guest_name="John Doe",
            currency="USD",
            rate_amount=50000,
            commission_amount=5000,
            received_amount=45000,
            income_method_id=1
        )
    )
    print("Reservation created successfully")
    
except Exception as e:
    print(f"Failed to create reservation: {e}")
```

### Batch Operations with Error Handling

```python
def batch_update_availability(client, updates, batch_size=10):
    """
    Update availability for multiple properties in batches
    """
    results = []
    
    for i in range(0, len(updates), batch_size):
        batch = updates[i:i + batch_size]
        print(f"Processing batch {i//batch_size + 1}/{(len(updates)-1)//batch_size + 1}")
        
        for update in batch:
            try:
                result = robust_api_call(
                    client,
                    lambda: client.availabilities.update(**update)
                )
                results.append({
                    'success': True,
                    'update': update,
                    'result': result
                })
                print(f"✓ Updated availability for property {update['property_ids']}")
                
            except Exception as e:
                results.append({
                    'success': False,
                    'update': update,
                    'error': str(e)
                })
                print(f"✗ Failed to update property {update['property_ids']}: {e}")
        
        # Small delay between batches to respect rate limits
        time.sleep(1)
    
    # Summary
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    print(f"\nBatch update complete: {successful} successful, {failed} failed")
    
    return results

# Usage
availability_updates = [
    {
        'property_ids': [12345],
        'start_date': '2024-07-01',
        'end_date': '2024-07-07',
        'available': False
    },
    {
        'property_ids': [67890],
        'dates': ['2024-07-15', '2024-07-16'],
        'available': True
    },
    # ... more updates
]

results = batch_update_availability(client, availability_updates)
```

This comprehensive examples document shows how to use all major features of the hostex-python library with proper error handling and real-world scenarios.