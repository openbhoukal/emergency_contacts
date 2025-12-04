/**
 * Contact Service
 * 
 * This service handles all HTTP communication with the Django REST API backend.
 * It provides methods for CRUD operations on emergency contacts.
 * 
 * @author Enterprise Emergency Contacts Team
 */

import { inject, Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpParams } from '@angular/common/http';
import { Observable, catchError, throwError } from 'rxjs';
import { Contact } from './contact';
import { environment } from '../environments/environment';

/**
 * Generic API response interface (for future use)
 */
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

/**
 * Paginated response interface for Django REST Framework pagination
 * The backend API returns paginated results in this format
 */
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

/**
 * Service for managing emergency contacts via REST API
 * Uses Angular's dependency injection with providedIn: 'root' for singleton pattern
 */
@Injectable({
  providedIn: 'root'
})
export class ContactService {
  private http = inject(HttpClient);
  private baseUrl = `${environment.apiUrl}/items/`;

  /**
   * Fetches all contacts from the backend API
   * Handles paginated response and extracts the results array
   * 
   * @returns Observable of Contact array
   */
  getContacts(params?: Record<string, string | number | boolean>): Observable<PaginatedResponse<Contact>> {
    let httpParams = new HttpParams();

    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          httpParams = httpParams.set(key, String(value));
        }
      });
    }

    return this.http.get<PaginatedResponse<Contact>>(this.baseUrl, { params: httpParams }).pipe(
      catchError(
        this.handleError<PaginatedResponse<Contact>>('getContacts', {
          count: 0,
          next: null,
          previous: null,
          results: []
        })
      )
    );
  }

  /**
   * Fetches a single contact by ID
   * 
   * @param id - The contact ID to fetch
   * @returns Observable of Contact
   */
  getContact(id: number): Observable<Contact> {
    return this.http.get<Contact>(`${this.baseUrl}${id}/`).pipe(
      catchError(this.handleError<Contact>('getContact'))
    );
  }

  /**
   * Creates a new emergency contact
   * 
   * @param data - Contact data to create
   * @returns Observable of created Contact
   */
  createContact(data: Contact): Observable<Contact> {
    return this.http.post<Contact>(this.baseUrl, data).pipe(
      catchError(this.handleError<Contact>('createContact'))
    );
  }

  /**
   * Updates an existing emergency contact
   * 
   * @param id - The contact ID to update
   * @param data - Updated contact data
   * @returns Observable of updated Contact
   */
  updateContact(id: number, data: Contact): Observable<Contact> {
    return this.http.put<Contact>(`${this.baseUrl}${id}/`, data).pipe(
      catchError(this.handleError<Contact>('updateContact'))
    );
  }

  /**
   * Deletes an emergency contact
   * 
   * @param id - The contact ID to delete
   * @returns Observable of void
   */
  deleteContact(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}${id}/`).pipe(
      catchError(this.handleError<void>('deleteContact'))
    );
  }

  /**
   * Generic error handler for HTTP requests
   * Logs errors and returns a user-friendly error message
   * 
   * @param operation - Name of the operation that failed
   * @param result - Optional default value to return on error
   * @returns Error handler function
   */
  private handleError<T>(operation = 'operation', result?: T) {
    return (error: HttpErrorResponse): Observable<T> => {
      console.error(`${operation} failed:`, error);
      return throwError(() => new Error(error.message || `${operation} failed`));
    };
  }
}
