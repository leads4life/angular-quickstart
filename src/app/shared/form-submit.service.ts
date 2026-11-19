import { Injectable } from '@angular/core';

/**
 * Posts a form to Netlify Forms (the site is deployed on Netlify).
 * Each form name must also exist as a hidden static form in src/index.html
 * so Netlify detects it at deploy time.
 */
@Injectable({ providedIn: 'root' })
export class FormSubmitService {
  async send(formName: string, data: Record<string, unknown>): Promise<boolean> {
    const body = new URLSearchParams({ 'form-name': formName });
    for (const [key, value] of Object.entries(data)) {
      if (value !== null && value !== undefined) {
        body.append(key, String(value));
      }
    }
    try {
      const res = await fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: body.toString(),
      });
      return res.ok;
    } catch {
      return false;
    }
  }
}
