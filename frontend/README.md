# Enterprise Emergency Contacts - Frontend Application

A modern Angular application for managing enterprise emergency contacts. Built with Angular 20+, TypeScript, and following best practices for accessibility, performance, and maintainability.

## Features

- 📋 **Contact List View**: Display all contacts with search, filter, sort, and pagination
- ➕ **Create Contact**: Add new emergency contacts with comprehensive form validation
- ✏️ **Edit Contact**: Update existing contacts with pre-filled forms
- 🗑️ **Delete Contact**: Remove contacts with confirmation
- 🔍 **Search & Filter**: Search by name, email, or mobile; filter by status
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile devices
- ♿ **Accessibility**: WCAG AA compliant with full keyboard navigation and screen reader support
- 🌍 **Country Codes**: Support for multiple country codes in mobile numbers
- 👥 **Notification Groups**: Tag-based notification group selection

## Prerequisites

Before you begin, ensure you have the following installed:

### For Ubuntu/Debian:

```bash
# Update package list
sudo apt update

# Install Node.js (version 20.x or higher)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version  # Should show v20.x.x or higher
npm --version   # Should show 10.x.x or higher

# Install Angular CLI globally
sudo npm install -g @angular/cli@20
```

### For Windows:

1. **Download Node.js**:
   - Visit [https://nodejs.org/](https://nodejs.org/)
   - Download the LTS version (20.x or higher)
   - Run the installer and follow the setup wizard
   - Make sure to check "Add to PATH" during installation

2. **Verify Installation**:
   - Open Command Prompt or PowerShell
   - Run:
     ```cmd
     node --version
     npm --version
     ```

3. **Install Angular CLI**:
   - Open Command Prompt or PowerShell as Administrator
   - Run:
     ```cmd
     npm install -g @angular/cli@20
     ```

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```
   
   If you encounter dependency conflicts, use:
   ```bash
   npm install --legacy-peer-deps
   ```

## Configuration

1. **Update API URL** (if needed):
   - Open `src/environments/environment.ts`
   - Update the `apiUrl` to match your Django backend URL:
     ```typescript
     export const environment = {
       production: false,
       apiUrl: 'http://localhost:8000/api'  // Change this to your backend URL
     };
     ```

2. **Verify Backend is Running**:
   - Ensure your Django REST API backend is running
   - Default URL: `http://localhost:8000/api`
   - The API should be accessible at: `http://localhost:8000/api/items/`

## Running the Application

### Development Server

Start the development server:

```bash
npm start
```

Or use the Angular CLI directly:

```bash
ng serve
```

The application will be available at:
- **URL**: `http://localhost:4200`
- The browser will automatically open (if configured)

### Build for Production

Create a production build:

```bash
npm run build
```

The build artifacts will be stored in the `dist/` directory.

### Running Tests

Run unit tests:

```bash
npm test
```

### Linting

Check code quality:

```bash
npm run lint
```

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── contact-list/          # Contact list component
│   │   ├── contact-add/           # Add contact component
│   │   ├── contact-edit/          # Edit contact component
│   │   ├── contact.service.ts     # API service
│   │   ├── contact.ts             # Contact model/interfaces
│   │   ├── app.component.ts       # Root component
│   │   └── app.routes.ts          # Route configuration
│   ├── environments/              # Environment configuration
│   ├── index.html                 # Main HTML file
│   ├── main.ts                    # Application entry point
│   └── styles.css                 # Global styles
├── angular.json                   # Angular configuration
├── package.json                   # Dependencies and scripts
├── tsconfig.json                  # TypeScript configuration
└── README.md                      # This file
```

## API Integration

The application expects the Django REST API to return data in the following format:

### Get All Contacts (Paginated)
```
GET /api/items/
Response: {
  "count": 2,
  "next": null,
  "previous": null,
  "results": [...]
}
```

### Get Single Contact
```
GET /api/items/{id}/
Response: {
  "id": 1,
  "first_name": "...",
  ...
}
```

### Create Contact
```
POST /api/items/
Body: {
  "first_name": "...",
  "last_name": "...",
  "email": "...",
  "country_code": "+1",
  "mobile_number": "1234567890",
  "event_notification_type": "ALL_USERS" | "GROUPS",
  "event_notification_groups": ["Group1", "Group2"],
  "event_types": ["SOS", "911"],
  "status": "ACTIVE" | "INACTIVE"
}
```

### Update Contact
```
PUT /api/items/{id}/
Body: (same as Create)
```

### Delete Contact
```
DELETE /api/items/{id}/
```

## Troubleshooting

### Port Already in Use

If port 4200 is already in use:

```bash
# Ubuntu/Windows
ng serve --port 4201
```

### CORS Issues

If you encounter CORS errors when connecting to the backend:

1. Ensure your Django backend has CORS configured
2. Check that the API URL in `environment.ts` is correct
3. Verify the backend is running and accessible

### Dependency Installation Issues

If `npm install` fails:

```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json  # Ubuntu
# or
rmdir /s node_modules & del package-lock.json  # Windows

# Reinstall
npm install --legacy-peer-deps
```

### TypeScript Errors

If you see TypeScript compilation errors:

1. Ensure TypeScript version is 5.8.0 or higher:
   ```bash
   npm list typescript
   ```

2. Update if needed:
   ```bash
   npm install typescript@~5.8.0 --save-dev
   ```

### Build Errors

If production build fails:

1. Check for TypeScript errors:
   ```bash
   npm run lint
   ```

2. Ensure all dependencies are installed:
   ```bash
   npm install
   ```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Development Guidelines

### Code Style

- Follow Angular style guide
- Use TypeScript strict mode
- Use signals for state management
- Use reactive forms
- Follow accessibility best practices

### Component Structure

- Standalone components (no NgModules)
- Use `inject()` for dependency injection
- Use signals for reactive state
- Use computed signals for derived state

### Accessibility

- All interactive elements have ARIA labels
- Keyboard navigation supported
- Screen reader compatible
- WCAG AA compliant

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Angular documentation: [https://angular.io/docs](https://angular.io/docs)
3. Check browser console for error messages

## License

This project is part of the Enterprise Emergency Contacts system.

---

**Last Updated**: December 2024
**Angular Version**: 20.0.0
**Node.js Version**: 20.x or higher
