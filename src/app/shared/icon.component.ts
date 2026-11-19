import { ChangeDetectionStrategy, Component, Input } from '@angular/core';

/** Circle as path data, so every icon is a plain list of <path d> strings. */
const c = (cx: number, cy: number, r: number) =>
  `M${cx - r} ${cy}a${r} ${r} 0 1 0 ${2 * r} 0a${r} ${r} 0 1 0 ${-2 * r} 0`;

const ICONS: Record<string, string[]> = {
  bowl: ['M3 11h18a9 9 0 0 1-18 0Z', 'M14 3l-4 7', 'M19 3l-5 7', 'M9 21h6'],
  bag: ['M5 8h14l-1 13H6L5 8Z', 'M9 8V6a3 3 0 0 1 6 0v2'],
  people: [c(12, 7, 2.8), c(5.5, 8.5, 2.2), c(18.5, 8.5, 2.2), 'M7 20v-1a5 5 0 0 1 10 0v1', 'M1.5 19v-.5a4 4 0 0 1 5.5-3.7', 'M22.5 19v-.5a4 4 0 0 0-5.5-3.7'],
  pin: ['M12 21s-7-6.5-7-12a7 7 0 0 1 14 0c0 5.5-7 12-7 12Z', c(12, 9, 2.5)],
  phone: ['M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2Z'],
  clock: [c(12, 12, 9), 'M12 7v5l3 2'],
  mail: ['M5 5h14a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2Z', 'm3 7 9 6 9-6'],
  facebook: ['M14 8h3V4h-3a4 4 0 0 0-4 4v2H8v4h2v8h4v-8h3l1-4h-4V8.5c0-.3.2-.5.5-.5Z'],
  instagram: ['M8 3h8a5 5 0 0 1 5 5v8a5 5 0 0 1-5 5H8a5 5 0 0 1-5-5V8a5 5 0 0 1 5-5Z', c(12, 12, 4), c(17.5, 6.5, 0.4)],
  leaf: ['M5 19C5 10 10 5 20 4c-1 10-6 15-15 15Z', 'M5 19l8-8'],
  pot: ['M4 10h16v6a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4v-6Z', 'M2 10h20', 'M9 10V7h6v3', 'M12 4v3'],
  heart: ['M12 20s-8-4.6-8-10.3A4.7 4.7 0 0 1 12 7a4.7 4.7 0 0 1 8 2.7C20 15.4 12 20 12 20Z'],
  check: ['m5 12 5 5 9-10'],
  car: ['M3 17h18v-5l-2-5H5l-2 5v5Z', 'M3 12h18', c(7.5, 17, 1.8), c(16.5, 17, 1.8)],
  monitor: ['M4.5 4h15A1.5 1.5 0 0 1 21 5.5v9a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 14.5v-9A1.5 1.5 0 0 1 4.5 4Z', 'M8 20h8', 'M12 16v4'],
  cloche: ['M3 18h18', 'M5 18a7 7 0 0 1 14 0', 'M12 11V8', 'M10 8h4'],
  noodles: ['M3 12h18a9 9 0 0 1-18 0Z', 'M8 12c0-3 2-3 2-6', 'M12 12c0-3 2-3 2-6', 'M15 3l6 3'],
  shrimp: ['M18 5a6 6 0 0 0-11 3c0 4 4 6 8 6h2', 'M7 8c-2 1-3 3-3 5a5 5 0 0 0 5 5h3', 'M10 15l-2 4', 'M13 14l-1 5', 'M18 5l3-2'],
  calendar: ['M5 5h14a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2Z', 'M3 10h18', 'M8 3v4', 'M16 3v4'],
  arrow: ['M5 12h14', 'M13 6l6 6-6 6'],
  menu: ['M4 7h16', 'M4 12h16', 'M4 17h16'],
  close: ['M6 6l12 12', 'M18 6 6 18'],
  prev: ['m15 6-6 6 6 6'],
  next: ['m9 6 6 6-6 6'],
};

@Component({
  selector: 'app-icon',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `<svg viewBox="0 0 24 24" [attr.width]="size" [attr.height]="size" fill="none"
    stroke="currentColor" [attr.stroke-width]="stroke" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true" focusable="false"><path *ngFor="let d of paths" [attr.d]="d"></path></svg>`,
  styles: [':host{display:inline-flex;line-height:0}'],
})
export class IconComponent {
  @Input() name = '';
  @Input() size: number | string = 24;
  @Input() stroke = 1.6;

  get paths(): string[] {
    return ICONS[this.name] ?? [];
  }
}
