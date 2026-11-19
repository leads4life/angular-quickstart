import { ChangeDetectionStrategy, Component, Input } from '@angular/core';

/** Dark cinematic hero used at the top of every page. Buttons are projected. */
@Component({
  selector: 'app-page-hero',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <section class="hero" [class.hero--home]="large">
      <img class="hero-img" [src]="image" alt="" fetchpriority="high">
      <img *ngIf="blossom" class="hero-blossom" src="assets/img/blossom.svg" alt="">
      <div class="container hero-content">
        <p class="eyebrow" *ngIf="eyebrow">{{ eyebrow }}</p>
        <h1>{{ title }} <em *ngIf="accent">{{ accent }}</em></h1>
        <p class="lead" *ngIf="lead">{{ lead }}</p>
        <div class="hero-actions"><ng-content></ng-content></div>
      </div>
    </section>
    <app-wave></app-wave>`,
})
export class PageHeroComponent {
  @Input() eyebrow = '';
  @Input() title = '';
  @Input() accent = '';
  @Input() lead = '';
  @Input() image = '';
  @Input() large = false;
  @Input() blossom = false;
}
