/**
 * Contact Model and Interfaces
 * 
 * Defines the data structures for emergency contacts and related entities.
 * 
 * @author Enterprise Emergency Contacts Team
 */

/**
 * Emergency Contact interface
 * Represents a single emergency contact in the system
 */
export interface Contact {
  id?: number; // Contact ID (optional for new contacts)
  first_name: string; // Contact's first name
  last_name: string; // Contact's last name
  email: string; // Contact's email address
  country_code?: string; // Country dial code (e.g., "+1", "+91")
  mobile_number: string; // Mobile number (10 digits, without country code)
  event_notification_type: 'ALL_USERS' | 'GROUPS'; // Notification type
  event_notification_groups?: string[]; // Array of notification group names (if type is GROUPS)
  event_types: string[]; // Array of event types: 'SOS', '911', 'TIMER', 'SAFEWALK'
  status: 'ACTIVE' | 'INACTIVE'; // Contact status
  created_at?: string; // ISO timestamp of creation
  updated_at?: string; // ISO timestamp of last update
}

/**
 * Country code interface
 * Represents a country with its dial code
 */
export interface CountryCode {
  code: string; // ISO country code (e.g., "US", "IN")
  name: string; // Country name (e.g., "United States")
  dialCode: string; // Dial code with + (e.g., "+1")
}

/**
 * Available country codes for mobile number selection
 * Can be extended to include more countries as needed
 */
export const COUNTRY_CODES: CountryCode[] = [
  { code: 'US', name: 'United States', dialCode: '+1' },
  { code: 'IN', name: 'India', dialCode: '+91' },
  { code: 'GB', name: 'United Kingdom', dialCode: '+44' },
  { code: 'CA', name: 'Canada', dialCode: '+1' },
  { code: 'AU', name: 'Australia', dialCode: '+61' },
  { code: 'DE', name: 'Germany', dialCode: '+49' },
  { code: 'FR', name: 'France', dialCode: '+33' },
  { code: 'JP', name: 'Japan', dialCode: '+81' },
  { code: 'CN', name: 'China', dialCode: '+86' },
  { code: 'BR', name: 'Brazil', dialCode: '+55' }
];
