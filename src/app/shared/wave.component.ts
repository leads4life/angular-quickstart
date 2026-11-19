import { ChangeDetectionStrategy, Component, Input } from '@angular/core';

/**
 * Flowing section divider with a brushed-gold edge.
 * Place it at the top of the section whose colour it should carry (`fill`);
 * it overlaps upward into the previous section.
 */
@Component({
  selector: 'app-wave',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `<svg viewBox="0 0 1440 120" preserveAspectRatio="none" aria-hidden="true" focusable="false">
    <path [attr.fill]="fill" [attr.d]="shape + ' L1440,124 L0,124 Z'"></path>
    <path class="wave-gold" fill="none" [attr.d]="shape"></path>
  </svg>`,
})
export class WaveComponent {
  @Input() fill = 'var(--cream)';
  @Input() variant: 'a' | 'b' = 'a';

  get shape(): string {
    return this.variant === 'a'
      ? 'M0,72 C300,8 620,8 880,52 C1110,92 1290,84 1440,34'
      : 'M0,40 C220,92 520,98 780,60 C1020,24 1240,18 1440,62';
  }
}
