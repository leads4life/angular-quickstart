import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { SITE } from '../site.data';

@Component({
  selector: 'app-logo',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <span class="logo" [class.logo--stacked]="stacked">
      <svg class="logo-mark" viewBox="0 0 64 52" aria-hidden="true" focusable="false">
        <path fill="var(--gold)" d="M32 1l2.4 5h-4.8z"/>
        <path fill="var(--gold)" d="M12 15Q32 3 52 15Q46 13.5 41 16H23Q18 13.5 12 15Z"/>
        <rect fill="var(--crimson)" x="22" y="16" width="20" height="7"/>
        <path fill="var(--gold)" d="M2 30Q32 17 62 30Q54 27.5 47 31H17Q10 27.5 2 30Z"/>
        <rect fill="var(--crimson)" x="14" y="31" width="3.2" height="15"/>
        <rect fill="var(--crimson)" x="25.5" y="31" width="3.2" height="15"/>
        <rect fill="var(--crimson)" x="35.3" y="31" width="3.2" height="15"/>
        <rect fill="var(--crimson)" x="46.8" y="31" width="3.2" height="15"/>
        <rect fill="var(--gold)" x="7" y="46" width="50" height="3.5" rx="1"/>
      </svg>
      <span class="logo-text">
        <span class="logo-name">{{ site.name }}</span>
        <span class="logo-tag">{{ site.tagline }}</span>
      </span>
      <span class="logo-seal" aria-hidden="true">金<br>苑</span>
    </span>`,
})
export class LogoComponent {
  @Input() stacked = false;
  readonly site = SITE;
}
