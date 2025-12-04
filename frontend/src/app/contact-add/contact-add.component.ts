/**
 * Contact Add Component
 * 
 * Form component for creating new emergency contacts.
 * Features:
 * - Reactive form with validation
 * - Country code dropdown
 * - Notification groups with tag-based input
 * - Event types selection
 * - Status selection
 * 
 * Uses Angular reactive forms for form management and validation.
 * 
 * @author Enterprise Emergency Contacts Team
 */

import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormArray, FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ContactService } from '../contact.service';
import { Contact, COUNTRY_CODES, CountryCode } from '../contact';

@Component({
  selector: 'app-contact-add',
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './contact-add.component.html',
  styleUrl: './contact-add.component.css',
  host: {
    'role': 'main',
    'aria-label': 'Create enterprise emergency contact'
  }
})
export class ContactAddComponent {
  // Dependency injection
  private fb = inject(FormBuilder);
  private contactService = inject(ContactService);
  private router = inject(Router);

  // Form and state management
  contactForm: FormGroup; // Reactive form group
  countryCodes = COUNTRY_CODES; // Available country codes for dropdown
  selectedGroups = signal<string[]>([]); // Selected notification groups
  groupInput = signal(''); // Input value for adding new groups
  loading = signal(false); // Loading state during submission
  errorMessage = signal<string | null>(null); // Error message to display

  // Available event types for selection
  eventTypes = [
    { value: 'SOS', label: 'SOS' },
    { value: '911', label: '911' },
    { value: 'TIMER', label: 'Timer' },
    { value: 'SAFEWALK', label: 'Safe Walk' }
  ];

  constructor() {
    // Initialize reactive form with validators
    this.contactForm = this.fb.group({
      first_name: ['', [Validators.required, Validators.maxLength(100)]],
      last_name: ['', [Validators.required, Validators.maxLength(100)]],
      email: ['', [Validators.required, Validators.email, Validators.maxLength(255)]],
      country_code: ['+1'],
      mobile_number: ['', [Validators.pattern(/^\d{10}$/)]],
      event_notification_type: ['ALL_USERS', Validators.required],
      event_types: this.fb.array([
        this.fb.control(false),
        this.fb.control(false),
        this.fb.control(false),
        this.fb.control(false)
      ]),
      status: ['ACTIVE', Validators.required]
    });

    // Watch for notification type changes - clear groups when switching to ALL_USERS
    this.contactForm.get('event_notification_type')?.valueChanges.subscribe(value => {
      if (value === 'ALL_USERS') {
        this.selectedGroups.set([]);
      }
    });
  }

  /**
   * Getter for event types FormArray
   * Used in template to bind checkboxes
   */
  get eventTypesFormArray(): FormArray {
    return this.contactForm.get('event_types') as FormArray;
  }

  /**
   * Getter for current notification type
   */
  get notificationType(): string {
    return this.contactForm.get('event_notification_type')?.value || 'ALL_USERS';
  }

  /**
   * Check if "Select Notification Groups" option is selected
   */
  get isGroupsSelected(): boolean {
    return this.notificationType === 'GROUPS';
  }

  /**
   * Adds a new notification group to the selected groups list
   * Prevents duplicates
   */
  addGroup(): void {
    const group = this.groupInput().trim();
    if (group && !this.selectedGroups().includes(group)) {
      this.selectedGroups.update(groups => [...groups, group]);
      this.groupInput.set('');
    }
  }

  /**
   * Removes a notification group from the selected groups list
   * 
   * @param group - Group name to remove
   */
  removeGroup(group: string): void {
    this.selectedGroups.update(groups => groups.filter(g => g !== group));
  }

  /**
   * Handles Enter key press in group input field
   * Adds the group when Enter is pressed
   * 
   * @param event - Keyboard event
   */
  onGroupInputKeydown(event: KeyboardEvent): void {
    if (event.key === 'Enter') {
      event.preventDefault();
      this.addGroup();
    }
  }

  /**
   * Handles form submission
   * Validates form, prepares data, and sends to API
   * Navigates to contact list on success
   */
  onSubmit(): void {
    if (this.contactForm.invalid) {
      this.markFormGroupTouched(this.contactForm);
      return;
    }

    const formValue = this.contactForm.value;
    const selectedEventTypes = this.eventTypes
      .filter((_, index) => this.eventTypesFormArray.at(index).value)
      .map(et => et.value);

    if (selectedEventTypes.length === 0) {
      this.errorMessage.set('Please select at least one event type.');
      return;
    }

    const contactData: Contact = {
      first_name: formValue.first_name.trim(),
      last_name: formValue.last_name.trim(),
      email: formValue.email.trim().toLowerCase(),
      country_code: formValue.mobile_number ? formValue.country_code : undefined,
      mobile_number: formValue.mobile_number || '',
      event_notification_type: formValue.event_notification_type,
      event_notification_groups: this.isGroupsSelected ? this.selectedGroups() : undefined,
      event_types: selectedEventTypes,
      status: formValue.status
    };

    this.loading.set(true);
    this.errorMessage.set(null);

    this.contactService.createContact(contactData).subscribe({
      next: () => {
        this.router.navigate(['/contacts']);
      },
      error: (error) => {
        this.errorMessage.set('Failed to create contact. Please try again.');
        this.loading.set(false);
        console.error('Error creating contact:', error);
      }
    });
  }

  onCancel(): void {
    this.router.navigate(['/contacts']);
  }

  private markFormGroupTouched(formGroup: FormGroup): void {
    Object.keys(formGroup.controls).forEach(key => {
      const control = formGroup.get(key);
      control?.markAsTouched();
      if (control instanceof FormGroup) {
        this.markFormGroupTouched(control);
      }
    });
  }

  getFieldError(fieldName: string): string | null {
    const field = this.contactForm.get(fieldName);
    if (field?.errors && field.touched) {
      if (field.errors['required']) {
        return `${fieldName.replace('_', ' ')} is required`;
      }
      if (field.errors['email']) {
        return 'Please enter a valid email address';
      }
      if (field.errors['pattern']) {
        return 'Please enter a valid 10-digit mobile number';
      }
      if (field.errors['maxLength']) {
        return `${fieldName.replace('_', ' ')} is too long`;
      }
    }
    return null;
  }

  isFieldInvalid(fieldName: string): boolean {
    const field = this.contactForm.get(fieldName);
    return !!(field?.invalid && field.touched);
  }
}
