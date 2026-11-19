import { ChangeDetectorRef, Component, Input } from '@angular/core';
import { NgForm } from '@angular/forms';
import { SITE } from '../site.data';
import { FormSubmitService } from './form-submit.service';

type Status = 'idle' | 'sending' | 'sent' | 'error';

@Component({
  selector: 'app-inquiry-form',
  templateUrl: './inquiry-form.component.html',
})
export class InquiryFormComponent {
  /** Netlify form name; must match a hidden form in src/index.html. */
  @Input() formName = 'contact';
  @Input() submitLabel = 'Send Message';
  /** Adds event date and guest count fields. */
  @Input() eventFields = false;
  /** Adds the "Inquiry Type" select (contact page). */
  @Input() inquiryTypes: string[] = [];
  @Input() messagePlaceholder = 'Your Message';

  status: Status = 'idle';
  readonly site = SITE;
  readonly today = new Date().toISOString().slice(0, 10);

  constructor(private forms: FormSubmitService, private cdr: ChangeDetectorRef) {}

  async submit(form: NgForm): Promise<void> {
    if (form.invalid) {
      form.control.markAllAsTouched();
      return;
    }
    // Honeypot: bots fill the hidden field, people don't.
    if (form.value['bot-field']) {
      return;
    }
    this.status = 'sending';
    const ok = await this.forms.send(this.formName, form.value);
    this.status = ok ? 'sent' : 'error';
    if (ok) {
      form.resetForm();
    }
    this.cdr.markForCheck();
  }
}
