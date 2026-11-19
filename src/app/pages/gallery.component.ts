import { Component, HostListener } from '@angular/core';
import { GALLERY } from '../site.data';

@Component({ selector: 'app-gallery', templateUrl: './gallery.component.html' })
export class GalleryComponent {
  readonly images = GALLERY;
  active: number | null = null;

  open(i: number): void {
    this.active = i;
  }

  close(): void {
    this.active = null;
  }

  step(delta: number): void {
    if (this.active === null) {
      return;
    }
    const n = this.images.length;
    this.active = (this.active + delta + n) % n;
  }

  @HostListener('document:keydown', ['$event'])
  onKey(e: KeyboardEvent): void {
    if (this.active === null) {
      return;
    }
    if (e.key === 'Escape') {
      this.close();
    } else if (e.key === 'ArrowRight') {
      this.step(1);
    } else if (e.key === 'ArrowLeft') {
      this.step(-1);
    }
  }
}
