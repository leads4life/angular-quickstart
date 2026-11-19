import { ChangeDetectionStrategy, Component, HostBinding, Input } from '@angular/core';

/** Dark cinematic hero; its lower edge bleeds into the rice paper. Buttons are projected. */
@Component({
  selector: 'app-page-hero',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <section class="hero" [class.hero--home]="large" [class.hero--flush]="!bleed">
      <img class="hero-img" [src]="image" alt="" fetchpriority="high">
      <img *ngIf="blossom" class="hero-blossom" src="assets/img/blossom.svg" alt="">
      <div class="container hero-content">
        <p class="eyebrow" *ngIf="eyebrow">{{ eyebrow }}</p>
        <h1>{{ title }} <em *ngIf="accent">{{ accent }}</em></h1>
        <p class="lead" *ngIf="lead">{{ lead }}</p>
        <div class="hero-actions"><ng-content></ng-content></div>
      </div>
    </section>`,
})
export class PageHeroComponent {
  @Input() eyebrow = '';
  @Input() title = '';
  @Input() accent = '';
  @Input() lead = '';
  @Input() image = '';
  @Input() large = false;
  @Input() blossom = false;
  /** Off when the footer follows directly (its own ink edge carries that seam). */
  @Input() bleed = true;

  @HostBinding('class.flush') get flush(): boolean {
    return !this.bleed;
  }
}
