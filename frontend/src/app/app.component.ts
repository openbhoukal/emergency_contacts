import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
  host: {
    'role': 'application',
    'aria-label': 'Enterprise Emergency Contacts Application'
  }
})
export class AppComponent {
  title = 'Emergency Contacts';
}
