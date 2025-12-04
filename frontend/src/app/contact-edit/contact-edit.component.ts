/**
 * Contact Edit Component
 * 
 * Form component for editing existing emergency contacts.
 * Features:
 * - Pre-fills form with existing contact data
 * - Reactive form with validation
 * - Country code dropdown
 * - Notification groups with tag-based input
 * - Event types selection
 * - Status selection
 * 
 * Loads contact data by ID from route parameter and populates the form.
 * 
 * @author Enterprise Emergency Contacts Team
 */

import { Component, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormArray, FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ContactService } from '../contact.service';
import { Contact, COUNTRY_CODES } from '../contact';

@Component({
  selector: 'app-contact-edit',
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './contact-edit.component.html',
  styleUrl: './contact-edit.component.css',
  host: {
    'role': 'main',
    'aria-label': 'Edit enterprise emergency contact'
  }
})
export class ContactEditComponent {
  private fb = inject(FormBuilder);
  private contactService = inject(ContactService);
  private route = inject(ActivatedRoute);
  private router = inject(Router);

  contactForm: FormGroup;
  countryCodes = COUNTRY_CODES;
  selectedGroups = signal<string[]>([]);
  groupInput = signal('');
  loading = signal(false);
  loadingData = signal(true);
  errorMessage = signal<string | null>(null);
  successMessage = signal<string | null>(null);

  eventTypes = [
    { value: 'SOS', label: 'SOS' },
    { value: '911', label: '911' },
    { value: 'TIMER', label: 'Timer' },
    { value: 'SAFEWALK', label: 'Safe Walk' }
  ];

  constructor() {
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

    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (id) {
      this.loadContact(id);
    }

    // Watch for notification type changes
    this.contactForm.get('event_notification_type')?.valueChanges.subscribe(value => {
      if (value === 'ALL_USERS') {
        this.selectedGroups.set([]);
      }
    });
  }

  get eventTypesFormArray(): FormArray {
    return this.contactForm.get('event_types') as FormArray;
  }

  get notificationType(): string {
    return this.contactForm.get('event_notification_type')?.value || 'ALL_USERS';
  }

  get isGroupsSelected(): boolean {
    return this.notificationType === 'GROUPS';
  }

  /**
   * Loads contact data from API by ID
   * Handles loading state and errors
   * 
   * @param id - Contact ID to load
   */
  loadContact(id: number): void {
    this.loadingData.set(true);
    this.errorMessage.set(null);
    this.contactService.getContact(id).subscribe({
      next: (contact) => {
        this.populateForm(contact);
        this.loadingData.set(false);
      },
      error: (error) => {
        this.errorMessage.set('Failed to load contact. Please try again.');
        this.loadingData.set(false);
        console.error('Error loading contact:', error);
      }
    });
  }

  /**
   * Populates the form with existing contact data
   * Handles country code parsing, notification groups, and event types
   * 
   * @param contact - Contact data from API
   */
  populateForm(contact: Contact): void {
    // Extract country code from mobile number if present
    let countryCode = '+1';
    let mobileNumber = contact.mobile_number || '';

    if (contact.country_code) {
      countryCode = contact.country_code;
    } else if (mobileNumber && mobileNumber.startsWith('+')) {
      const match = mobileNumber.match(/^(\+\d{1,3})/);
      if (match) {
        countryCode = match[1];
        mobileNumber = mobileNumber.substring(match[1].length);
      }
    }

    // Parse notification groups
    if (contact.event_notification_groups) {
      if (Array.isArray(contact.event_notification_groups)) {
        this.selectedGroups.set([...contact.event_notification_groups]);
      } else {
        // Handle case where API might return string instead of array
        const groupsStr = contact.event_notification_groups as unknown as string;
        if (typeof groupsStr === 'string') {
          const groups = groupsStr.split(',').map((g: string) => g.trim()).filter((g: string) => g.length > 0);
          this.selectedGroups.set(groups);
        }
      }
    }

    // Set event types checkboxes
    const eventTypesArray = this.eventTypesFormArray;
    this.eventTypes.forEach((et, index) => {
      eventTypesArray.at(index).setValue(contact.event_types?.includes(et.value) || false);
    });

    this.contactForm.patchValue({
      first_name: contact.first_name,
      last_name: contact.last_name,
      email: contact.email,
      country_code: countryCode,
      mobile_number: mobileNumber,
      event_notification_type: contact.event_notification_type || 'ALL_USERS',
      status: contact.status || 'ACTIVE'
    });
  }

  addGroup(): void {
    const group = this.groupInput().trim();
    if (group && !this.selectedGroups().includes(group)) {
      this.selectedGroups.update(groups => [...groups, group]);
      this.groupInput.set('');
    }
  }

  removeGroup(group: string): void {
    this.selectedGroups.update(groups => groups.filter(g => g !== group));
  }

  onGroupInputKeydown(event: KeyboardEvent): void {
    if (event.key === 'Enter') {
      event.preventDefault();
      this.addGroup();
    }
  }

  onSubmit(): void {
    if (this.contactForm.invalid) {
      this.markFormGroupTouched(this.contactForm);
      return;
    }

    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (!id) {
      this.errorMessage.set('Invalid contact ID.');
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
      id,
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

    this.contactService.updateContact(id, contactData).subscribe({
      next: () => {
        this.successMessage.set('Contact updated successfully.');
        setTimeout(() => {
          this.router.navigate(['/contacts']);
        }, 1500);
      },
      error: (error) => {
        this.errorMessage.set('Failed to update contact. Please try again.');
        this.loading.set(false);
        console.error('Error updating contact:', error);
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
