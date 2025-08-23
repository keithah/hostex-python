# Hostex API Documentation

## Overview

The Hostex API provides comprehensive management of property and reservation systems for property managers and hosts. This Python library wraps the Hostex API v3.0.0 (Beta).

**Base URL**: `https://api.hostex.io/v3`

## Authentication

### API Token Authentication
Each API request must include a valid `Hostex-Access-Token` in the request header:
```
Hostex-Access-Token: your_access_token_here
```

### OAuth Authentication
For software partners building SaaS platforms or third-party tools, OAuth 2.0 authentication is required.

## Core Endpoints

### 1. Properties

#### Query Properties
- **Endpoint**: `GET /properties`
- **Description**: Retrieves a comprehensive list of properties with details
- **Parameters**:
  - `offset` (int): Starting point for results (default: 0)
  - `limit` (int): Maximum results to return, max 100 (default: 20)
  - `id` (int): Filter by specific property ID

**Response Structure**:
```json
{
  "request_id": "string",
  "error_code": 200,
  "error_msg": "Success",
  "data": {
    "properties": [
      {
        "id": 12345,
        "title": "Beautiful Apartment",
        "channels": [
          {
            "channel_type": "airbnb",
            "listing_id": "airbnb_listing_123"
          }
        ],
        "address": "123 Main St",
        "longitude": "-122.4194",
        "latitude": "37.7749"
      }
    ],
    "total": 1
  }
}
```

### 2. Room Types

#### Query Room Types
- **Endpoint**: `GET /room_types`
- **Description**: Fetches details and lists of room types
- **Parameters**:
  - `offset` (int): Starting point (default: 0)
  - `limit` (int): Maximum results, max 100 (default: 20)

### 3. Reservations

#### Query Reservations
- **Endpoint**: `GET /reservations`
- **Description**: Provides detailed lookup of reservation information
- **Parameters**:
  - `reservation_code` (string): Filter by reservation code
  - `property_id` (int): Filter by property ID
  - `status` (string): Filter by reservation status
  - `start_check_in_date` (date): Check-in date range start (YYYY-MM-DD)
  - `end_check_in_date` (date): Check-in date range end (YYYY-MM-DD)
  - `start_check_out_date` (date): Check-out date range start (YYYY-MM-DD)
  - `end_check_out_date` (date): Check-out date range end (YYYY-MM-DD)
  - `order_by` (string): Sort field (default: 'booked_at')
  - `offset` (int): Starting index (default: 0)
  - `limit` (int): Maximum results, max 100 (default: 20)

**Reservation Status Values**:
- `wait_accept` - Waiting for acceptance
- `wait_pay` - Waiting for payment
- `accepted` - Accepted
- `cancelled` - Cancelled
- `denied` - Denied
- `timeout` - Timed out

#### Create Reservation
- **Endpoint**: `POST /reservations`
- **Description**: Creates a direct booking reservation in Hostex
- **Required Fields**:
  - `property_id` (string): Property ID
  - `custom_channel_id` (int): Custom channel ID
  - `check_in_date` (date): Check-in date (YYYY-MM-DD)
  - `check_out_date` (date): Check-out date (YYYY-MM-DD)
  - `guest_name` (string): Primary guest name
  - `currency` (string): Currency code
  - `rate_amount` (int): Total rate amount
  - `commission_amount` (int): Commission amount
  - `received_amount` (int): Total received amount
  - `income_method_id` (int): Income method identifier

#### Cancel Reservation
- **Endpoint**: `DELETE /reservations/{reservation_code}`
- **Description**: Cancel a direct booking reservation (channel bookings not supported)

#### Update Lock Code
- **Endpoint**: `PATCH /reservations/{stay_code}/check_in_details`
- **Description**: Update lock code for a stay
- **Body**: `{"lock_code": "string"}`

### 4. Availabilities

#### Query Property Availabilities
- **Endpoint**: `GET /availabilities`
- **Description**: Retrieves availability information for properties
- **Parameters**:
  - `property_ids` (string): Comma-separated property IDs (max 100)
  - `start_date` (date): Start date (YYYY-MM-DD, within 1 year)
  - `end_date` (date): End date (YYYY-MM-DD, within 3 years)

#### Update Property Availabilities
- **Endpoint**: `POST /availabilities`
- **Description**: Updates property availability status
- **Body Parameters**:
  - `property_ids` (array): Property IDs to update
  - `start_date` (date): Update start date (YYYY-MM-DD)
  - `end_date` (date): Update end date (YYYY-MM-DD)
  - `dates` (array): Specific dates list (alternative to date range)
  - `available` (boolean): Availability status

### 5. Listing Calendar

#### Query Listing Calendars
- **Endpoint**: `POST /listings/calendar`
- **Description**: Retrieves calendar information for multiple listings
- **Body Parameters**:
  - `start_date` (date): Calendar start date (YYYY-MM-DD)
  - `end_date` (date): Calendar end date (YYYY-MM-DD)
  - `listings` (array): List of listing objects with channel_type and listing_id

#### Update Listing Inventories
- **Endpoint**: `POST /listings/inventories`
- **Description**: Updates inventory levels for channel listings
- **Body Parameters**:
  - `channel_type` (string): Channel type
  - `listing_id` (string): Channel listing ID
  - `inventories` (array): Inventory update objects

#### Update Listing Prices
- **Endpoint**: `POST /listings/prices`
- **Description**: Modifies listing prices for channel listings
- **Body Parameters**:
  - `channel_type` (string): Channel type
  - `listing_id` (string): Channel listing ID
  - `prices` (array): Price update objects

#### Update Listing Restrictions
- **Endpoint**: `POST /listings/restrictions`
- **Description**: Alters listing restrictions for channel listings
- **Body Parameters**:
  - `channel_type` (string): Channel type
  - `listing_id` (string): Channel listing ID
  - `restrictions` (array): Restriction update objects

### 6. Messaging (Conversations)

#### Query Conversations
- **Endpoint**: `GET /conversations`
- **Description**: Retrieves list of guest conversations and inquiries
- **Parameters**:
  - `offset` (int): Starting index (default: 0)
  - `limit` (int): Maximum results, max 100 (default: 20)

#### Get Conversation Details
- **Endpoint**: `GET /conversations/{conversation_id}`
- **Description**: Provides messages and conversation details

#### Send Message
- **Endpoint**: `POST /conversations/{conversation_id}`
- **Description**: Sends a text or image message to a guest
- **Body Parameters**:
  - `message` (string): Text content
  - `jpeg_base64` (string): Base64 encoded JPEG image

### 7. Reviews

#### Query Reviews
- **Endpoint**: `GET /reviews`
- **Description**: Queries reviews similar to Hostex Reviews Page
- **Parameters**:
  - `reservation_code` (string): Filter by reservation code
  - `property_id` (int): Filter by property ID
  - `review_status` (string): Filter by review status (default: 'reviewed')
  - `start_check_out_date` (date): Check-out date range start
  - `end_check_out_date` (date): Check-out date range end
  - `offset` (int): Starting index (default: 0)
  - `limit` (int): Maximum results, max 100 (default: 20)

#### Create Review
- **Endpoint**: `POST /reviews/{reservation_code}`
- **Description**: Submits a review or reply for a reservation
- **Body Parameters**:
  - `host_review_score` (number): Rating score (0-5)
  - `host_review_content` (string): Review comment
  - `host_reply_content` (string): Reply to guest review

### 8. Custom Fields

#### Query Custom Fields
- **Endpoint**: `GET /reservations/{stay_code}/custom_fields`
- **Description**: Query custom fields for a stay

#### Update Custom Fields
- **Endpoint**: `PATCH /reservations/{stay_code}/custom_fields`
- **Description**: Update custom fields for a stay
- **Body**: `{"custom_fields": {"field_name": "field_value"}}`

### 9. Webhooks

#### Query Webhooks
- **Endpoint**: `GET /webhooks`
- **Description**: Lists configured webhooks

#### Create Webhook
- **Endpoint**: `POST /webhooks`
- **Description**: Creates a new webhook
- **Body**: `{"url": "https://your-endpoint.com/webhook"}`

#### Delete Webhook
- **Endpoint**: `DELETE /webhooks/{id}`
- **Description**: Deletes a webhook (only manageable ones)

### 10. Utility Endpoints

#### Query Custom Channels
- **Endpoint**: `GET /custom_channels`
- **Description**: Retrieves custom channels from Custom Options Page

#### Query Income Methods
- **Endpoint**: `GET /income_methods`
- **Description**: Retrieves income methods from Custom Options Page

## OAuth Endpoints

### Obtain/Refresh Tokens
- **Endpoint**: `POST /oauth/authorizations`
- **Description**: Obtain new access token or refresh existing token
- **Body Parameters**:
  - `client_id` (string): Client application ID
  - `client_secret` (string): Client secret
  - `grant_type` (string): 'authorization_code' or 'refresh_token'
  - `code` (string): Authorization code (for authorization_code grant)
  - `refresh_token` (string): Refresh token (for refresh_token grant)

### Revoke Tokens
- **Endpoint**: `POST /oauth/revoke`
- **Description**: Revokes access or refresh token
- **Body Parameters**:
  - `client_id` (string): Client application ID
  - `client_secret` (string): Client secret
  - `token` (string): Token to revoke

## Supported Channels

The following booking channels are supported:
- `airbnb` - Airbnb
- `booking.com` - Booking.com
- `agoda` - Agoda
- `expedia` - Expedia
- `vrbo` - VRBO
- `trip.com` - Trip.com
- `booking_site` - Hostex BookingSite
- `tujia_intl` - Tujia International
- `hostex_direct` - Direct bookings via Hostex
- `tujia` - Tujia
- `xiaozhu` - Xiaozhu
- `meituan_bnb` - Meituan BnB
- `meituan_hotel` - Meituan Hotel
- `muniao` - Muniao
- `fliggy` - Fliggy
- `zhukeyun` - Zhukeyun
- `tiktok` - TikTok
- `xiaohongshu` - Xiaohongshu (RED)
- `ctrip` - Ctrip
- `houfy` - Houfy

## Supported Currencies

Uses ISO 4217 currency codes. Supported currencies include:
AED, ARS, AUD, AWG, BAM, BBD, BGN, BHD, BND, BRL, BTN, BZD, CAD, CHF, CLP, CNY, COP, CRC, CZK, DKK, EUR, FJD, GBP, GTQ, GYD, HKD, HNL, HRK, HUF, IDR, ILS, INR, JMD, JOD, JPY, KRW, LAK, LKR, MAD, MOP, MXN, MYR, NOK, NZD, OMR, PEN, PGK, PHP, PLN, RON, RUB, SAR, SEK, SGD, THB, TRY, TTD, TWD, UAH, USD, UYU, VND, ZAR

## Error Codes

- `200` - Success
- `400` - Validation error
- `401` - Invalid API key or access token
- `403` - Insufficient permissions
- `404` - Resource not found
- `405` - Method not allowed
- `420` - User account issue
- `429` - Rate limit exceeded
- `500`/`503` - Internal server error

## Rate Limits

### Host-level Limits
- 1 minute: 1,200 requests (600 per endpoint)
- 5 minutes: 12,000 requests (6,000 per endpoint)  
- 1 hour: 20,000 requests (10,000 per endpoint)
- 1 day: 100,000 requests (50,000 per endpoint)

### API-level Limits
- `POST /availabilities`: 120/min per host
- `POST /listings/*`: 120/min per host
- `POST /reservations`: 60/min per host
- `POST /conversations/*`: 5/5 sec per host, 1,000/hr per host

## Webhook Events

Supported webhook event types:
- `reservation_created` - New reservation made
- `reservation_updated` - Existing reservation updated
- `property_availability_updated` - Property availability changed
- `listing_calendar_updated` - Listing calendar updated
- `message_created` - New message created
- `review_created` - Review created
- `review_updated` - Review updated

## Security Notes

- Always include `Hostex-Access-Token` header for authentication
- Set `User-Agent` header to your application name
- Verify `Hostex-Webhook-Secret-Token` for webhook authenticity
- Webhook endpoints must respond within 3 seconds
- Use HTTPS for all API requests
- Never expose client secrets or access tokens in client-side code