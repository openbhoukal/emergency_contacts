/**
 * Contact List Component
 * 
 * Displays all emergency contacts in a table format with:
 * - Search functionality
 * - Status filtering
 * - Column sorting
 * - Pagination
 * - Edit and Delete actions
 * 
 * Uses Angular signals for reactive state management and computed values
 * for derived state (filtered, sorted, and paginated contacts).
 * 
 * @author Enterprise Emergency Contacts Team
 */

import { Component, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ContactService } from '../contact.service';
import { Contact } from '../contact';

// Type definitions for sorting functionality
type SortField = 'first_name' | 'last_name' | 'email' | 'mobile_number' | 'status';
type SortDirection = 'asc' | 'desc';

@Component({
  selector: 'app-contact-list',
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './contact-list.component.html',
  styleUrl: './contact-list.component.css',
  host: {
    'role': 'main',
    'aria-label': 'Emergency contacts list'
  }
})
export class ContactListComponent {
  // Dependency injection using inject() function (Angular 20+)
  private contactService = inject(ContactService);
  private router = inject(Router);

  // State management using signals
  contacts = signal<Contact[]>([]); // Contacts for the current page
  searchTerm = signal(''); // Search input value
  statusFilter = signal<string>('all'); // Status filter: 'all', 'ACTIVE', or 'INACTIVE'
  sortField = signal<SortField | null>(null); // Current column being sorted
  sortDirection = signal<SortDirection>('asc'); // Sort direction
  currentPage = signal(1); // Current page number
  pageSize = signal(10); // Number of items per page (matches backend default)
  count = signal(0); // Total number of contacts available on the server
  hasNext = signal(false); // Whether another page is available after current
  hasPrevious = signal(false); // Whether previous page exists
  loading = signal(false); // Loading state
  errorMessage = signal<string | null>(null); // Error message to display
  successMessage = signal<string | null>(null); // Success message to display

  /**
   * Computed signal that calculates total number of pages
   * Based on count provided by the backend and configured page size
   */
  totalPages = computed(() => {
    if (this.count() === 0 || this.pageSize() === 0) {
      return 0;
    }
    return Math.ceil(this.count() / this.pageSize());
  });

  constructor() {
    // Load contacts when component initializes
    this.fetchContacts();
  }

  /**
   * Loads all contacts from the API
   * Handles loading state and error messages
   */
  fetchContacts(): void {
    this.loading.set(true);
    this.errorMessage.set(null);
    const params = this.buildQueryParams();

    this.contactService.getContacts(params).subscribe({
      next: (response) => {
        // If we requested a page beyond the last one (e.g., after deletions), step back
        if (response.results.length === 0 && response.count > 0 && this.currentPage() > 1) {
          this.currentPage.update(page => Math.max(1, page - 1));
          this.fetchContacts();
          return;
        }

        this.contacts.set(response.results);
        this.count.set(response.count);
        this.hasNext.set(Boolean(response.next));
        this.hasPrevious.set(Boolean(response.previous));
        this.loading.set(false);
      },
      error: (error) => {
        this.errorMessage.set('Failed to load contacts. Please try again.');
        this.loading.set(false);
        console.error('Error loading contacts:', error);
      }
    });
  }

  /**
   * Handles search input changes
   * Resets to first page when search term changes
   * 
   * @param value - New search term
   */
  onSearchChange(value: string): void {
    this.searchTerm.set(value);
    this.currentPage.set(1); // Reset to first page
    this.fetchContacts();
  }

  /**
   * Handles status filter changes
   * Resets to first page when filter changes
   * 
   * @param value - New filter value ('all', 'ACTIVE', or 'INACTIVE')
   */
  onStatusFilterChange(value: string): void {
    this.statusFilter.set(value);
    this.currentPage.set(1); // Reset to first page
    this.fetchContacts();
  }

  /**
   * Handles column sorting
   * Toggles sort direction if clicking the same column, otherwise sets new sort field
   * 
   * @param field - Column field to sort by
   */
  onSort(field: SortField): void {
    if (this.sortField() === field) {
      this.sortDirection.set(this.sortDirection() === 'asc' ? 'desc' : 'asc');
    } else {
      this.sortField.set(field);
      this.sortDirection.set('asc');
    }
    this.currentPage.set(1);
    this.fetchContacts();
  }

  /**
   * Clears all filters and resets to default state
   */
  clearFilters(): void {
    this.searchTerm.set('');
    this.statusFilter.set('all');
    this.sortField.set(null);
    this.currentPage.set(1);
    this.fetchContacts();
  }

  /**
   * Handles pagination page changes
   * Scrolls to top of page for better UX
   * 
   * @param page - Page number to navigate to
   */
  onPageChange(page: number): void {
    if (page < 1 || page === this.currentPage()) {
      return;
    }
    this.currentPage.set(page);
    this.fetchContacts();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  /**
   * Builds the query parameters used when requesting paginated data
   */
  private buildQueryParams(): Record<string, string> {
    const params: Record<string, string> = {
      page: this.currentPage().toString()
    };

    const searchValue = this.searchTerm().trim();
    if (searchValue) {
      params['search'] = searchValue;
    }

    const status = this.statusFilter();
    if (status !== 'all') {
      params['status'] = status;
    }

    const field = this.sortField();
    if (field) {
      params['ordering'] = this.sortDirection() === 'asc' ? field : `-${field}`;
    }

    return params;
  }

  /**
   * Deletes a contact after user confirmation
   * Shows success message and refreshes the list
   * 
   * @param id - Contact ID to delete
   */
  deleteContact(id: number | undefined): void {
    if (!id) return;
    
    if (confirm('Are you sure you want to delete this contact?')) {
      this.loading.set(true);
      this.errorMessage.set(null);
      this.contactService.deleteContact(id).subscribe({
        next: () => {
          this.successMessage.set('Contact deleted successfully.');
          this.fetchContacts();
          setTimeout(() => this.successMessage.set(null), 3000);
        },
        error: (error) => {
          this.errorMessage.set('Failed to delete contact. Please try again.');
          this.loading.set(false);
          console.error('Error deleting contact:', error);
        }
      });
    }
  }

  /**
   * Returns the appropriate sort icon for a column
   * 
   * @param field - Column field to get icon for
   * @returns Sort icon string (↕️ for unsorted, ↑ for ascending, ↓ for descending)
   */
  getSortIcon(field: SortField): string {
    if (this.sortField() !== field) return '↕️';
    return this.sortDirection() === 'asc' ? '↑' : '↓';
  }

  /**
   * Formats mobile number with country code for display
   * Handles cases where country code is separate or included in mobile number
   * 
   * @param contact - Contact object containing mobile number and country code
   * @returns Formatted mobile number string
   */
  formatMobileNumber(contact: Contact): string {
    if (!contact.mobile_number) return '-';
    if (contact.country_code) {
      return `${contact.country_code}-${contact.mobile_number}`;
    }
    // If mobile_number already starts with +, return as is
    if (contact.mobile_number.startsWith('+')) {
      return contact.mobile_number;
    }
    return contact.mobile_number;
  }

  /**
   * Formats event types array as comma-separated string for display
   * 
   * @param types - Array of event type strings
   * @returns Comma-separated string of event types
   */
  formatEventTypes(types: string[]): string {
    return types?.join(', ') || '';
  }
}
