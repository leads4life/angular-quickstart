import { Component } from '@angular/core';
import { SITE } from '../site.data';

@Component({ selector: 'app-contact', templateUrl: './contact.component.html' })
export class ContactComponent {
  readonly site = SITE;
  readonly inquiryTypes = ['General Question', 'Reservations', 'Private Events', 'Catering', 'Feedback'];
}
